"""Confirm the synthetic fixtures work, including their intended flaws."""

import unittest

from app import app


class FixtureTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_accounts_are_synthetic_and_filtered(self):
        response = self.client.get("/accounts?team=finance")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"accounts": [{"name": "demo-alice", "team": "finance"}]},
        )

    def test_sql_injection_fixture_bypasses_filter(self):
        response = self.client.get(
            "/accounts", query_string={"team": "' OR '1'='1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["accounts"]), 2)

    def test_greeting(self):
        response = self.client.get("/greeting")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "<h1>Hello, demo-user</h1>")

    def test_html_is_deliberately_unescaped(self):
        response = self.client.get(
            "/greeting", query_string={"name": "<em>synthetic</em>"}
        )
        self.assertEqual(response.mimetype, "text/html")
        self.assertIn("<em>synthetic</em>", response.text)


if __name__ == "__main__":
    unittest.main()
