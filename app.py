import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')

@app.route("/api/v1.0/precipitation")
# will create a dictionary with the date as the key and the precipitation as the value (jsonify!)
def precipitation():
    # add the line of code that calculates the date one year ago from the most recent date
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    #get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # get all of the stations in our database
    results = session.query(Station.station).all()
    # start by unraveling our results into a one-dimensional array
    # unravel = undo twisted
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
# tobs = temperature observations
def temp_monthly():
    # calculate the date a year ago from the last date in the database
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # finally unravel the results into one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# report on the minimum, average, and maximum temperatures
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# we need start parameter and end parameter
def stats(start=None, end=None):
    # create a query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # we need to determine the starting and ending date
    # if-not statement
    if not end:
        # * meaning = multiple results
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)