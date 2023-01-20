from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session


app = Flask(__name__)
app.config["SECRET_KEY"] = "abc123"

boggle_game = Boggle()


@app.route("/")
def home():
    """Display and Start Game"""

    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    attempts = session.get("attempts", 0)

    return render_template(
        "index.html", board=board, highscore=highscore, attempts=attempts
    )


@app.route("/verify-guess")
def verify_guess():
    """Check if guess is a valid word"""

    board = session["board"]
    guess = request.args["guess"]
    res = boggle_game.check_valid_word(board, guess)

    return jsonify({"result": res})


@app.route("/post-stats", methods=["POST"])
def post_score():
    """Get score, update # of attempts and high score when record is broken"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    attempts = session.get("attempts", 0)

    session["attempts"] = attempts + 1
    session["highscore"] = max(score, highscore)

    return jsonify(newRecord=score > highscore)
