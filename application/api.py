from flask_restful import Resource, fields, marshal_with, reqparse, marshal, output_json
from application.database import db
from flask_security import login_required, current_user, roles_required, auth_required
from .models import *
from .validation import *
from sqlalchemy import desc
import requests
from datetime import datetime
import numbers

# marshaling for venue
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

class searchApi(Resource):
    def get(self, search_words):
        try:
            wor=search_words.split(',')
            words=[x.strip() for x in wor]
            # five parameters for searching in user dashboard!
            venue_name=Venue.query.with_entities(Venue.venue_name).all()
            vname=[tup[0].upper() for tup in venue_name]
            venue_place=Venue.query.with_entities(Venue.venue_place).all()
            vplace=[tup[0].upper() for tup in venue_place]
            venue_location=Venue.query.with_entities(Venue.venue_location).all()
            vlocation=[tup[0].upper() for tup in venue_location]
            show_name=Show.query.with_entities(Show.show_name).all()
            sname=[tup[0].upper() for tup in show_name]
            show_likes=Show.query.with_entities(Show.show_likes).all()
            srating=[tup[0] for tup in show_likes]
            show_tag=Show.query.with_entities(Show.show_tag).all()
            stag=[tup[0].upper() for tup in show_tag]

            primarykeys=[]
            for word in words:
                if primarykeys==[]:
                    if word.upper() in vname:
                        primarykey=Venue.query.filter(Venue.venue_name.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                        if len(primarykey)>len(primarykeys):
                            primarykeys=[tup[0] for tup in primarykey]
                    if word.upper() in vplace:
                        primarykey=Venue.query.filter(Venue.venue_place.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                        if len(primarykey)>len(primarykeys):
                            primarykeys=[tup[0] for tup in primarykey]
                    if word.upper() in vlocation:
                        primarykey=Venue.query.filter(Venue.venue_location.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                        if len(primarykey)>len(primarykeys):
                            primarykeys=[tup[0] for tup in primarykey]
                    if word.upper() in sname:
                        primarykey=Show.query.filter(Show.show_name.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                        primarykey1=[tup[0] for tup in primarykey]
                        venue_shows=Venue_Shows.query.all()
                        for vs in venue_shows:
                            if vs.show_id in primarykey1:
                                if vs.venue_id not in primarykeys:
                                    primarykeys.append(vs.venue_id)
                    if isinstance(word, numbers.Number):
                        if float(word) in srating:
                            primarykey=Show.query.filter_by(show_likes=int(word)).with_entities(Show.show_id).all()
                            primarykey1=[tup[0] for tup in primarykey]
                            venue_shows=Venue_Shows.query.all()
                            for vs in venue_shows:
                                if vs.show_id in primarykey1:
                                    if vs.venue_id not in primarykeys:
                                        primarykeys.append(vs.venue_id)
                        else:
                            pass
                    if word.upper() in stag:
                        primarykey=Show.query.filter(Show.show_tag.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                        primarykey1=[tup[0] for tup in primarykey]
                        venue_shows=Venue_Shows.query.all()
                        for vs in venue_shows:
                            if vs.show_id in primarykey1:
                                if vs.venue_id not in primarykeys:
                                    primarykeys.append(vs.venue_id)
                else:
                    midprimarykey=[]
                    if word in vname:
                        primarykey=Venue.query.filter(Venue.venue_name.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                        if len(midprimarykey)<len(primarykey):
                            midprimarykey=[tup[0] for tup in primarykey]
                    if word in vplace:
                        primarykey=Venue.query.filter(Venue.venue_place.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                        if len(midprimarykey)<len(primarykey):
                            midprimarykey=[tup[0] for tup in primarykey]
                    if word in sname:
                        primarykey=Show.query.filter(Show.show_name.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                        primarykey1=[tup[0] for tup in primarykey]
                        venue_shows=Venue_Shows.query.all()
                        for vs in venue_shows:
                            if vs.show_id in primarykey1:
                                if vs.venue_id not in primarykeys:
                                    primarykeys.append(vs.venue_id)
                    if word in srating:
                        primarykey=Show.query.filter_by(show_likes=int(word)).with_entities(Show.show_id).all()
                        primarykey1=[tup[0] for tup in primarykey]
                        venue_shows=Venue_Shows.query.all()
                        for vs in venue_shows:
                            if vs.show_id in primarykey1:
                                if vs.venue_id not in midprimarykey:
                                    midprimarykey.append(vs.venue_id)
                    if word in stag:
                        primarykey=Show.query.filter(Show.show_tag.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                        primarykey1=[tup[0] for tup in primarykey]
                        venue_shows=Venue_Shows.query.all()
                        for vs in venue_shows:
                            if vs.show_id in primarykey1:
                                if vs.venue_id not in midprimarykey:
                                    midprimarykey.append(vs.venue_id)

                    if midprimarykey!=[]:
                        set1=set(primarykeys)
                        set2=set(midprimarykey)
                        primarykeys=list(set1.intersection(set2))
            venues = []
            for pkey in primarykeys:
                venues.append(Venue.query.filter_by(venue_id=pkey).first())
            if venues:
                datalist=[]
                i=1
                for venue in venues:
                    data={}
                    data["seq_no"]=i
                    data["venue_id"]=venue.venue_id
                    data["venue_name"]=venue.venue_name
                    data["venue_location"]=venue.venue_location
                    j=len(venues)+1
                    data['shows']=[]
                    for show in venue.shows:
                        data1={}
                        data1['seq_no']=j
                        data1["img_name"]=show.img_name
                        data1["show_id"]=show.show_id
                        data1["show_stime"]=show.show_stime.strftime("%H:%m")
                        data1["show_etime"]=show.show_etime.strftime("%H:%m")
                        data1["no_seats"]=(Venue_Shows.query.filter_by(venue_id=venue.venue_id, show_id=show.show_id).first()).no_seats
                        data['shows'].append(data1)
                        j+=1
                    datalist.append(data)
                return datalist
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e))
        
class specificvenueApi(Resource):
    def get(self, venue_location):
        try:
            venues=Venue.query.all()
            if venues:
                datalist=[]
                i=1
                for venue in venues:
                    if venue.venue_location==venue_location:
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
        
# class venueApi(Resource):
#     # @auth_required('token')
#     def get(self):
#         try:
#             start=perf_counter_ns()
#             venues=get_value()
#             stop= perf_counter_ns()
#             print("time taken", stop-start)
#             if venues:
#                 datalist=[]
#                 i=1
#                 for venue in venues:
#                     data={}
#                     data["seq_no"]=i
#                     i=i+1
#                     data["venue_id"]=venue.venue_id
#                     data["venue_name"]=venue.venue_name
#                     data["venue_location"]=venue.venue_location
#                     data['shows']=[]
#                     for show in venue.shows:
#                         data1={}
#                         data1['seq_no']=i
#                         i=i+1
#                         data1["img_name"]=show.img_name
#                         data1["show_id"]=show.show_id
#                         data1["show_stime"]=show.show_stime.strftime("%H:%m")
#                         data1["show_etime"]=show.show_etime.strftime("%H:%m")
#                         data1["no_seats"]=(Venue_Shows.query.filter_by(venue_id=venue.venue_id, show_id=show.show_id).first()).no_seats
#                         data['shows'].append(data1)
#                     datalist.append(data)
#                 return datalist
#             else:
#                 raise NotFoundError(status_code=400)
#         except requests.exceptions.RequestException as e:
#             raise NetworkError(status_code=405, message="Error: {}".format(e))
        
#     @marshal_with(venue) 
#     def put(self, venue_id):
#         venue = Venue.query.filter_by(venue_id=int(venue_id)).first()
#         if venue:
#             args=venue_parser.parse_args()
#             if "venue_name" in args:
#                 venue.venue_name = args["venue_name"]
#             if "venue_place" in args:
#                 venue.venue_place = args["venue_place"]
#             if "venue_capacity" in args:
#                 venue.venue_capacity = args["venue_capacity"]
#             if "venue_location" in args:
#                 venue.venue_location = args["venue_location"]
#             if "price_factor" in args:
#                 venue.price_factor = args["price_factor"]
#             db.session.commit()
#             return venue
#         else:
#             raise NotFoundError(status_code=404)
        
#     def delete(self, venue_id):
#         venue = Venue.query.filter_by(venue_id=venue_id).first()
#         if venue is None:
#             raise NotFoundError(status_code=400)            
#         else:
#             try:
#                 for show in venue.shows:
#                     seat=Venue_Shows.query.filter_by(venue_id=venue_id, show_id=show.show_id).first()
#                     db.session.delete(seat)
#                     db.session.commit()
#                     db.session.delete(show)
#                     db.session.commit()
#                 db.session.delete(venue)
#                 db.session.commit()
#                 return output_json(data={"message":"successfully deleted"}, code=200)
#             except requests.exceptions.RequestException as e:
#                 db.session.rollback()
#                 raise NetworkError(status_code=405, message="Error: {}".format(e))
            
#     @marshal_with(venue)
#     def post(self):
#         args=venue_parser.parse_args()
#         venue_name=args.get("venue_name", None)
#         venue_place=args.get("venue_place", None)
#         venue_capacity=args.get("venue_capacity", None)
#         venue_location=args.get("venue_location", None)
#         price_factor=args.get("price_factor", None)
#         if price_factor is None:
#             price_factor=0
#         if venue_name is None:
#             raise NotFoundError(status_code=400)
#         elif venue_place is None:
#             raise NotFoundError(status_code=400)
#         elif venue_capacity is None:
#             raise NotFoundError(status_code=400)
#         elif venue_location is None:
#             raise NotFoundError(status_code=400)
#         else:
#             try:
#                 venue=Venue(venue_name=venue_name, venue_place=venue_place, venue_capacity=venue_capacity, venue_location=venue_location, price_factor=price_factor)
#                 db.session.add(venue)
#                 db.session.commit()
#                 return venue
#             except requests.exceptions.RequestException as e:
#                 db.session.rollback()
#                 raise NetworkError(status_code=405, message="Error: {}".format(e))    

shows= {
    "show_id": fields.Integer,
    "venue_id": fields.Integer,
    "show_name":fields.String,
    "show_name":fields.String,
    "show_likes":fields.Integer,
    "show_tag": fields.String,
    "show_price": fields.Float,
    "show_stime":fields.String,
    "show_etime":fields.String
}

show_parser = reqparse.RequestParser()
show_parser.add_argument("show_name", type=str)
show_parser.add_argument("show_likes", type=int)
show_parser.add_argument("selecte_venue", type=int)
show_parser.add_argument("show_tag", type=str)
show_parser.add_argument("img_name", type=str)
show_parser.add_argument("show_price", type=float)
show_parser.add_argument("show_stime", type=str)
show_parser.add_argument("show_etime", type=str)
show_parser.add_argument("show_date", type=str)

class specificshowApi(Resource):
    def get(self, show_id):
        try:
            show=Show.query.filter_by(show_id=show_id).first()
            if show:
                resposeData={}
                resposeData["show_id"]=show.show_id
                resposeData["show_name"]=show.show_name
                resposeData["img_name"]=show.img_name
                resposeData["show_likes"]=show.show_likes
                resposeData["show_tag"]=show.show_tag
                resposeData["show_price"]=show.show_price
                resposeData["show_stime"]=show.show_stime.strftime("%H:%m")
                resposeData["show_etime"]=show.show_etime.strftime("%H:%m")
                resposeData["show_date"]=show.show_date.strftime("%Y-%m-%d")
                resposeData["venueList"]=[venue.venue_id for venue in show.venues]
                return resposeData
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
class showApi(Resource):
    @marshal_with(shows)
    def get(self):
        try:
            shows1=Show.query.all()
            if shows1:
                marsha_show=[marshal(sh, shows) for sh in shows1]
                return marsha_show
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
    @marshal_with(shows)
    def put(self, show_id):
        args=show_parser.parse_args()
        show_name=args.get("show_name", None)
        show_likes=args.get("show_likes", None)
        show_tag=args.get("show_tag", None)
        show_price=args.get("show_price", None)
        show_stime=args.get("show_stime", None)
        show_etime=args.get("show_etime", None)
        show_date=args.get("show_date", None)
        if show_id is None:
            raise NotFoundError(status_code=400)
        elif show_name is None:
            NotFoundError(status_code=400)
        elif show_tag is None:
            NotFoundError(status_code=400)
        elif show_price is None:
            NotFoundError(status_code=400)
        elif show_stime is None:
            NotFoundError(status_code=400)
        elif show_etime is None:
            NotFoundError(status_code=400)
        else:
            try:
                date_format="%H:%M"
                date_format1="%Y-%m-%d"
                show=Show.query.filter_by(show_id=show_id).first()
                show.show_name=show_name
                show.show_likes=show_likes
                show.show_tag=show_tag
                show.show_price=show_price
                show.show_stime=datetime.strptime(show_stime, date_format)
                show.show_etime=datetime.strptime(show_etime, date_format)
                show.show_date=datetime.strptime(show_date, date_format1)
                db.session.commit()
                return show
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))
            
    def delete(self, show_id):
        show=Show.query.filter_by(show_id=show_id).first()
        if show_id is None:
            raise NotFoundError(status_code=400)            
        else:
            seats=Venue_Shows.query.filter_by(show_id=show.show_id).all()
            if len(seats)>0:
                try:
                    for seat in seats:
                        db.session.delete(seat)
                        db.session.commit()
                    db.session.delete(show)
                    db.session.commit()
                    return output_json(data={"message":"successfully deleted"}, code=200)
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    @marshal_with(shows)
    def post(self):
        args=show_parser.parse_args()
        show_name=args.get("show_name", None)
        show_likes=args.get("show_likes", "Not rated")
        show_tag=args.get("show_tag", None)
        img_name=args.get("img_name", None)
        show_price=args.get("show_price", None)
        show_stime=args.get("show_stime", None)
        show_etime=args.get("show_etime", None)
        show_date=args.get("show_date", None)
        selecte_venue=args.get("selecte_venue", None)
        if show_name is None:
            raise NotFoundError(status_code=400)
        elif show_tag is None:
            raise NotFoundError(status_code=400)
        elif show_price is None:
            raise NotFoundError(status_code=400)
        elif img_name is None:
            raise NotFoundError(status_code=400)
        elif show_stime is None:
            raise NotFoundError(status_code=400)
        elif show_etime is None:
            raise NotFoundError(status_code=400)
        else:
            try:
                date_format="%H:%M"
                date_format1="%Y-%m-%d"
                sstime=datetime.strptime(show_stime, date_format)
                setime=datetime.strptime(show_etime, date_format)
                show_date=datetime.strptime(show_date, date_format1)
                venue=Venue.query.filter_by(venue_id=selecte_venue).first()
                show=Show(show_name=show_name, show_tag=show_tag, show_price=show_price, img_name=img_name, show_stime=sstime, show_etime=setime, show_likes=show_likes, show_date=show_date)
                db.session.add(show)
                db.session.commit()
                seat=Venue_Shows(venue_id=selecte_venue, show_id=show.show_id, no_seats=venue.venue_capacity)
                db.session.add(seat)
                db.session.commit()
                return show
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))

ticket={
    "ticket_id":fields.Integer
}
user_output={
    "id": fields.String,
    "username":fields.String,
    "mobile":fields.String,
    "password":fields.String,
    "tickets":fields.List(fields.Nested(ticket))
}

user_update_parse=reqparse.RequestParser()
user_update_parse.add_argument("username", type=str)
user_update_parse.add_argument("mobile", type=str)
user_update_parse.add_argument("password", type=str)

user_create_parse=reqparse.RequestParser()
user_create_parse.add_argument("id", type=str)
user_create_parse.add_argument("username", type=str)
user_create_parse.add_argument("mobile", type=str)
user_create_parse.add_argument("password", type=str)
# cannot update tickets in the user!!
class userApi(Resource):
    @marshal_with(user_output)
    def get(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                return user
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e) )
    @marshal_with(user_output)   
    def put(self, id):
        args=user_update_parse.parse_args()
        username=args.get("username")
        mobile=args.get("mobile")
        password=args.get("password")
        if id is None:
            raise NotFoundError(status_code=400)
        elif username is None:
            raise NotFoundError(status_code=400)
        elif mobile is None:
            raise NotFoundError(status_code=400)
        elif password is None:
            raise NotFoundError(status_code=400)
        else:
            id=User.query.with_entities(User.id).all()
            ids=[i[0] for i in id]
            if id in ids:
                try:
                    user=User.query.filter_by(id=id).first()
                    user.username=username
                    user.mobile=mobile
                    user.password=password
                    db.session.commit()
                    return user
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    def delete(self, id):
        if id is None:
            raise NotFoundError(status_code=400)
        else:
            id=User.query.with_entities(User.id).all()
            ids=[i[0] for i in id]
            if id in ids:
                try:
                    user=User.query.filter_by(id=id).first()
                    db.session.delete(user)
                    db.session.commit()
                    return output_json(data={"message":"successfully deleted"}, code=200)
                except requests.exceptions.RequestException as e:
                    db.session.rollback()
                    raise NetworkError(status_code=405, message="Error: {}".format(e))
            else:
                raise NotFoundError(status_code=404)
    @marshal_with(user_output)
    def post(self):
        args=user_create_parse.parse_args()
        id=args.get("id")
        username=args.get("username")
        mobile=args.get("mobile")
        password=args.get("password")
        if username is None:
            raise NotFoundError(status_code=400)
        elif mobile is None:
            raise NotFoundError(status_code=400)
        elif password is None:
            raise NotFoundError(status_code=400)
        else:
            try:
                user = User(id=id, username=username, mobile=mobile, password=password)
                db.session.add(user)
                db.session.commit()
                return user
            except requests.exceptions.RequestException as e:
                db.session.rollback()
                raise NetworkError(status_code=405, message="Error: {}".format(e))
class topthreeapi(Resource):
    # @auth_required('token')
    def get(self):
        try:
            topthrees=TopThree.query.all()
            if topthrees:
                data={}
                for i in range(len(topthrees)):
                    data["image" + str(i+1)]=topthrees[i].image
                return data
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e))
                   
