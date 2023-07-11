import unittest
from unittest.mock import Mock

from services.adventure_service import AdventureService
from interface.i_adventure_repository import IAdventureRepository
from domain.adventure_model import AdventureModel

class AdventureServiceTest(unittest.TestCase):
    def setUp(self):
        self.mock_adventure_repo = Mock(spec=IAdventureRepository)
        self.service = AdventureService(self.mock_adventure_repo)

    def test_create_new_adventure(self):
        adventure = AdventureModel("1", [], "Intro 1", "Log 1")
        self.mock_adventure_repo.create_new_adventure.return_value = adventure

        result = self.service.create_new_adventure(adventure)

        self.assertEqual(result, adventure)
        self.mock_adventure_repo.create_new_adventure.assert_called_once_with(1, adventure)

    def test_get_all_adventures_for_user(self):
        user_id = 1
        adventures = [
            AdventureModel("1", [], "Intro 1", "Log 1"),
            AdventureModel("2", [], "Intro 2", "Log 2")
        ]
        self.mock_adventure_repo.get_all_adventures_for_user.return_value = adventures

        result = self.service.get_all_adventures_for_user(user_id)

        self.assertEqual(result, adventures)
        self.mock_adventure_repo.get_all_adventures_for_user.assert_called_once_with(user_id)


if __name__ == '__main__':
    unittest.main()
