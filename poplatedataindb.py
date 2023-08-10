from main import *
import csv
f=open('venue.csv', 'r')
csvreader = csv.reader(f)
header = next(csvreader)
from datetime import datetime,timedelta
for i in range(1,10):
    row=next(csvreader)
    ven=Venue(venue_name=row[1],venue_place=row[2], venue_capacity=row[3],venue_location=row[4], price_factor=row[5])
    db.session.add(ven)
    db.session.commit()
    f1=open('show.csv', 'r')
    csvreader1 = csv.reader(f1)
    header = next(csvreader1)
    for j in range(1,10):
        row1=next(csvreader1)
        sho=Show(show_name=row1[1],img_name="comedy-shows-collection.avif",show_likes=5,show_tag=row1[4], show_price=300.0, show_stime=datetime.now(), show_etime=datetime.now()+timedelta(hours=2), show_date=datetime.now())
        db.session.add(sho)
        db.session.commit()
        ven_sho=Venue_Shows(venue_id=ven.venue_id, show_id=sho.show_id, no_seats=ven.venue_capacity)
        db.session.add(ven_sho)
        db.session.commit()
    f1.close()
f.close()