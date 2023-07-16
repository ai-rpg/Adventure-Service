from interface.i_adventure_service import IAdventureService
from interface.i_adventure_repository import IAdventureRepository
from domain.adventure_model import AdventureModel, Conversation

import uuid


class AdventureService(IAdventureService):
    def __init__(self, i_adventure_repository: IAdventureRepository):
        self.adventure_repo = i_adventure_repository

    def create_new_adventure(self, user_id):
        adventure = AdventureModel(str(uuid.uuid4()))
        adventure.gamelog.append(
            Conversation(
                "system",
                "Assume the role of an expert in the characters, scenarios, locations, and plot of the D&D adventure The Lost Mine of Phandelver. As an expert be my Dungeon Master in a roleplaying game based on this adventure. Give a narrative description of everything that follows, based on my actions, in the style of R.A Salvatore, without taking control of me or my character. Also, give suitable names for characters and places.",
            ).toJSON()
        )
        adventure.users.append(user_id)

        return self.adventure_repo.create_new_adventure(adventure)

    def get_all_adventures_for_user(self, user_id):
        return self.adventure_repo.get_all_adventures_for_user(user_id)

    def update_adventure(self, adventure):
        new_adventure = AdventureModel(adventure.adventure_id)
        for log in adventure.gamelog:
            new_adventure.gamelog.append(Conversation(log.role, log.content).toJSON())

        new_adventure.users = adventure.users
        return self.adventure_repo.update_adventure(new_adventure)
