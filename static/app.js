guesses = new Set();
score = 0;

function startGame() {
  $(".start-game").hide();
  $(".board").show();
  $(".guess-form").show();
  setInterval(updateTimer, 1000);
  $(".guess").focus();
}

$(".start-game").click(startGame);

async function formSubmit(evt) {
  evt.preventDefault();

  const $guess = $(".guess");
  let guess = $guess.val();

  if (!guess) {
    $guess.focus();
    return;
  }

  if (guesses.has(guess)) {
    sendMsg(`${guess} - Already Found`, "caution");
    $guess.val("").focus();
    return;
  }

  const res = await axios.get("/verify-guess", { params: { guess: guess } });

  if (res.data.result === "not-a-word") {
    sendMsg(`${guess} - Not a Valid Word`, "invalid");
  } else if (res.data.result === "not-on-board") {
    sendMsg(`${guess} - Not Found`, "caution");
  } else {
    $(".guesses").append(`<li>${guess.toUpperCase()}</li>`);
    score += guess.length;
    updateScore();
    guesses.add(guess);
    sendMsg(`${guess}, Found`, "valid");
  }

  $guess.val("").focus();
}

$(".guess-form").submit(formSubmit);

function sendMsg(msg, type) {
  $(".msg").text(msg).removeClass().addClass(`msg ${type}`);
}

function updateScore() {
  $(".score").text(score);
}

time = 59;
function updateTimer() {
  if (time >= 10) {
    $(".timer").text(`00:${time}`);
  } else if (time < 10 && time >= 0) {
    $(".timer").text(`00:0${time}`);
  }
  if (time === 0) {
    gameOver();
  }
  time--;
}

async function gameOver() {
  $(".start-game").show();
  $(".guess-form").hide();
  guesses.clear();

  const res = await axios.post("/post-stats", { score: score });

  if (res.data.newRecord) {
    sendMsg(`New Record: ${score}`, "valid");
  } else {
    sendMsg(`Total Score: ${score}`, "valid");
  }
}
