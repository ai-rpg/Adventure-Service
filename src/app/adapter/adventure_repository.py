import json
import uuid
from couchbase.options import QueryOptions
from interface.i_adventure_repository import IAdventureRepository
from interface.i_couchbase_repository import ICouchbaseRepository


class AdventureRepsitory(IAdventureRepository):
    def __init__(self, i_couchbase_repo: ICouchbaseRepository):
        self.couchbase_repository = i_couchbase_repo

    def get_all_adventures_for_user(self, user_id):
        pass

    def create_new_adventure(self, user_id, adventure):
        try:
            self.couchbase_repository.cb_coll.upsert(
                str(uuid.uuid4()), adventure.__dict__
            )
        except Exception as e:
            print(e)
