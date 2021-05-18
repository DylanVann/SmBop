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

    conn = sqlite3.connect('dataset/database/eventlibrary/eventlibrary.sqlite', check_same_thread=False)
    try:
        cursor = conn.cursor()
        cursor.execute(inferredSql)
        jsonResult = json.dumps(cursor.fetchall(), default=datetime_handler, indent=2)
    except sqlite3.OperationalError as e:
        errorString = str(e)
        jsonResult = f'''Query failed.
        
        {errorString}
        '''
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
