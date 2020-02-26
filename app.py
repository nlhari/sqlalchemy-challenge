import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#Reference: https://github.com/pallets/flask/issues/974
app.config["JSON_SORT_KEYS"] = False
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"- Enter date in YYYY-MM-DD format, e.g. /api/v1.0/2016-02-23.  Data is available between 2010-01-01 and 2017-08-23<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"- Enter date in YYYY-MM-DD format, e.g. /api/v1.0/2016-02-23/2016-07-18.  Data is available between 2010-01-01 and 2017-08-23<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    # step 1: get the last date of the measurement data by listing them in descending order and reading the date on first row.
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #note the result is a list and reading the first index is the date in string format

    last_date = dt.datetime.strptime(lastdate[0], '%Y-%m-%d')

    # Calculate the date 1 year ago from the last data point in the database
    # step 3: using timedelta function find the query start date (subtract 365 days from the last date of measurement)
    query_date = dt.date(last_date.year, last_date.month, last_date.day) - dt.timedelta(days=365)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    precipitation = []
    for row in results:
        pcpt_dict = {}
        pcpt_dict["date"] = row.date
        pcpt_dict["prcp"] = row.prcp
        precipitation.append(pcpt_dict)

    return jsonify(precipitation)
    session.close()


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    stations = []
    for row in results:
        station_dict = {}
        station_dict["station"] = row.station
        station_dict["name"] = row.name
        station_dict["latitude"] = row.latitude
        station_dict["longitude"] = row.longitude
        station_dict["elevation"] = row.elevation
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    # step 1: get the last date of the measurement data by listing them in descending order and reading the date on first row.
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #note the result is a list and reading the first index is the date in string format

    last_date = dt.datetime.strptime(lastdate[0], '%Y-%m-%d')

    # Calculate the date 1 year ago from the last data point in the database
    # step 3: using timedelta function find the query start date (subtract 365 days from the last date of measurement)
    query_date = dt.date(last_date.year, last_date.month, last_date.day) - dt.timedelta(days=365)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).all()

    all_tobs = []
    for row in results:
        tobs_dict = {}
        tobs_dict["date"] = row.date
        tobs_dict["tobs"] = row.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)
    session.close()

@app.route("/api/v1.0/<start>")
def temp_start(start=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    all_tobs = []
    for Tmin, Tmax, Tavg in results:
        tobs_dict = {}
        tobs_dict["start date"] = start
        tobs_dict["end date"] = "2017-08-23"
        tobs_dict["Min Temp"] = Tmin
        tobs_dict["Max Temp"] = Tmax
        tobs_dict["Avg Temp"] = Tavg
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    all_tobs = []
    for Tmin, Tmax, Tavg in results:
        tobs_dict = {}
        tobs_dict["start date"] = start
        tobs_dict["end date"] = end
        tobs_dict["Min Temp"] = Tmin
        tobs_dict["Max Temp"] = Tmax
        tobs_dict["Avg Temp"] = Tavg
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)
    session.close()

if __name__ == '__main__':
    app.run(debug=True)
