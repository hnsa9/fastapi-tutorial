from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

# start server command - uvicorn app:app --reload


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None # none - default value

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None # none - default value

# initialize fastapi instance
app = FastAPI()


# @app.method("/endpoint") - method: get, post, put, delete
@app.get("/")
def home():
    return {"Data": "Test"}

@app.get("/about")
def about():
    return {"Data": "About"}

# path parameter - endpoint
# 1 - id
inventory = {}


# item:type
@app.get("/get-item/{item_id}")
# description - description of request in documentation
# gt - greater than, lt - less than : validate item_id parameter
def get_item(item_id:int = Path(None, description="The ID of the item to view", gt=0)):
    return inventory[item_id]

# query parameter
# name parameter is optional
@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not Found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item with the name found")


# combine query and path parameter
@app.get("/getItem/{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    return {"Data": "Not Found"}

# post request to create item through request body
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error" : "Item ID already exists"}

    inventory[item_id] = item
    # inventory.update(inventory[item_id])
    return inventory[item_id]

# update items - put request
@app.put("/update-item/{item_id}")
def update_item(item_id:int, item:UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exists"}

    if item.name != None:
        inventory[item_id].name = item.name

    if item.brand != None:
        inventory[item_id].brand = item.brand

    if item.price!= None:
        inventory[item_id].price = item.price

    # inventory[item_id].update(item)
    # inventory.update(inventory[item_id])
    return inventory[item_id]

# delete request
@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to be deleted")):
    if item_id not in inventory:
        return {"Error": "ID does not exist."}

    del inventory[item_id]
    return {"Success": "Item deleted"}



