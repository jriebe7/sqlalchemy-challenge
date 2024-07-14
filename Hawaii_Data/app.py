# Import the dependencies.

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# 1.

# Start at the homepage.

# List all the available routes.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
#2. /api/v1.0/precipitation

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    precip_results = session.query(Measurement.prcp, Measurement.date).all()

    session.close()

    precipitaton_query_values = []
    for prcp, date in precip_results:
        precipitation_dict = {}
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"] = date
        precipitaton_query_values.append(precipitation_dict)

    return jsonify(precipitaton_query_values) 

#3./api/v1.0/stations

#Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def station(): 

    session = Session(engine)

    station_results = session.query(Station.station,Station.id).all()

    session.close()

    stations_values = []
    for station, id in station_results:
        stations_values_dict = {}
        stations_values_dict['station'] = station
        stations_values_dict['id'] = id
        stations_values.append(stations_values_dict)
    return jsonify(stations_values)

#4. /api/v1.0/tobs

# Query the dates and temperature observations of the most-active station for the previous year of data.

# Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs") 
def tobs():
    
    session = Session(engine) 
    station_id = 'USC00519281'
    tob_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == station_id).\
        filter(Measurement.date > '2016-08-22').all()
    
    session.close()

    tob_values = []
    for date, tobs in tob_results:
        tob_values_dict = {}
        tob_values_dict['date'] = date
        tob_values_dict['tobs'] = tobs
        tob_values.append(tob_values_dict)
    return jsonify(tob_values)

#5. /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    start_date_tobs_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    start_date_tobs_values =[]
    for min, avg, max in start_date_tobs_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["tmin"] = min
        start_date_tobs_dict["tavg"] = avg
        start_date_tobs_dict["tmax"] = max
        start_date_tobs_values.append(start_date_tobs_dict)
    
    return jsonify(start_date_tobs_values)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    session = Session(engine)

    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()

    start_end_date_values = []
    for min, avg, max in start_end_results:
        start_end_date_dict = {}
        start_end_date_dict["tmin"] = min
        start_end_date_dict["tavg"] = avg
        start_end_date_dict["tmax"] = max
        start_end_date_values.append(start_end_date_dict) 
    return jsonify(start_end_date_values)

if __name__ == '__main__':
    app.run(debug=True)