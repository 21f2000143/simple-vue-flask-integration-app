from flask_restful import Resource, fields, marshal_with, reqparse, marshal
from application.database import db
from .models import *

# Define marshaling for models
venue_fields = {
    "venue_id": fields.Integer,
    "venue_name": fields.String,
    "venue_place": fields.String,
    "venue_capacity": fields.Integer,
    "venue_location": fields.String,
    "price_factor": fields.Float,
    "venue_visitors": fields.Integer,
    "venue_revenue": fields.Float,
    "shows": fields.List(fields.Nested({
        "show_id": fields.Integer,
        "show_name": fields.String,
        "show_tag": fields.String,
        "show_price": fields.Float,
        "show_stime": fields.DateTime(dt_format='iso8601'),
        "show_etime": fields.DateTime(dt_format='iso8601')
    }))
}

show_fields = {
    "show_id": fields.Integer,
    "show_name": fields.String,
    "img_name": fields.String,
    "show_likes": fields.Integer,
    "show_tag": fields.String,
    "show_price": fields.Float,
    "show_watched": fields.Integer,
    "show_collection": fields.Float,
    "show_stime": fields.DateTime(dt_format='iso8601'),
    "show_etime": fields.DateTime(dt_format='iso8601'),
    "show_date": fields.DateTime(dt_format='iso8601'),
    "venues": fields.List(fields.Nested({
        "venue_id": fields.Integer,
        "venue_name": fields.String,
        "venue_place": fields.String,
        "venue_capacity": fields.Integer,
        "venue_location": fields.String,
        "price_factor": fields.Float
    }))
}

ticket_fields = {
    "ticket_id": fields.Integer,
    "venue_name": fields.Integer,
    "show_name": fields.Integer,
    "no_seats": fields.Integer,
    "show_stime": fields.DateTime(dt_format='iso8601'),
    "show_etime": fields.DateTime(dt_format='iso8601'),
    "show_date": fields.DateTime(dt_format='iso8601'),
    "book_time": fields.DateTime(dt_format='iso8601'),
    "amount_paid": fields.Float,
    "user_id": fields.Integer
}

# Define request parsers
venue_parser = reqparse.RequestParser()
venue_parser.add_argument("venue_name", type=str, required=True)
venue_parser.add_argument("venue_place", type=str, required=True)
venue_parser.add_argument("venue_capacity", type=int, required=True)
venue_parser.add_argument("venue_location", type=str, required=True)
venue_parser.add_argument("price_factor", type=float)

show_parser = reqparse.RequestParser()
show_parser.add_argument("show_name", type=str, required=True)
show_parser.add_argument("img_name", type=str)
show_parser.add_argument("show_tag", type=str, required=True)
show_parser.add_argument("show_price", type=float, required=True)
show_parser.add_argument("show_stime", type=str)
show_parser.add_argument("show_etime", type=str)
show_parser.add_argument("show_date", type=str)

ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument("venue_name", type=int, required=True)
ticket_parser.add_argument("show_name", type=int, required=True)
ticket_parser.add_argument("no_seats", type=int, required=True)
ticket_parser.add_argument("show_stime", type=str)
ticket_parser.add_argument("show_etime", type=str)
ticket_parser.add_argument("show_date", type=str)
ticket_parser.add_argument("book_time", type=str)
ticket_parser.add_argument("amount_paid", type=float, required=True)
ticket_parser.add_argument("user_id", type=int, required=True)

class VenueResource(Resource):
    @marshal_with(venue_fields)
    def get(self, venue_id):
        venue = Venue.query.get(venue_id)
        if venue:
            return venue
        return {'message': 'Venue not found'}, 404

    @marshal_with(venue_fields)
    def put(self, venue_id):
        args = venue_parser.parse_args()
        venue = Venue.query.get(venue_id)
        if venue:
            for key, value in args.items():
                if value is not None:
                    setattr(venue, key, value)
            db.session.commit()
            return venue
        return {'message': 'Venue not found'}, 404

    def delete(self, venue_id):
        venue = Venue.query.get(venue_id)
        if venue:
            db.session.delete(venue)
            db.session.commit()
            return {'message': 'Venue deleted successfully'}
        return {'message': 'Venue not found'}, 404

