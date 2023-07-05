import json
import uuid
from couchbase.options import QueryOptions

from interface.i_adventure_repository import IAdventureRepository
from interface.i_couchbase_repository import ICouchbaseRepository
from domain.adventure_model import AdventureModel

class AdventureRepsitory(IAdventureRepository):
    def __init__(self, i_couchbase_repo: ICouchbaseRepository):
        self.couchbase_repository = i_couchbase_repo

    def get_all_adventures_for_user(self, user_id):
        #select * from OpenAI._default.adventures where ARRAY_CONTAINS(users,'01026f99-896e-49be-94e1-6e8c2a05dd5e')
        scope = self.couchbase_repository.cb.scope("_default")
        sql_query = "select * from OpenAI._default.adventures where ARRAY_CONTAINS(users, $1)"
        row_iter = scope.query(
            sql_query, QueryOptions(positional_parameters=[user_id])
        )
        adventures = []
        for row in row_iter:
            result:AdventureModel= AdventureModel(
                row['adventures']['adventure_id'],
                row['adventures']['users'],
                row['adventures']['intro_text'], 
                row['adventures']['history'])
            adventures.append(result)
        return adventures

    def create_new_adventure(self, user_id, adventure):
        try:
            self.couchbase_repository.cb_coll.upsert(
                str(uuid.uuid4()), adventure.__dict__
            )
        except Exception as e:
            print(e)
