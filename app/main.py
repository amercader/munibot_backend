import configparser
import os
from timeit import default_timer as timer
from typing import Optional
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

config = {}

app = FastAPI()
origins = [
    "http://localhost:7777",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search/{code}")
def search(code: str, q: Optional[str] = None):

    t1 = timer()

    out = _search(code, q)

    t2 = timer()

    out["t"] = t2 - t1

    return out


def _search(code, q):

    load_config()

    if f"profile:{code}" not in config:
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


def load_config(path=None):

    if not path:
        path = os.environ.get("MUNIBOT_CONFIG_FILE")

    if not path or not os.path.exists(path):
        raise ValueError(
            """
INI file not found. It must be a "munibot.ini" file in the current directory,
otherwise pass the location with the "--config" parameter""".strip()
        )

    cp = configparser.RawConfigParser()
    cp.read(path)
    for section in cp.sections():
        config[section] = dict(cp[section])
