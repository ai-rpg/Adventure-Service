import abc


class IAdventureRepository(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def get_all_adventures_for_user(self, user_id):
        raise NotImplementedError

    @abc.abstractclassmethod
    def create_new_adventure(self, user_id, adventure):
        raise NotImplementedError
