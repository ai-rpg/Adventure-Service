import uvicorn
import atexit
from config import HOST, BUILD_VERSION, METRICS_PATH, NAME, HTTPPORT
from flask import Flask, request
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette_prometheus import metrics, PrometheusMiddleware
from metrics import (
    PORT,
    BASE_ROOT_CALLED,
    GET_USER_ADVENTURES_CALLED,
    NEW_ADVENTURE_CALLED,
    UPDATE_ADVENTURE_CALLED
)
from adapter.couchbase_repository import CouchbaseRepository
from adapter.adventure_repository import AdventureRepository
from services.adventure_service import AdventureService
from domain.adventure_model import AdventureModel

from logger import log


class AdventureApp:
    def __init__(
        self, couchbase_repo=None, adventure_repo=None, adventure_service=None
    ):
        if couchbase_repo is None:
            self.couchbase_repo = CouchbaseRepository()
        else:
            self.couchbase_repo = couchbase_repo

        if adventure_repo is None:
            self.adventure_repo = AdventureRepository(self.couchbase_repo)
        else:
            self.adventure_repo = adventure_repo

        if adventure_service is None:
            self.adventure_service = AdventureService(self.adventure_repo)
        else:
            self.adventure_service = adventure_service

        self.security = HTTPBearer()

    def base_root(self):
        log.debug("base route called", extra={"tags": {"application": NAME}})
        BASE_ROOT_CALLED.inc()

    def create_new_adventure(self, model):
        try:
            NEW_ADVENTURE_CALLED.inc()
            return self.adventure_service.create_new_adventure(model)
        except Exception as inst:
            log.error(
                "create_new_adventure",
                extra={"tags": {"application": NAME}},
                exc_info=True,
            )

    async def get_all_adventures_for_user(self, user_id):
        try:
            GET_USER_ADVENTURES_CALLED.inc()
            return await self.adventure_service.get_all_adventures_for_user(user_id)
        except Exception as inst:
            log.error(
                "get_all_adventures_for_user",
                extra={"tags": {"application": NAME}},
                exc_info=True,
            )

    async def update_adventure(self, model):
        try:
            UPDATE_ADVENTURE_CALLED.inc()
            return self.adventure_service.update_adventure(model)
        except Exception as inst:
            log.error(
                "update_adventure", extra={"tags": {"application": NAME}}, exc_info=True
            )

    def goodbye(self):
        log.info("Application Shutting down", extra={"tags": {"application": NAME}})


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


@app.get("/")
def base_root():
    adventureApp.base_root()


@app.post("/create")
def create_new_adventure(user_id: str):
    return adventureApp.create_new_adventure(user_id)


@app.get("/adventures/{user_id}")
async def get_all_adventures_for_user(user_id):
    return await adventureApp.get_all_adventures_for_user(user_id)


@app.post("/update")
async def update_adventure(model: AdventureModel):
    return await adventureApp.update_adventure(model)


adventureApp = AdventureApp()


@atexit.register
def goodbye():
    adventureApp.goodbye()


if __name__ == "__main__":
    log.info("Application Starting up", extra={"tags": {"application": NAME}})

    uvicorn.run("main:app", host=HOST, port=int(HTTPPORT), log_level="debug")
