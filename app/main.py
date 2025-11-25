import configparser
import os
from timeit import default_timer as timer
from typing import Optional
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_MUNIBOT_DB = "/opt/munibot/munibot.sqlite"

config = {}

app = FastAPI()
origins = [
    "http://localhost:7777",
    "https://munibot.amercader.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/search/{code}")
def search(code: str, q: str):

    t1 = timer()

    out = _search(code, q)

    t2 = timer()

    out["t"] = t2 - t1

    return out


def _search(code, q):

    db_path = load_db_path()

    profiles = get_profiles()

    if code not in profiles:
        raise HTTPException(status_code=404, detail="Unknown munibot")

    out = {"results": []}

    sql = f"""
        SELECT fullname, xmin, ymin, xmax, ymax
        FROM {code}
        WHERE fullname LIKE ?
        ORDER BY fullname
        LIMIT 100
        """
    params = (q + "%",)
    with sqlite3.connect(config[f"profile:{code}"]["db_path"]) as db:
        data = db.execute(sql, params)
        for row in data:
            out["results"].append(
                {"name": row[0], "extent": [row[1], row[2], row[3], row[4]]}
            )
    return out


def load_db_path():

    path = os.environ.get("MUNIBOT_DB_FILE", DEFAULT_MUNIBOT_DB)

    if not path or not os.path.exists(path):
        raise ValueError(f"Database file not found: {path}")

    return path


def get_profiles(db_path):

    with sqlite3.connect(db_path) as db:
        out = db.execute(
            "SELECT name FROM sqlite_master  WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    return [t[0] for t in out]
