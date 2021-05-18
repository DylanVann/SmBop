from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from infer import infer

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


class InferData(BaseModel):
    query: str


@app.post("/infer")
def post_infer(body: InferData):
    result = infer(body.query, 'eventlibrary')
    return {"result": result}
