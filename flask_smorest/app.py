from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


app = Flask(__name__)


app.config["PROPAGATE_EXCEPTIONS"] = True               # config to propagate exceptions from extensions to main app
app.config["API_TITLE"] = "Stores REST API"             # title for documentation
app.config["API_VERSION"] = "v1"                        # our api version
app.config["OPENAPI_VERSION"] = "3.0.3"                 # open api documentation version
app.config["OPENAPI_URL_PREFIX"] = "/"                  # our endpoints start from here
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"    # swagger url (pee yin d mhr page paw lr)
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # where swagger info live


api = Api(app)                                          # connect flask app with smorest extension


api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

