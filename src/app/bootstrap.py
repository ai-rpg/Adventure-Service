import uvicorn
from config import HOST, BUILD_VERSION, METRICS_PATH, NAME, HOST, HTTPPORT

from flask import Flask, request
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from starlette_prometheus import metrics, PrometheusMiddleware
from metrics import PORT, BASE_ROOT_CALLED, GET_USER_ADVENTURES_CALLED, NEW_ADVENTURE_CALLED

from adapter.couchbase_repository import CouchbaseRepository
from adapter.adventure_repository import AdventureRepsitory
from services.adventure_service import AdventureService
from logger import log


log.info("Application Starting up", extra={"tags": {"application": NAME}})
PORT.info({"port": HTTPPORT})

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

security = HTTPBearer()

@app.get("/")
def base_root():
    log.debug("base route called", extra={"tags": {"application": NAME}})
    BASE_ROOT_CALLED.inc()
    pass

from domain.adventure_model import AdventureModel


#, credentials: HTTPAuthorizationCredentials = Depends(security)
@app.post("/create")
async def create_new_adventure(model: AdventureModel):
    try:
        NEW_ADVENTURE_CALLED.inc()
        adventureService.create_new_adventure(model)
    except Exception as inst: 
        log.error("create_new_adventure",extra={"tags": {"application": NAME}}, exc_info=True)

@app.get("/adventures/{user_id}")
async def get_all_adventures_for_user(user_id):
    try:
        GET_USER_ADVENTURES_CALLED.inc()
        return await adventureService.get_all_adventures_for_user(user_id)
    except Exception as inst: 
        log.error("get_all_adventures_for_user",extra={"tags": {"application": NAME}}, exc_info=True)


if __name__ == "__main__":
    uvicorn.run("bootstrap:app", host=HOST, port=int(HTTPPORT), log_level="debug")
