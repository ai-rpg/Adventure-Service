import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import sys

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, "/workspace/ai-rpg/adventure-service/src/app")

from main import app
from services.adventure_service import AdventureService

# import bootstrap


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_base_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_new_adventure(self):
        adventure_service = MagicMock()
        app.dependency_overrides[AdventureService] = lambda: adventure_service

        response = self.client.post(
            "/create",
            json={
                "id": "3163acd1-c119-4e9e-a52f-7d6d642ca021",
                "user_ids": [
                    "c1b73974-999b-492c-8a13-1c21c2663f1f",
                    "d998eec4-57ce-4926-9d12-07044113866d",
                ],
                "intro_text": "intro_text",
                "history": ["one", "two", "three"],
            },
        )

        self.assertEqual(response.status_code, 200)
        adventure_service.create_new_adventure.assert_called_once()

    def test_get_all_adventures_for_user(self):
        adventure_service = MagicMock()
        adventure_service.get_all_adventures_for_user.return_value = {"adventures": []}
        app.dependency_overrides[AdventureService] = lambda: adventure_service

        response = self.client.get("/adventures/123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"adventures": []})
        adventure_service.get_all_adventures_for_user.assert_called_once_with("123")


if __name__ == "__main__":
    unittest.main()