class topgenresapi(Resource):
    # @auth_required('token')
    def get(self):
        try:
            topgenres= Show.query.order_by(desc(Show.show_watched)).limit(4).all()
            if topgenres:
                data={}
                for i in range(len(topgenres)):
                    data["image" + str(i+1)]=topgenres[i].img_name
                return data
            else:
                raise NotFoundError(status_code=400)
        except requests.exceptions.RequestException as e:
            raise NetworkError(status_code=405, message="Error: {}".format(e))           


# class ticketApi(Resource):
#     @marshal_with(ticket_output)
#     def get(self):
#         try:
#             tickets=Ticket.query.all()
#             if tickets:
#                 marshal_ticket=[marshal(t, ticket_output) for t in tickets]
#                 return marshal_ticket
#             else:
#                 raise NotFoundError(status_code=400)
#         except requests.exceptions.RequestException as e:
#             raise NetworkError(status_code=405, message="Error: {}".format(e) )
#     @marshal_with(ticket_output)
#     def get(self, ticket_id):
#         try:
#             if ticket_id:
#                 return Ticket.query.filter_by(ticket_id=ticket_id).first()
#             else:
#                 raise NotFoundError(status_code=400)
#         except requests.exceptions.RequestException as e:
#             raise NetworkError(status_code=405, message="Error: {}".format(e) )
