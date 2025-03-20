from typing import Union

from fastapi import FastAPI, Path

from pydantic import BaseModel

app = FastAPI()

store = []
class Item(BaseModel):
    item_id : int
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return "Hello World"


@app.get("/items/")
def read_item():
    return store

@app.get("/items/{id}")
def read_by_id(id:int):
    id = id - 1
    return store[id]

@app.put("/items/{id}")
def update(id:int , item:Item):
    store[id-1] = item
    return store

#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.price, "item_id": item_id}
#
@app.post("/create-items/")
def create_item(item: Item):
    store.append(dict(item))
    return item

# @app.get("/hello/{name}")
# def read_item(*,name: str=Path(...,min_length=3 , max_length=10), age: Union[int, None] = None):
#     return {"name": name, "age": age}