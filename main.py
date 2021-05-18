from infer import infer
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Form
import datetime
import sqlite3

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@app.post("/slack")
def post_slack(text: str = Form(...)):
    inferredSql = infer(text, 'eventlibrary')
    conn = sqlite3.connect('dataset/database/eventlibrary/eventlibrary.sqlite')
    cursor = conn.cursor()

    # conn = psycopg2.connect(
    #     database="event_library",
    #     user="postgres",
    #     password="HHn7zyuiTjXzA7Peg9mA3oJjGrWfpCmv",
    #     host="event-library-3241.codnnlrpojpl.us-east-1.rds.amazonaws.com",
    #     port="5432",
    #     options=f'-c search_path=app_public'
    # )
    # cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # cur.execute(inferredSql)
        cursor.execute(inferredSql)
        jsonResult = json.dumps(cursor.fetchall(), default=datetime_handler, indent=2)
    except:
        jsonResult = "No json for you."
    finally:
        conn.close()

    resultMarkdown = f'''*Question:*
`{text}`

*Inferred SQL*:
`{inferredSql}`

*Result:*
```{jsonResult}```'''

    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": resultMarkdown
                }
            }
        ]
    }
