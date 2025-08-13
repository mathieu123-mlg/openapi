import json
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse

app = FastAPI()


class Student(BaseModel):
    reference: str
    first_name: str
    last_name: str
    age: int


students_store: List[Student] = []


@app.get("/hello")
def hello():
    return Response(content="Hello world!", status_code=200, media_type="text/plain")


@app.get("/welcome")
def welcome(name: str):
    return Response(content=f"Welcome {name}!", status_code=200, media_type="text/plain")


@app.post("/students")
def create_students(students_payload: List[Student]):
    students_store.extend(students_payload)
    students_as_json = []
    for s in students_store:
        students_as_json.append(s.model_dump())
    return JSONResponse(content=students_as_json, status_code=201, media_type="application/json")


@app.get("/students")
def read_students():
    students_as_json = []
    for s in students_store:
        students_as_json.append(s.model_dump())
    return JSONResponse(content=students_as_json, status_code=200, media_type="application/json")
