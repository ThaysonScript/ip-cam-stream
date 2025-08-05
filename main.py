from fastapi import FastAPI
from endpoints import routes

app = FastAPI()

app.include_router(routes.router)