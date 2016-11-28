#!/usr/bin/python

# This script looks up tatripid and tablockid for tripid and blockid
#   input: <date>-vehicle-strip.txt
#   output: rows of vehicle locations (json objects)
#

import json
import io
import sys

from datetime import date
from gtfs import Schedule
from gtfs.entity import Base, Trip, Route, HistoricalVehicleLocation
from sqlalchemy import create_engine, distinct, func, select
from sqlalchemy.orm import sessionmaker

# config
db_filename = "pitt_1609.sqlite3"
target_date = date(2016, 11, 8)

# init
engine = create_engine("sqlite:///" + db_filename)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

sched = Schedule(db_filename)

def store_historical_vehicle_location(record):
  vehicle_location = HistoricalVehicleLocation(
                       timestamp = record[u"tmstmp"],
                       trip_id = record[u"tripid"],
                       vehicle_id = record[u"vid"],
                       vehicle_lon = record[u"lon"],
                       vehicle_lat = record[u"lat"],
                       vehicle_heading = record[u"hdg"],
                       vehicle_speed = record[u"spd"],
                       vehicle_shape_distance = record[u"pdist"]
		     ) 
  session.add(vehicle_location)
  #session.commit()


def main():
  if len(sys.argv) < 2:
    print "Error: no input file given"
    print "Usage: %s <date>-vehicle-strip.txt" % sys.argv[0]
    return

  active_services = sched.service_for_date(target_date)
  if len(active_services) == 0:
    print "No active service found on date", target_date
    return

  input_fname = sys.argv[1]
  count = 0
  cached_lookups = {}
  with open(input_fname) as data_file:
    for line in data_file:
      record = json.loads(line)

      route = record[u'rt']
      # pattern_id = record[u'pid'] # did not find a matching field in GTFS
      tatripid = record[u'tatripid']
      tablockid = record[u'tablockid']

      key = tatripid + tablockid
      if key in cached_lookups:
        trip_id, block_id = cached_lookups[key]
      else:
        q = Trip.query
        q = q.filter(Trip.service_id.in_(active_services))
        q = q.filter(Trip.trip_id.like(tatripid + "%"))  # tripid start with tatripid
        q = q.filter(Trip.block_id == tablockid)
        if q.count() == 0:
          cached_lookups[key] = ("", "")
          pass
        elif q.count() == 1:
          trip = q.first()
          trip_id = trip.trip_id
          block_id = trip.block_id
          cached_lookups[key] = (trip.trip_id, trip.block_id)
        else:
          # print "Error: multiple rows found.", route, "|", tatripid, "|", tablockid, "|", q.all()
          pass

      if trip_id != "" and block_id != "":
	record[u'tripid'] = trip_id
	record[u'blockid'] = block_id
	store_historical_vehicle_location(record)

        count += 1
        if count % 1000 == 0:
          session.commit()
          print count  # 1633544
      else:
        print "Matching Error:", record 
      


if __name__ == "__main__":
    main()
