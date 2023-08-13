import os
from flask import Flask, render_template, redirect, url_for
from application.config import LocalDevelopmentConfig, StageConfig, TestingConfig     
from application.database import db
from application import workers
from application.models import *
from flask_restful import Api
from application.validation import *
from flask_restful import Resource, fields, marshal_with, reqparse, marshal, output_json
from flask_security import Security, current_user, login_required, auth_required, hash_password, SQLAlchemySessionUserDatastore, UserDatastore
from flask_sse import sse
from flask_cors import CORS
from flask_migrate import Migrate
from flask_caching import Cache
from time import perf_counter_ns
import requests
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



app, api, celery, cache = None, None, None, None
def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development")== "production":
        # app.logger.info("Currently no production is being setup")
        raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "testing":
        app.logger.info("Starting testing.")
        app.config.from_object(TestingConfig)
    elif os.getenv('ENV', "development") == "stage":
        app.logger.info("Staring stage.")
        app.config.from_object(StageConfig)
    else:
        # app.logger.info("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    migrate = Migrate(app, db)
    app.app_context().push()
    db.create_all()
    
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
    cache=Cache(app)
    app.app_context().push()
    api=Api(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app, api, celery, cache

app, api, celery, cache = create_app()

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
show= {
    "show_id": fields.Integer,
    "show_name":fields.String,
    "img_name":fields.String,
    "show_likes":fields.Integer,
    "show_watched":fields.Integer,
    "show_tag": fields.String,
    "show_price": fields.Float,
    "show_collection": fields.Float,
    "show_stime":fields.String,
    "show_etime":fields.String,
    "show_date":fields.String
}
@cache.cached(timeout=50, key_prefix="get_all_venues")
def get_all_venues():
    venues=Venue.query.all()
    return venues
venue={
    "venue_id":fields.Integer,
    "venue_name":fields.String,
    "venue_place":fields.String,
    "venue_capacity": fields.Integer,
    "venue_location": fields.String,
    "price_factor": fields.Float,
    "shows":fields.List(fields.Nested(show)),
}

venue_parser = reqparse.RequestParser()
venue_parser.add_argument("venue_name", type=str)
venue_parser.add_argument("venue_place", type=str)
venue_parser.add_argument("venue_capacity", type=int)
venue_parser.add_argument("venue_location", type=str)
venue_parser.add_argument("price_factor", type=float)

class venueApi(Resource):
    # @auth_required('token')
    def get(self):
        try:
            start=perf_counter_ns()
            venues=get_all_venues()
            # venues=Venue.query.all()
            stop= perf_counter_ns()
            print("time taken", stop-start)
            if venues:
                datalist=[]
                i=1
                for venue in venues:
                    data={}
                    data["seq_no"]=i
                    i=i+1
                    data["venue_id"]=venue.venue_id
                    data["venue_name"]=venue.venue_name
                    data["venue_location"]=venue.venue_location
                    data['shows']=[]
                    for show in venue.shows:
                        data1={}
                        data1['seq_no']=i
                        i=i+1
                        data1["img_name"]=show.img_name
                        data1["show_id"]=show.show_id
                        data1["show_stime"]=show.show_stime.strftime("%H:%m")
                        data1["show_etime"]=show.show_etime.strftime("%H:%m")
                        data1["no_seats"]=(Venue_Shows.query.filter_by(venue_id=venue.venue_id, show_id=show.show_id).first()).no_seats
                        data['shows'].append(data1)
                    datalist.append(data)
                return datalist
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e))
        
    @marshal_with(venue) 
    def put(self, venue_id):
        venue = Venue.query.filter_by(venue_id=int(venue_id)).first()
        if venue:
            args=venue_parser.parse_args()
            if "venue_name" in args:
                venue.venue_name = args["venue_name"]
            if "venue_place" in args:
                venue.venue_place = args["venue_place"]
            if "venue_capacity" in args:
                venue.venue_capacity = args["venue_capacity"]
            if "venue_location" in args:
                venue.venue_location = args["venue_location"]
            if "price_factor" in args:
                venue.price_factor = args["price_factor"]
            db.session.commit()
            return venue
        else:
            raise NotFoundError(status_code=404)
        
    def delete(self, venue_id):
        venue = Venue.query.filter_by(venue_id=venue_id).first()
        if venue is None:
            raise NotFoundError(status_code=400)            
        else:
            try:
                for show in venue.shows:
                    seat=Venue_Shows.query.filter_by(venue_id=venue_id, show_id=show.show_id).first()
                    db.session.delete(seat)
                    db.session.commit()
                    db.session.delete(show)
                    db.session.commit()
                db.session.delete(venue)
                db.session.commit()
                return output_json(data={"message":"successfully deleted"}, code=200)
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))
            
    @marshal_with(venue)
    def post(self):
        args=venue_parser.parse_args()
        venue_name=args.get("venue_name", None)
        venue_place=args.get("venue_place", None)
        venue_capacity=args.get("venue_capacity", None)
        venue_location=args.get("venue_location", None)
        price_factor=args.get("price_factor", None)
        if price_factor is None:
            price_factor=0
        if venue_name is None:
            raise NotFoundError(status_code=400)
        elif venue_place is None:
            raise NotFoundError(status_code=400)
        elif venue_capacity is None:
            raise NotFoundError(status_code=400)
        elif venue_location is None:
            raise NotFoundError(status_code=400)
        else:
            try:
                venue=Venue(venue_name=venue_name, venue_place=venue_place, venue_capacity=venue_capacity, venue_location=venue_location, price_factor=price_factor)
                db.session.add(venue)
                db.session.commit()
                return venue
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))    

from application.api import showApi, userApi, topthreeapi, topgenresapi, specificvenueApi, searchApi, specificshowApi
api.add_resource(venueApi, '/api/get/venue', '/api/get/venue/<int:venue_id>')
api.add_resource(specificvenueApi, '/api/location/<string:venue_location>')
api.add_resource(specificshowApi, '/api/get/one/show/<int:show_id>')
api.add_resource(searchApi, '/api/search/<string:search_words>')
api.add_resource(showApi, '/api/get/show', '/api/get/show/<int:show_id>')
api.add_resource(userApi, '/api/get/user', '/api/get/user/<int:id>')
api.add_resource(topthreeapi, '/api/get/top3/movies')
api.add_resource(topgenresapi, '/api/get/top/genres')

if __name__=="__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000)