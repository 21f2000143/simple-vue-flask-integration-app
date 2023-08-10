from application.database import *
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey, UnicodeText, Float

#Creating models/tables for the the database
class Venue(db.Model):
    __tablename__= 'venue'
    venue_id=Column(Integer, primary_key=True, autoincrement = True)
    venue_name = Column(String, nullable=False)
    venue_place = Column(String, nullable=False)
    venue_capacity = Column(Integer, nullable=False)
    venue_visitors = Column(Integer)
    venue_revenue = Column(Float)
    venue_location = Column(String, nullable=False)
    price_factor = Column(Float)
    shows = relationship('Show', secondary='venue_shows', lazy='subquery',backref=db.backref('venues', lazy=True))

class Show(db.Model):
    __tablename__='show'
    show_id=Column(Integer, primary_key=True, autoincrement=True)
    show_name = Column(String, nullable=False)
    img_name = Column(String)
    show_likes = Column(Integer)
    show_tag = Column(String(20), nullable=False)
    show_price = Column(Float, nullable=False)
    show_watched = Column(Integer)
    show_collection = Column(Float)
    show_stime = Column(DateTime)
    show_etime = Column(DateTime)
    show_date = Column(DateTime)

class Venue_Shows(db.Model):
    __tablename__='venue_shows'
    show_id = Column(Integer, ForeignKey('show.show_id'), primary_key=True, nullable=False)
    venue_id = Column(Integer, ForeignKey('venue.venue_id'), primary_key=True, nullable=False)
    no_seats = Column(Integer)

class Ticket(db.Model):
    __tablename__='ticket'
    ticket_id = Column(Integer(), primary_key=True, autoincrement=True)
    venue_name = Column(Integer(), nullable=False)
    show_name = Column(Integer(), nullable=False)
    no_seats = Column(Integer(), nullable=False)
    show_stime = Column(DateTime)
    show_etime = Column(DateTime)
    show_date = Column(DateTime)
    book_time = Column(DateTime)
    amount_paid = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

# All models have been created, let's move to other part.

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class TopThree(db.Model):
    __tablename__ = 'topthree'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String, nullable=False)

class Image_Collection(db.Model):
    __tablename__ = 'image_collection'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String, nullable=False)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(UnicodeText)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    profile_img = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    mobile = Column(String(10))
    tickets = relationship('Ticket', backref='user', lazy=True)
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    