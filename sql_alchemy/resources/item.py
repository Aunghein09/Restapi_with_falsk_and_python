import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from schemas import ItemSchema, ItemUpdateSchema

from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError


#Create a flask_smorest blue print object 
blp = Blueprint("items", __name__, description="Operaions on items")


#Inherit class from MethodView and decorate the class with endpoint route
@blp.route("/item/<string:item_id>")
class Item(MethodView):
# def the endpoint methods
    # get an item
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item


    # delte an item
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted."}
    
    # update an item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(**item_data, id=item_id)
        
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    # get all items
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()       # list of items
    
    # create an item
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self, item_data):
        
        item = ItemModel(**item_data)       # Item model will check the required fields

        try:
            db.session.add(item)
            db.session.commit()             # write to disk
        except SQLAlchemyError:
            abort(500, message="An error occur while inserting the item.")

        return item, 201 # accepted the request

