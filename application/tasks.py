from application.workers import celery
from datetime import datetime
from application.send import *
from application.sendGchatmessage import *
from .models import *
from .dynamic_price_factor import calculate_percentile
from flask import render_template
from flask_sse import sse
from celery.schedules import crontab
import time
import csv

def mail_offer():
    topshows=Show.query.order_by(Show.show_likes.desc()).limit(3).all()
    return render_template('offeremail.html', topshows=topshows)

def mail_report(user):
    result=list()
    if (len(user.tickets)>0):
        for ticket in  user.tickets:
            datadict=dict()
            datadict["Venue Name"]=ticket.venue_name
            datadict["Show Name"]=ticket.show_name
            datadict["no_seats"]=ticket.no_seats
            datadict["book_time"]=ticket.book_time.strftime("%H:%m")
            datadict["amount_paid"]=ticket.amount_paid
            result.append(datadict)
        return render_template('mail_format.html', result=result)
    else:
        return None


# scheduled task
@celery.task()
def daily_reminder_to_user():
    users=User.query.all()
    for user in users:
        flag=True
        for ticket in user.tickets:
            if ticket.book_time.strftime("%m/%d")==datetime.now().strftime("%m/%d"):
                flag=False
                break
        if flag:
            if 'user' in list(user.roles):
                body=mail_offer()
                send_message(service, user.email, "Ticket Show V2", 
                        body)
                sse.publish({"message": "You have not booked any ticket, please book now!", "color":"alert alert-primary" },type='notifyuser')
    gchatMessage("You have not booked any ticket, please book now!")
    return {"status": "success"}

# scheduled task
@celery.task()
def monthly_entertainment_report_to_users():
    users=User.query.all()
    error=True
    for user in users:
        body=mail_report(user)
        if body is not None:
            send_message(service, user.email, "Ticket Show V2", body)
            error=False
    if error:
        sse.publish({"message": "Sent emails fo monthly report to all users successfully", "color":"alert alert-info" }, type='notifyadmin')
    else:
        sse.publish({"message": "Sent emails fo monthly report to not all users.", "color":"alert alert-warning" }, type='notifyadmin')
    return {"status": "success"}


            
        
celery.conf.beat_schedule = {
    'my_monthly_task': {
        'task': "application.tasks.monthly_entertainment_report_to_users",
        'schedule': crontab(hour=13, minute=50, day_of_month=1, month_of_year='*/1'),  # Sending report to users on first day of each month at 6pm
    },
    'my_daily_task': {
        'task': "application.tasks.daily_reminder_to_user",
        'schedule': crontab(hour=21, minute=0),  # Sending email and notification for inactive users
    },
    'my_daily_dynamic_price_update_task': {
        'task': "application.tasks.dynamic_price_update",
        'schedule': crontab(hour=21, minute=0),  # updating price factor in venue
    },
    'my_quick_check_task': {
        'task': "application.tasks.daily_reminder_to_user",
        'schedule': crontab(minute='*/1'),  # Sending email and notification for inactive users
    },
    # Add more scheduled tasks as needed
}
# scheduled task
@celery.task()
def dynamic_price_update():
    venues=Venue.query.all()
    data={}
    for venue in venues:
        data[venue.venue_id]=0
        tickets=Ticket.query.filter_by(venue_name=venue.venue_name).all()
        total_ticket=sum([ticket.no_seats for ticket in tickets ])
        data[venue.venue_id]=total_ticket
    data_list=list(data.values())
    data_list.sort()
    for venue in venues:
        venue.price_factor = calculate_percentile(data_list, data[venue.venue_id])
        db.session.commit()
        sse.publish({"message": "price factor update successfully for venues", "color":"alert alert-success" }, type='notifyadmin')
    return {"status": "success"}


@celery.task()
def user_triggerd_async_job(v_id):
    venue=Venue.query.filter_by(venue_id=v_id).first()
    header=["Venue Name","Show Name","Show Rating","Number of bookings"] 
    f=open('venue_report.csv', 'w')
    csvwriter=csv.writer(f)
    csvwriter.writerow(header)
    for show in venue.shows:
        ticket=Ticket.query.filter_by(show_name=show.show_name).all()
        csvwriter.writerow([venue.venue_name, show.show_name, show.show_likes, len(ticket)])
    f.close()
    time.sleep(5)
    return {"status": "success"}


