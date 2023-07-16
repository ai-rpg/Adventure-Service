from prometheus_client import Summary, Gauge, Counter, Info

PORT = Info("port", "port")
BASE_ROOT_CALLED = Counter("base_root_called", "base root called")
NEW_ADVENTURE_CALLED = Counter("new_adventure_caled", "new adventure called")
GET_USER_ADVENTURES_CALLED = Counter(
    "get_user_adventures", "gets all the advetures for the user"
)

UPDATE_ADVENTURE_CALLED = Counter("update_adventure", "adventure updated")
