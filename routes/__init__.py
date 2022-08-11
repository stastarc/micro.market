from fastapi import FastAPI
from . import market
from . import internal

def include(app: FastAPI):
    app.include_router(market.router)
    app.include_router(internal.router)