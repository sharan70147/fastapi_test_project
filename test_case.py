from fastapi.testclient import TestClient
from fastapi import status
from books import app

client = TestClient(app=app)

def test_one():
    response = client.get("/books/list/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
  {
    "title": "string",
    "author": "string",
    "publisher": "string",
    "id": 1
  },
  {
    "title": "string2",
    "author": "string2",
    "publisher": "string2",
    "id": 2
  }
]

def test_two():
    response = client.post("/book/add/" ,json={
            "title": "string",
            "author": "string",
            "publisher": "string",
            "id": 3
        })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
            "title": "string",
            "author": "string",
            "publisher": "string",
            "id": 3
        }


def test_three():
    response = client.get("/v2/book/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
    "title": "string",
    "author": "string",
    "publisher": "string",
    "id": 1
  }

