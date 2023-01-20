from app import app
from boggle import Boggle
from flask import session
from unittest import TestCase


class FlaskTests(TestCase):
    def test_home(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("board", session)
            self.assertIn('<p>Score: <span class="score">0</span></p>', html)
            self.assertIn('<p>Time: <span class="timer">1:00</span></p>', html)
            self.assertIsNone(session.get("highscore"))

    def test_verify_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session["board"] = [
                    ["A", "A", "A", "A", "A"],
                    ["A", "A", "A", "A", "A"],
                    ["A", "A", "B", "A", "A"],
                    ["A", "A", "A", "A", "A"],
                    ["A", "A", "A", "A", "A"],
                ]

            res = client.get("/verify-guess?guess=b")

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json["result"], "ok")

    def test_invalid_guess(self):
        with app.test_client() as client:
            make_board = client.get("/")
            res = client.get("/verify-guess?guess=asdfg")

            self.assertEqual(res.json["result"], "not-a-word")

    def test_not_on_board(self):
        with app.test_client() as client:
            make_board = client.get("/")
            res = client.get("/verify-guess?guess=python")

            self.assertEqual(res.json["result"], "not-on-board")
