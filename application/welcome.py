from flask import render_template, redirect, url_for, request, jsonify
from flask import current_app as app
from flask_security import current_user, login_required
from application.database import db
from .models import *
import numbers
from datetime import datetime
import csv



# User dashboard
@app.route('/')
def welcome():
    return render_template('vuewelcome.html')

@app.route('/theatre/<int:vid>', methods=['POST', 'GET'])
def theatre_view(vid):
    venue = Venue.query.filter_by(venue_id=vid).first()
    data=dict()
    data["venue_id"]=venue.venue_id
    data["venue_name"]=venue.venue_name
    data["venue_place"]=venue.venue_place
    data["venue_location"]=venue.venue_location
    data["venue_capacity"]=venue.venue_capacity
    data["price_factor"]=venue.price_factor
    return jsonify(data)

@app.route('/redirecting', methods=['GET', 'POST'])
@login_required
def redirecting():
    if current_user.has_role('admin'):
        return redirect(url_for('admin_dashboard'))
    elif current_user.has_role('user'):
        user=User.query.filter_by(id=current_user.id).first()
        user.last_login_at=datetime.now()
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    else:
        role = Role.query.filter_by(name='user').first()
        app.security.datastore.add_role_to_user(user=current_user, role=role)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    

#------------------------------celery tasks endpoints----------------------------#

# @app.route('/hello/time', methods=['POST', 'GET'])
# def print_current_time_job():
#     print("IN flask app")
#     now = datetime.now()
#     print("now =", now)
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     job = tasks.print_current_time_job.apply_async(countdown=10)
#     result=job.wait()
#     return str(result), 200

# @app.route('/show_updates', methods=['GET'])
# def show_updates():
#     return render_template('show_updates.html', error=None)

# @app.route('/email_sending', methods=['GET'])
# def email_sending():
#     job = tasks.send_daily_reminder.delay()
#     result=job.wait()
#     return str(result), 200

# @app.route('/show_updates_vue', methods=['GET'])
# def show_updates_vue():
#     return render_template('show_updates_vue.html', error=None)

# @app.route('/test_send_message', methods=['GET'])
# def test_send_message():
#     sse.publish({"message": "hello!"}, type='greeting')
#     return "Message sent to browsers, please check!"

# @app.route("/start_long_running_job", methods=["GET","POST"])
# def start_long_running_job():
#     job_id = tasks.long_running_job.delay()
#     sse.publish({"message": "STARTING JOB "+ str(job_id)}, type='greeting')
#     return "STARTED!"+str(job_id)
# @app.route('/test/vue')
# def vuetest():
#     return render_template('alertmessage.html')