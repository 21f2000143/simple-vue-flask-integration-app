from flask import render_template, request, jsonify
from flask import current_app as app
from application.database import db
from .models import *
from datetime import datetime
import numbers
from flask_security import login_required, current_user, roles_required

     
# User dashboard
@app.route('/user/dashboard', methods=['POST','GET'])
@login_required
@roles_required('user')
def user_dashboard():
    if request.method=='POST':
        wor=request.form['words']
        wor=wor.split(',')
        words=[x.strip() for x in wor]
        # five parameters for searching in user dashboard!
        venue_name=Venue.query.with_entities(Venue.venue_name).all()
        vname=[tup[0].upper() for tup in venue_name]
        venue_place=Venue.query.with_entities(Venue.venue_place).all()
        vplace=[tup[0].upper() for tup in venue_place]
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
                    primarykeys=[tup[0] for tup in primarykey]
                elif word.upper() in vplace:
                    primarykey=Venue.query.filter(Venue.venue_place.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                    primarykeys=[tup[0] for tup in primarykey]
                elif word.upper() in sname:
                    primarykey=Show.query.filter(Show.show_name.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in primarykeys:
                                primarykeys.append(vs.venue_id)
                elif isinstance(word, numbers.Number):
                    if float(word) in srating:
                        primarykey=Show.query.filter_by(show_likes=float(word)).with_entities(Show.show_id).all()
                        primarykey1=[tup[0] for tup in primarykey]
                        venue_shows=Venue_Shows.query.all()
                        for vs in venue_shows:
                            if vs.show_id in primarykey1:
                                if vs.venue_id not in primarykeys:
                                    primarykeys.append(vs.venue_id)
                    else:
                        pass
                elif word.upper() in stag:
                    primarykey=Show.query.filter(Show.show_tag.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in primarykeys:
                                primarykeys.append(vs.venue_id)
                else:
                    pass
            else:
                midprimarykey=[]
                if word in vname:
                    primarykey=Venue.query.filter(Venue.venue_name.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                    midprimarykey=[tup[0] for tup in primarykey]
                elif word in vplace:
                    primarykey=Venue.query.filter(Venue.venue_place.ilike('%'+word+'%')).with_entities(Venue.venue_id).all()
                    midprimarykey=[tup[0] for tup in primarykey]
                elif word in sname:
                    primarykey=Show.query.filter(Show.show_name.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in primarykeys:
                                primarykeys.append(vs.venue_id)
                elif word in srating:
                    primarykey=Show.query.filter_by(show_likes=float(word)).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in midprimarykey:
                                midprimarykey.append(vs.venue_id)
                elif word in stag:
                    primarykey=Show.query.filter(Show.show_tag.ilike('%'+word+'%')).with_entities(Show.show_id).all()
                    primarykey1=[tup[0] for tup in primarykey]
                    venue_shows=Venue_Shows.query.all()
                    for vs in venue_shows:
                        if vs.show_id in primarykey1:
                            if vs.venue_id not in midprimarykey:
                                midprimarykey.append(vs.venue_id)
                else:
                    pass
                if midprimarykey!=[]:
                    set1=set(primarykeys)
                    set2=set(midprimarykey)
                    primarykeys=list(set1.intersection(set2))
        venues = []
        for pkey in primarykeys:
            venues.append(Venue.query.filter_by(venue_id=pkey).first())
        email = current_user.email
        i=email.index("@")
        email=email[:i]
        
        return render_template('user.html', venues=venues, user=email, current_user=current_user)
    elif request.method=='GET':
        venues = Venue.query.all()
        email = current_user.email
        i=email.index("@")
        email=email[:i]
        data=dict()
        data["user_id"]=current_user.email
        return render_template('vueuser.html', data=data)

@app.route('/user/user_booking/<string:user_id>', methods=['POST','GET'])
@login_required
@roles_required('user')
def user_booking(user_id):
    user=User.query.filter_by(email=user_id).first()
    item=[]
    for ticket in user.tickets:
        data=dict()
        data["venue_name"]= ticket.venue_name
        data["show_name"]= ticket.show_name
        data["book_time"]= ticket.book_time.strftime("%H:%m")
        data["amount_paid"]= ticket.amount_paid
        item.append(data)
    return jsonify(item)

@app.route('/user/book/<int:show_id>/<int:venue_id>', methods=['POST','GET'])
@login_required
@roles_required('user')
def user_book(show_id, venue_id):
    email=current_user.email
    venue=Venue.query.filter_by(venue_id=venue_id).first()
    show=Show.query.filter_by(show_id=show_id).first()
    seat=Venue_Shows.query.filter_by(venue_id=venue.venue_id, show_id=show.show_id).first()
    data=dict()
    data["show_name"]=show.show_name
    data["img_name"]=show.img_name
    data["show_tag"]=show.show_tag
    data["show_stime"]=show.show_stime.strftime("%H:%m")
    data["show_etime"]=show.show_etime.strftime("%H:%m")
    data["no_seats"]=seat.no_seats
    data["price_factor"]=venue.price_factor
    data["show_likes"]=show.show_likes
    data["show_price"]=int(show.show_price + show.show_price * venue.price_factor)
    i=email.index("@")
    email=email[:i]
    return jsonify(data)

@app.route('/ts/rate/<int:show_id>', methods=['POST','GET'])
@login_required
@roles_required('user')
def rate_show(show_id):
    if request.method=='GET':
        show = Show.query.filter_by(show_id=show_id).first()
        return render_template('rate.html', show=show)
    if request.method=='POST':
        rate=request.form['rate']
        if int(rate)>=0 and int(rate)<=5:
            show = Show.query.filter_by(show_id=show_id).first()
            show.show_likes=float(rate)
            db.session.commit()
            admin_login_status='success_rate'
            return render_template('adminpage.html', admin_login_status=admin_login_status)
        else:
            admin_login_status='rate_incorrect'
            return render_template('adminpage.html', admin_login_status=admin_login_status, show_id=show_id)


@app.route('/ts/show/booking/<int:show_id>/<int:venue_id>', methods=['POST', 'GET'])
@login_required
@roles_required('user')
def show_book(show_id, venue_id):
    show=Show.query.filter_by(show_id=show_id).first()
    venue=Venue.query.filter_by(venue_id=venue_id).first()
    seat=Venue_Shows.query.filter_by(show_id=show_id, venue_id=venue_id).first()
    data=request.get_json()
    if seat.no_seats>=int(data["no_seats"]):
        seat.no_seats=seat.no_seats - int(data["no_seats"])
        ticket=Ticket(show_name=show.show_name, venue_name=venue.venue_name, no_seats=int(data["no_seats"]), show_stime=show.show_stime, show_etime=show.show_etime , show_date=show.show_date, book_time=datetime.now(), amount_paid=float(data["amountpaid"]))
        current_user.tickets.append(ticket)
        if not venue.venue_revenue:
            venue.venue_revenue=float(data["amountpaid"])
            venue.venue_visitors=int(data["no_seats"])
        else:
            venue.venue_revenue+=float(data["amountpaid"])
            venue.venue_visitors+=int(data["no_seats"])
            
        
        if not show.show_collection:
            show.show_collection=float(data["amountpaid"])
            show.show_watched=int(data["no_seats"])
        else:
            show.show_collection+=float(data["amountpaid"])
            show.show_watched+=int(data["no_seats"])
            
        db.session.commit()
        return {"message": "Booked successfully"}
    else:
        return {"message": "error occured"}

#User account create
@app.route('/user/create', methods=['POST','GET'])
@login_required
@roles_required('user')
def user_create():
    if request.method=='GET':
        return render_template('create.html')
    elif request.method=='POST':
        email=request.form['Email']
        name=request.form['Name']
        mobile=request.form['mobile']
        password=request.form['password']
        cpassword=request.form['cpassword']
        if email and name and mobile and password:
            if "@" in email:  
                if (name.replace(' ','')).isalpha():
                    if mobile.isdigit():
                        if password==cpassword:
                            user = User(email=email, user_name=name, user_mobile=mobile, user_pass=password)
                            db.session.add(user)
                            db.session.commit()
                            admin_login_status='user_create_success'
                            return render_template('adminpage.html', admin_login_status=admin_login_status, userid=current_user.email)
                        else:
                            admin_login_status='user_pass_mis'
                            return render_template('adminpage.html', admin_login_status=admin_login_status)
                    else:
                        admin_login_status='invalid_user_mobile'
                        return render_template('adminpage.html', admin_login_status=admin_login_status)
                else:
                    admin_login_status='invalid_user_name'
                    return render_template('adminpage.html', admin_login_status=admin_login_status)
            else:
                admin_login_status='invalid_email_user_create'
                return render_template('adminpage.html', admin_login_status=admin_login_status)
        else:
            admin_login_status='empty_user_create'
            return render_template('adminpage.html')

@app.route('/user/theatre/<int:vid>')
@login_required
@roles_required('user')
def utheatre_view(vid):
    venue = Venue.query.filter_by(venue_id=vid).first()
    data=dict()
    data["venue_id"]=venue.venue_id
    data["venue_name"]=venue.venue_name
    data["venue_place"]=venue.venue_place
    data["venue_location"]=venue.venue_location
    data["venue_capacity"]=venue.venue_capacity
    data["price_factor"]=venue.price_factor
    return jsonify(data)

@app.route('/user/info')
@login_required
@roles_required('user')
def user_info():
    data=dict()
    data["email"]=current_user.email
    data["username"]=current_user.username
    return jsonify(data)
# ******* User's routers end here ******