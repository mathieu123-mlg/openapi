from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse

app = FastAPI()


class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: str


post_stored: List[Post] = []


@app.get("/ping")
def hello():
    return Response(content="pong", status_code=200, media_type="text/plain")


@app.get("/home")
def home():
    return Response("<html><body><h1>Welcome home!</h1></body></html>", status_code=200, media_type="text/html")


@app.post("/posts")
def create_post(post_payload: List[Post]):
    post_stored.extend(post_payload)
    post_serialized = serialize_posts()
    return JSONResponse(content=post_serialized, status_code=201, media_type="application/json")


def serialize_posts():
    post_serialized = []
    for p in post_stored:
        post_serialized.append(p.model_dump())
    return post_serialized


@app.get("/posts")
def list_posts():
    return JSONResponse(content=serialize_posts(), status_code=200, media_type="application/json")


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return Response(content="<html><body><h1>404 NOT FOUND</h1></body></html>", status_code=404
                    , media_type="text/html")
