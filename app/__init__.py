__all__ = ['api_calendar', 'mod_auth', 'mod_base']

from flask import Flask, render_template, current_app, send_from_directory, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os
import re

from app.mod_auth.auth import AuthError

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path, track_modifications=False):
    if database_path:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = track_modifications
    db.app = app
    db.init_app(app)

'''
create_app(config)
    creates the flask application
'''
def create_app(config='config'):
    # Define the WSGI application object
    app = Flask(__name__)

    # Configurations
    app.config.from_object(config)
    app.config['CORS_HEADERS'] = 'Content-Type'

    if 'DATABASE_URL' in os.environ:
        database_path = os.environ['DATABASE_URL']
    else:
        database_path = None
    setup_db(app, database_path)
    CORS(app)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_api.controllers import mod_api as api_module

    # Register blueprint(s)
    app.register_blueprint(api_module)

    @app.route('/', methods=['GET'])
    def index():
        return redirect("/api/calendars/", code=302)

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
                             #'Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept"
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PATCH, DELETE')
        return response

    '''
    Error handler for 400: bad request
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400

    '''
    Error handler for 404
        error handler should conform to general task above 
    '''
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "internal server error"
        }), 500

    '''
    Error handler for AuthError
        error handler should conform to general task above 
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False, 
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    # Create the Flask-Migrate object
    migrate = Migrate(app, db)

    return app

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy()

# Create the app
app = create_app()
