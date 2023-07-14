import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

import sys

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, "/workspace/ai-rpg/adventure-service/src/app")

from main import app, AdventureApp, AdventureModel


class AdventureAppTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.adventure_repo = MagicMock()
        self.couchbase_repo = MagicMock()
        self.adventure_service = MagicMock()
        self.adventure_app = AdventureApp(
            couchbase_repo=self.couchbase_repo,
            adventure_repo=self.adventure_repo,
            adventure_service=self.adventure_service,
        )

    def test_base_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_create_new_adventure(self):
        adventure_model = AdventureModel("1", "this is the intro")
        self.adventure_app.adventure_service.create_new_adventure = MagicMock()
        self.client.post("/create", json=adventure_model)
        # Add assertions to check the behavior of the create_new_adventure method

    def test_get_all_adventures_for_user(self):
        user_id = 123  # Provide a valid user ID for testing
        self.adventure_app.adventure_service.get_all_adventures_for_user = MagicMock(
            return_value="Test Adventures"
        )
        response = self.client.get(f"/adventures/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Test Adventures")
        # Add more assertions as needed

    def test_goodbye(self):
        self.adventure_app.goodbye()
        # Add assertions to check the behavior of the goodbye method


if __name__ == "__main__":
    unittest.main()
