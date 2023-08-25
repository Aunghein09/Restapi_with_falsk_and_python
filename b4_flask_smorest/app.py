import uuid
from flask import Flask, request
from db import items, stores
from flask_smorest import abort
app = Flask(__name__)

#endpoint


## endpoint/route = /store; function associated= get_stores() 
@app.get("/store") ##http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if (
        "name" not in store_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'name' is included in json payload"
        )
    for store in stores.values():
        if(
            store_data["name"] == store["name"]
        ):
            abort(
                400,
                message=f"Store already exists."
        )  
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id":store_id}
    stores[store_id] = new_store
    return new_store, 201 # accepted the request


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not Found.")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(400, message="Store not found.")


@app.post("/item")
def create_item():
    item_data = request.get_json()
    print(item_data)
    # here we not only need to validate data exits,
    # but also what type of data, e.g. price should be float
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' is included in json payload"
        )
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(
                400,
                message=f"Item already exists."
        )  
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")

    item_id = uuid.uuid4().hex
    new_item= {**item_data, "id":item_id}
    items[item_id] = new_item
    return new_item, 201 # accepted the request


@app.get("/item")
def get_all_items():
    return {"items" :list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not Found.")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(400, message="Item not found.")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    # There are other validations to do here, we will skip for now
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'price' and 'name' are included."
        )
    try:
        item = items[item_id]
        item |= item_data
        return item
    
    except KeyError:
        abort(404, message="Item not found.")