# def helper(venue_name="No data", show_name="No data", show_likes="No data", total=0):
#     return venue_name + ','+show_name+','+show_likes+','+str(total)+'\n'
# # user triggered task
# def on_task_success(result, task_id,task_name, args, kwargs):
#     current_time=datetime.now().strftime("%d/%m%Y %H:%M:%S")
#     sse.publish({"message": "Current time = "+current_time }, type='report')

# def on_task_failure(exc, task_id, task_name, args, kwargs, einfo):
#     print(f"Task failed. Exception: {exc}")
#     sse.publish({"message": "failure" }, type='report')

# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#   # sender.add_periodic_task(crontab(minute='*/1'), daily_reminder_to_user.s(), name='updating price factor in venue')
#   # sender.add_periodic_task(crontab(hour=13, minute=50), daily_reminder_to_user.s(), name='Sending email and notification for inactive users')
    # sender.add_periodic_task(crontab(hour=21, minute=0), daily_reminder_to_user.s(), name='Sending email and notification for inactive users')
    # sender.add_periodic_task(crontab(hour=13, minute=50, day_of_month=1, month_of_year='*/1'), monthly_entertainment_report_to_users.s(), name='Sending report to users on first day of each month at 6pm')
    # sender.add_periodic_task(crontab(hour=18, minute=0, day_of_month=1, month_of_year='*/1'), monthly_entertainment_report_to_users.s(), name='Sending report to users on first day of each month at 6pm')
    # sender.add_periodic_task(crontab(hour=18, minute=0), dynamic_price_update.s(), name='updating price factor in venue')


# @celery.task(on_success=on_task_success, on_failure=on_task_failure)
    # print("Inside the task")
    # now = datetime.now()
    # print("now =", now)
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # # test send email
    # # send_message(service, "sachinthesensitive2@gmail.com", "This is a subject", 
    # #         "This is the body of the email", ["test.txt", "photo.jpg"])
    # sse.publish({"message": "Current time ="+dt_string }, type='greeting')
    # print("date and time =", dt_string) 
    # print("COMPLETE")
    # return dt_string
# from main import gmail_service ---------there is problem with controllers, need to fix this--------
# from googleapiclient.errors import HttpError
# from email.mime.text import MIMEText
# import base64
# from celery.decorators import periodic_task

# print("crontab ", crontab)

# def create_message(email, subject, message):
#     msg = MIMEText(message)
#     msg['to'] = email
#     msg['subject'] = subject
#     return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


# def send_email(service, email, subject, message):
#     try:
#         message = create_message(email, subject, message)
#         service.users().messages().send(userId='me', body=message).execute()
#     except HttpError as error:
#         print(f"An error occurred: {error}")
# def create_message(email, subject, message):
#     message = {
#         'to': email,
#         'subject': subject,
#         'message': message
#     }
#     return message


# @celery.task
# def send_daily_reminder():
#     email = "21f2000143@ds.study.iitm.ac.in"
#     subject = "Daily Reminder"
#     message = "Don't forget your daily tasks!"
#     send_email(gmail_service, email, subject, message)
#     return "sent!"

# Schedule the daily reminder task
# from flask import current_app as app
# celery.conf.beat_schedule = {
#     'send-daily-reminder': {
#         'task': 'print_current_time_job',
#         'schedule': crontab(minute=1),  # Schedule at 8:00 AM every day
#     },
# }

# @celery.task()
# def just_say_hello(name):
#     print("INSIDE TASK")
#     print("Hello {}".format(name))
#     return name





# @celery.task()
# def calculate_aggregate_likes(article_id):
#     # You can get all the likes for the `article_id`
#     # Calculate the aggregate and store in the DB
#     print("#####################################")
#     print("Received {}".format(article_id))
#     print("#####################################")
#     return True



# @celery.task()
# def long_running_job():
#     print("STARTED LONG JOB")
#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#     sse.publish({"message": "STARTED ="+dt_string }, type='greeting')
#     for lp in range(100):
#         now = datetime.now()
#         print("now =", now)
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         sse.publish({"message": "RUNNING ="+dt_string }, type='greeting')
#         print("date and time =", dt_string) 
#         time.sleep(2)

#     now = datetime.now()
#     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")        
#     sse.publish({"message": "COMPLETE ="+dt_string }, type='greeting')
#     print("COMPLETE LONG RUN")