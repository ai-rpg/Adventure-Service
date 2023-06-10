from config import BUILD_VERSION, METRICS_PATH, NAME

from flask import Flask, request
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from starlette_prometheus import metrics, PrometheusMiddleware
from metrics import PORT

from adapter.couchbase_repository import CouchbaseRepository
from adapter.adventure_repository import AdventureRepsitory


PORT.info({"port": "8000"})

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origains=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route(("/" + METRICS_PATH), metrics)
couchbaseRepo = CouchbaseRepository()
adventureRepo = AdventureRepsitory(couchbaseRepo)


@app.post("/")
def base_root(request: Request):
    pass
