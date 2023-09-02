import pickle
from datetime import datetime
import requests
import pandas as pd
import traceback
import config
import pymysql
import json
import functools
from sqlalchemy import create_engine
from flask_mail import Mail, Message
from flask import Flask, g, render_template, jsonify, request
from flask_cors import CORS


app = Flask("dublin bikes", static_url_path="/static")
app.config.from_object("config")
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
# mainpage


@app.route("/")
def main():
    return render_template("index_home.html")

# about page with team members detail


@app.route("/about")
def about():
    return render_template("about.html")

# page with all the main functions


@app.route("/services")
def services():
    return render_template("services.html")

# email page


@app.route("/contact")
def contact():
    return render_template("contact.html")


# function to connect to database with bikes data
def connect_to_database():
    conn = pymysql.connect(
        host=config.URL,
        port=config.PORT,
        user=config.USER,
        password=config.PASSWORD,
        db=config.DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# function to connect to database with weather data


def connect_to_weather_database():
    conn = pymysql.connect(
        host=config.WEATHER_URL,
        port=config.WEATHER_PORT,
        user=config.WEATHER_USER,
        password=config.WEATHER_PASSWORD,
        db=config.WEATHER_DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# define a global object to store bikes data


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = connect_to_database()
    return db

# define a global object to store weather data


def get_weather_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = connect_to_weather_database()
    return db

# closing the database connection when finished


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# api to retrieve station data from database


@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    conn = get_db()
    stations = []

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT station.number,name,address,position_lat,position_lng,status,bike_stands,available_bikes_stands,available_bikes,MAX(last_update) as last_update from availability join station WHERE station.number = availability.number GROUP BY availability.number;")
            rows = cursor.fetchall()
            for row in rows:
                stations.append(dict(row))
        return jsonify(stations=stations)
    except:
        print(traceback.format_exc())
        return "error in get_stations", 404

# api to retrieve availability data to do machine learning


@app.route("/availability")
def availability():
    conn = get_db()
    availability = []

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * from availability_data;")
            rows = cursor.fetchall()
            for row in rows:
                availability.append(dict(row))
        return jsonify(availability=availability)
    except:
        print(traceback.format_exc())
        return "error in availability", 404

# api to retrieve weather data from database


@app.route("/weather")
def weather():
    conn = get_db()
    weather = []

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * from weather_data;")
            rows = cursor.fetchall()
            for row in rows:
                weather.append(dict(row))
        return jsonify(weather=weather)
    except:
        print(traceback.format_exc())
        return "error in weather", 404


@app.route("/history7/<int:station_id>")
def get_history_7(station_id):
    engine = get_db()
    df = pd.read_sql_query(
        "select * from availability where number = %(number)s and last_update between '2023-03-27' and '2023-04-03'",
        engine, params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)
    res_7 = df['available_bikes'].resample('1d').mean()
    return jsonify(data_24=json.dumps(list(zip(map(lambda x: x.isoformat(), res_7.index), res_7.values))))

# api to retrieve data for selected station to show 24hrs chart


@app.route("/history24/<int:station_id>")
def get_history_24(station_id):
    engine = get_db()
    df = pd.read_sql_query(
        "select * from availability where number = %(number)s and last_update like '2023-04-06%%'", engine,
        params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)
    res_24 = df['available_bikes'].resample('60min').mean()
    print(res_24)
    return jsonify(data_24=json.dumps(list(zip(map(lambda x: x.isoformat(), res_24.index), res_24.values))))


# de-serialize machine learning model files into an object called model using pickle
with open('models.pkl', 'rb') as handle:
    models = pickle.load(handle)
with open('models2.pkl', 'rb') as handle:
    models2 = pickle.load(handle)

# receive input from user and use models above to do prediction


@app.route("/predict", methods=['POST'])
def predict():
    time = request.form['hour']
    days = request.form['day']
    month = request.form['month']
    selectedStart = request.form['selectedStart']
    selectedDest = request.form['selectedDest']

    # get weatherforecast data for the day user entered
    response = requests.get('http://127.0.0.1:5000/weatherforecast')
    try:
        data = json.loads(response.text)
        # print(data)
    except json.JSONDecodeError:
        print("Invalid JSON format")

    for forecast in data["list"]:
        if int(datetime.fromtimestamp(forecast["dt"]).day) == int(days):
            temp = forecast["temp"]["day"]
            print(temp)
            wind_speed = forecast["speed"]
            humidity = forecast["humidity"]

    # prediction for available bikes at starting point
    for model in models:
        if selectedStart in model:
            predictedStart = models[selectedStart].predict(
                [[int(time), temp, wind_speed, humidity]])

    # prediction for available bikes stands at destination point
    for model in models2:
        if selectedDest in model:
            predictedDest = models2[selectedDest].predict(
                [[int(time), temp, wind_speed, humidity]])

    start = json.dumps(predictedStart.tolist())
    dest = json.dumps(predictedDest.tolist())
    return jsonify(start, dest, days, month)

# api to get weather forecast data from openweatherapi


@app.route("/weatherforecast")
def weatherforecast():
    weather = requests.get(
        'WEATHER_API')
    return jsonify(weather.json())


# email submission
# Configure Flask Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'comp30830db@gmail.com'
# app.config['MAIL_PASSWORD'] = 'yincazvkpsjopnzi'
# mail = Mail(app)


@app.route('/submit_contact_form', methods=['POST'])
def submit_form():
    # name = request.form['name']
    # email = request.form['email']
    # message = request.form['message']

    # # Create and send the email
    # msg = Message('New form submission', sender=email,
    #               recipients=['your-email@example.com'])
    # msg.body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
    # mail.send(msg)

    return 'Thank you for your message!'


if __name__ == "__main__":
    app.run(debug=True)
