import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import ItemSchema, ItemUpdateSchema
from db import items, stores


#Create a flask_smorest blue print object 
blp = Blueprint("items", __name__, description="Operaions on items")


#Inherit class from MethodView and decorate the class with endpoint route
@blp.route("/item/<string:item_id>")
class Item(MethodView):
# def the endpoint methods
    # get an item
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not Found.")


    # delte an item
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(400, message="Item not found.")

    
    # update an item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):

        try:
            item = items[item_id]
            item |= item_data
            return item
        
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    # get all items
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()       # list of items
    
    # create an item
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self, item_data):
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