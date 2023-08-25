import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import stores
from schemas import StoreSchema


#Create a flask_smorest blue print object 
blp = Blueprint("stores", __name__, description="Operaions on stores")


#Inherit class from MethodView and decorate the class with endpoint route
@blp.route("/store/<string:store_id>")
class Item(MethodView):
# def the endpoint methods
# get_store
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not Found.")


# delete store
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(400, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    # get all stores
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    

    # create a store
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self, store_data):

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