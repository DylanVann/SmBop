from typing import Optional
from typing import Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI
from infer import infer
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


class InferData(BaseModel):
    text: str


@app.post("/slack")
def post_infer(data: Dict[Any, Any] = None):
    print('-----------------------------------------------')
    print('data', data)
    print('-----------------------------------------------')
    inferredSql = infer(data.text, 'eventlibrary')
    conn = psycopg2.connect(
        database="event_library",
        user="postgres",
        password="HHn7zyuiTjXzA7Peg9mA3oJjGrWfpCmv",
        host="event-library-3241.codnnlrpojpl.us-east-1.rds.amazonaws.com",
        port="5432",
        options=f'-c search_path=app_public'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(inferredSql)
    jsonResult = json.dumps(cur.fetchall(), default=datetime_handler, indent=2)
    conn.close()
    return {"result": inferredSql, "data": jsonResult}
