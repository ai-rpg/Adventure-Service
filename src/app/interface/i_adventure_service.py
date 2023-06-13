import abc
from domain.adventure_model import AdventureModel

class IAdventureService(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def create_new_adventure(self, adventure: AdventureModel):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_all_adventures_for_user(self, user_id):
        raise NotImplementedError