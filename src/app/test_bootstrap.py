import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from bootstrap import app
from services.adventure_service import AdventureService
from domain.adventure_model import AdventureModel

class AdventureServiceUnitTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.token = "your_jwt_token_here"

    def test_create_new_adventure(self):
        AdventureService.create_new_adventure = MagicMock()
        headers = {"Authorization": f"Bearer {self.token}"}
       
        response = self.client.post('/create',headers=headers, json={
            "adventure_id": "3163acd1-c119-4e9e-a52f-7d6d642ca021",
            "users": ['c1b73974-999b-492c-8a13-1c21c2663f1f', 'd998eec4-57ce-4926-9d12-07044113866d'],
            "intro_text": "intro_text",
            "game_log": ['one', 'two', 'three']
        })

        self.assertEqual(response.status_code, 200)
        AdventureService.create_new_adventure.assert_called_once_with(AdventureModel(
            "3163acd1-c119-4e9e-a52f-7d6d642ca021",
            ['c1b73974-999b-492c-8a13-1c21c2663f1f', 'd998eec4-57ce-4926-9d12-07044113866d'],
            'intro_text',
            ['one', 'two', 'three']
        ))

    def test_get_all_adventures_for_user(self):
        AdventureService.get_all_adventures_for_user = MagicMock(return_value=['adventure1', 'adventure2'])

        response = self.client.get('/adventures/123')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['adventure1', 'adventure2'])
        adventureService.get_all_adventures_for_user.assert_called_once_with('123')


if __name__ == '__main__':
    unittest.main()