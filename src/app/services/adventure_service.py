from interface.i_adventure_service import IAdventureService
from interface.i_adventure_repository import IAdventureRepository
from domain.adventure_model import AdventureModel

class AdventureService(IAdventureService):

    def __init__(self, i_adventure_repository: IAdventureRepository):
        self.adventure_repo = i_adventure_repository

    def create_new_adventure(self, adventure: AdventureModel):
        return self.adventure_repo.create_new_adventure(1, adventure)

    def get_all_adventures_for_user(self, user_id):
        return self.adventure_repo.get_all_adventures_for_user(user_id)