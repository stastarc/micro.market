from fastapi import FastAPI
from . import market

def include(app: FastAPI):
    app.include_router(market.router)