from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from infer import infer
import json
import psycopg2
from psycopg2.extras import RealDictCursor

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
    inferredSql = infer(body.query, 'eventlibrary')
    con = psycopg2.connect(database="event_library", user="postgres", password="HHn7zyuiTjXzA7Peg9mA3oJjGrWfpCmv",
                           host="event-library-3241.codnnlrpojpl.us-east-1.rds.amazonaws.com", port="5432",
                           search_path="app_public")
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute(inferredSql)
    jsonResult = json.dumps(cur.fetchall(), indent=2)
    print(jsonResult)
    con.close()
    return {"result": inferredSql, "data": jsonResult}
