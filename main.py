import os
from flask import Flask, render_template, redirect, url_for
from application.config import LocalDevelopmentConfig, StageConfig     
from application.database import db
from application import workers
from application.models import *
from flask_restful import Api
from flask_security import Security, current_user, login_required, auth_required, hash_password, SQLAlchemySessionUserDatastore, UserDatastore
from flask_sse import sse
from flask_cors import CORS
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

from wtforms import SelectField
from flask_security.forms import RegisterForm


class ExtendedRegisterForm(RegisterForm):
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User'), ('superuser', 'Superuser')])      

# applying logging in the project
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)



app, api, celery = None, None, None
def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development")== "production":
        # app.logger.info("Currently no production is being setup")
        raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "stage":
        app.logger.info("Staring stage.")
        app.config.from_object(StageConfig)
    else:
        # app.logger.info("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    api=Api(app)
    app.security = Security(app, user_datastore)# to pass your user form {register_form=ExtendedRegisterForm}
    # with app.app_context():
        # Create a user to test with
        # init_db()
        # db.create_all()
        # To initialize the roles in the role table
    roles = [
            ('admin', 'Administrator'),
            ('user', 'User'),
            ('superuser', 'Superuser')
        ]
    for name, description in roles:
        role = Role.query.filter_by(name=name).first()
        if role is None:
            role = Role(name=name, description=description)
            db.session.add(role)
    db.session.commit()
    # To add admin on initializing of database
    role = Role.query.filter_by(name='admin').first()
    if not app.security.datastore.find_user(email="sk9666338@gmail.com"):
        app.security.datastore.create_user(email="sk9666338@gmail.com", password=hash_password("password"))
    db.session.commit()
    user=app.security.datastore.find_user(email="sk9666338@gmail.com")
    app.security.datastore.add_role_to_user(user=user,role=role)
    db.session.commit()
    
    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone = app.config["CELERY_TIMEZONE"],
        broker_connection_retry_on_startup=app.config["BROKER_CONNECTION_RETRY_ON_STARTUP"]
    )
    celery.conf.timezone = 'Asia/Kolkata' 


    celery.Task = workers.ContextTask
    app.app_context().push()
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app, api, celery

app, api, celery = create_app()

# # Load the Gmail API credentials from the JSON key file
# credentials = service_account.Credentials.from_service_account_file(
#     app.config['GMAIL_CREDS_FILE'],
#     scopes=['https://www.googleapis.com/auth/gmail.modify']
# )
# # Build the Gmail service
# gmail_service = build('gmail', 'v1', credentials=credentials, cache_discovery=False)

# import all the controllers so they are loaded
app.logger.info("Starting local development")

# This is for streaming
app.register_blueprint(sse, url_prefix='/stream')

@app.errorhandler(404)
def page_not_found(e):
    # setting 404 status explicitly
    return render_template('404.html'), 404

from application.adminControllers import *
from application.userControllers import *
from application.welcome import *


from application.api import venueApi, showApi, userApi, topthreeapi,topgenresapi,specificvenueApi,searchApi,specificshowApi
api.add_resource(venueApi, '/api/get/venue', '/api/get/venue/<int:venue_id>')
api.add_resource(specificvenueApi,'/api/location/<string:venue_location>')
api.add_resource(specificshowApi,'/api/get/one/show/<int:show_id>')
api.add_resource(searchApi,'/api/search/<string:search_words>')
api.add_resource(showApi, '/api/get/show', '/api/get/show/<int:show_id>')
api.add_resource(userApi, '/api/get/user', '/api/get/user/<int:id>')
api.add_resource(topthreeapi, '/api/get/top3/movies')
api.add_resource(topgenresapi, '/api/get/top/genres')


if __name__=="__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000)