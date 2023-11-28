from fastapi import FastAPI
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temp_data = ["hello","world"]
    yield
    

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"temp_data:": app.state.temp_data}