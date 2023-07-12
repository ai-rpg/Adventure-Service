import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/workspace/ai-rpg/adventure-service/src/app')

import unittest

from domain.adventure_model import AdventureModel
from adapter.adventure_repository import AdventureRepsitory
from unittest.mock import MagicMock

class AdventureRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.couchbase_repository_mock = MagicMock()
        self.repository = AdventureRepsitory(self.couchbase_repository_mock)

    def test_get_all_adventures_for_user(self):
        user_id = '01026f99-896e-49be-94e1-6e8c2a05dd5e'
        mock_row_iter = [
            {
                'adventures': {
                    'adventure_id': '123',
                    'users': [user_id],
                    'intro_text': 'Adventure intro text',
                    'history': 'Adventure game log'
                }
            }
        ]
        self.couchbase_repository_mock.cb.scope.return_value.query.return_value = mock_row_iter
        adventures = self.repository.get_all_adventures_for_user(user_id)
        self.assertEqual(len(adventures), 1)
        self.assertIsInstance(adventures[0], AdventureModel)
        self.assertEqual(adventures[0].adventure_id, '123')
        self.assertEqual(adventures[0].users, [user_id])
        self.assertEqual(adventures[0].intro_text, 'Adventure intro text')
        self.assertEqual(adventures[0].game_log, 'Adventure game log')

    def test_create_new_adventure(self):
        user_id = '01026f99-896e-49be-94e1-6e8c2a05dd5e'
        adventure = AdventureModel('123', [user_id], 'Adventure intro text', 'Adventure game log')
        self.repository.create_new_adventure(user_id, adventure)
        self.couchbase_repository_mock.cb_coll.upsert.assert_called_once_with(
            unittest.mock.ANY, adventure.__dict__
        )
if __name__ == '__main__':
    unittest.main()