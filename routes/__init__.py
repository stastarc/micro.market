from fastapi import FastAPI
from . import internal

def include(app: FastAPI):
    app.include_router(internal.router)