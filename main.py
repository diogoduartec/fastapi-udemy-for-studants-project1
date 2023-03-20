from fastapi import FastAPI
from routers import router

app = FastAPI()


@app.get('/')
def hello_world():
    return 'Olá mundo'

app.include_router(router)