class VenueListResource(Resource):
    @marshal_with(venue_fields)
    def get(self):
        venues = Venue.query.all()
        return venues

    @marshal_with(venue_fields)
    def post(self):
        args = venue_parser.parse_args()
        venue = Venue(**args)
        db.session.add(venue)
        db.session.commit()
        return venue, 201

class ShowResource(Resource):
    @marshal_with(show_fields)
    def get(self, show_id):
        show = Show.query.get(show_id)
        if show:
            return show
        return {'message': 'Show not found'}, 404

    @marshal_with(show_fields)
    def put(self, show_id):
        args = show_parser.parse_args()
        show = Show.query.get(show_id)
        if show:
            for key, value in args.items():
                if value is not None:
                    setattr(show, key, value)
            db.session.commit()
            return show
        return {'message': 'Show not found'}, 404

    def delete(self, show_id):
        show = Show.query.get(show_id)
        if show:
            db.session.delete(show)
            db.session.commit()
            return {'message': 'Show deleted successfully'}
        return {'message': 'Show not found'}, 404

class ShowListResource(Resource):
    @marshal_with(show_fields)
    def get(self):
        shows = Show.query.all()
        return shows

    @marshal_with(show_fields)
    def post(self):
        args = show_parser.parse_args()
        show = Show(**args)
        db.session.add(show)
        db.session.commit()
        return show, 201

class TicketResource(Resource):
    @marshal_with(ticket_fields)
    def get(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            return ticket
        return {'message': 'Ticket not found'}, 404

    @marshal_with(ticket_fields)
    def put(self, ticket_id):
        args = ticket_parser.parse_args()
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            for key, value in args.items():
                if value is not None:
                    setattr(ticket, key, value)
            db.session.commit()
            return ticket
        return {'message': 'Ticket not found'}, 404

    def delete(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            db.session.delete(ticket)
            db.session.commit()
            return {'message': 'Ticket deleted successfully'}
        return {'message': 'Ticket not found'}, 404

class TicketListResource(Resource):
    @marshal_with(ticket_fields)
    def get(self):
        tickets = Ticket.query.all()
        return tickets

    @marshal_with(ticket_fields)
    def post(self):
        args = ticket_parser.parse_args()
        ticket = Ticket(**args)
        db.session.add(ticket)
        db.session.commit()
        return ticket, 201

# Define marshaling for the User model
user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String,
    "profile_img": fields.String,
    "last_login_at": fields.DateTime(dt_format='iso8601'),
    "current_login_at": fields.DateTime(dt_format='iso8601'),
    "last_login_ip": fields.String,
    "current_login_ip": fields.String,
    "login_count": fields.Integer,
    "active": fields.Boolean,
    "mobile": fields.String,
    "confirmed_at": fields.DateTime(dt_format='iso8601')
}

# Define request parser for User
user_parser = reqparse.RequestParser()
user_parser.add_argument("email", type=str, required=True)
user_parser.add_argument("username", type=str, required=True)
user_parser.add_argument("password", type=str, required=True)
user_parser.add_argument("profile_img", type=str)
user_parser.add_argument("mobile", type=str)

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user
        return {'message': 'User not found'}, 404

    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_parser.parse_args()
        user = User.query.get(user_id)
        if user:
            for key, value in args.items():
                if value is not None:
                    setattr(user, key, value)
            db.session.commit()
            return user
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        return {'message': 'User not found'}, 404

class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return user, 201

# Define routes
api.add_resource(VenueResource, '/venues/<int:venue_id>')
api.add_resource(VenueListResource, '/venues')
api.add_resource(ShowResource, '/shows/<int:show_id>')
api.add_resource(ShowListResource, '/shows')
api.add_resource(TicketResource, '/tickets/<int:ticket_id>')
api.add_resource(TicketListResource, '/tickets')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')
