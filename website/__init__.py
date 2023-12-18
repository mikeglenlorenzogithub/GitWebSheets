from flask import Flask
from os import path
from .static.get_sheets import get_sheets

def create_app():
    app = Flask(__name__)
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app

def read_sheets():
    sheet = get_sheets('reporting.json', 'REPORTING', 'Report')

    return sheet