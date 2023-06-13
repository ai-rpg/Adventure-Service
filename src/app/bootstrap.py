import uvicorn
from config import BUILD_VERSION, METRICS_PATH, NAME, HOST, HTTPPORT

from flask import Flask, request
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from starlette_prometheus import metrics, PrometheusMiddleware
from metrics import PORT

from adapter.couchbase_repository import CouchbaseRepository
from adapter.adventure_repository import AdventureRepsitory
from services.adventure_service import AdventureService


PORT.info({"port": "8000"})

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route(("/" + METRICS_PATH), metrics)
couchbaseRepo = CouchbaseRepository()
adventureRepo = AdventureRepsitory(couchbaseRepo)
adventureService= AdventureService(adventureRepo)

@app.post("/")
def base_root(request: Request):
    pass

from domain.adventure_model import AdventureModel

@app.get("/create")
async def create_new_adventure():
    model = AdventureModel("3163acd1-c119-4e9e-a52f-7d6d642ca021", ['c1b73974-999b-492c-8a13-1c21c2663f1f','d998eec4-57ce-4926-9d12-07044113866d'], 'intro_text', ['one','two', 'three'])
    adventureService.create_new_adventure(model)

@app.get("/adventures/{user_id}")
async def get_all_adventures_for_user(user_id):
    return adventureService.get_all_adventures_for_user(user_id)



if __name__ == "__main__":
    uvicorn.run("bootstrap:app", host=HOST, port=int(HTTPPORT), log_level="info")
