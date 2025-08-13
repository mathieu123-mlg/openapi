import base64
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
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

@app.put("/posts")
def create_or_update_posts(payload: List[Post]):
    for new_post in payload:
        found = False
        for i, existing_post in enumerate(post_stored):
            if existing_post.title == new_post.title:
                post_stored[i] = new_post
                break
        if not found:
            post_stored.append(new_post)
    return JSONResponse(content=serialize_posts(), status_code=201, media_type="application/json")



@app.get("/ping/auth")
def ping_auth(request: Request):
    admin_encoded_base64 = credentials_encoded()
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header == f"Basic {admin_encoded_base64}":
        return JSONResponse(content="Invalid Authorization header", status_code=401)
    return Response(content="pong", status_code=200, media_type="text/plain")


def credentials_encoded():
    username = "admin"
    password = "123456"
    to_encode = username + ":" + password
    text_bytes = to_encode.encode("utf-8")
    encoded = base64.b64encode(text_bytes)
    return encoded.decode("utf-8")


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return Response(content="<html><body><h1>404 NOT FOUND</h1></body></html>", status_code=404
                    , media_type="text/html")
