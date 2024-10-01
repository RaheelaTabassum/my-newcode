# # from flask import Blueprint

# # # my_blueprint = Blueprint('MyBlueprint', __name__, url_prefix='/webhook')
# # # Blueprints help you organize your web application into smaller, manageable pieces. This makes it easier to build and maintain.
# # webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# # # my_blueprint = Blueprint('MyBlueprint', __name__, url_prefix='/webhook')
# # # Blueprints help you organize your web application into smaller, manageable pieces. This makes it easier to build and maintain.
# # # webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# # from .routes import *
# from flask import Flask

# from app.webhook.routes import webhook

# app = Flask(__name__)

# # Creating our flask app
# def create_app():

   
   
#     # registering all the blueprints
#     app.register_blueprint(webhook)
 
    
#     return app
