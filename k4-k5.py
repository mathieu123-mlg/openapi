from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()


@app.get("/hello")
def hello():
    return Response(content="Hello world!", status_code=200, media_type="text/plain")

@app.get("/welcome")
def welcome(name: str):
    return Response(content=f"Welcome {name}!" , status_code=200, media_type="text/plain")