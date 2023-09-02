import Project_Info
import json
import sqlalchemy as sqla
import traceback
import requests
import time

# Here is applying to mysql + pymysql
engine = sqla.create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(Project_Info.RDS_USERNAME, Project_Info.RDS_PASSWORD, Project_Info.RDS_URL, Project_Info.RDS_PORT,
                                            Project_Info.RDS_SCHEMA), echo=True)


# def write_to_file(text):
#     with open("data/bike_{}".format(now).replace(" ", "_"), "w") as f:
#         f.write(r.text)

# update station data into database
# def stations_to_db(text):
#     stations = json.loads(text)
#     # print(type(stations), len(stations))
#     # print(stations)
#     for station in stations:
#         # print(station)
#         vals = (
#             station.get('address'), int(station.get('banking')),
#             station.get('bike_stands'), station.get('name'), station.get('position').get('lat'),
#             station.get('position').get('lng'), int(station.get('number')))
#         engine.execute(
#             "UPDATE station SET address=%s, banking = %s, bike_stands = %s, name = %s, position_lat = %s, "
#             "position_lng = %s WHERE number = %s",
#             vals)
#     return


# update availability info into database
def station_weather_to_db(a_stations, weather):
    availability = json.loads(a_stations)
    weather = json.loads(weather)
    for a in availability:
        # print(a)
        # vals = (
        #     a.get('last_update'), int(a.get('available_bikes')),
        #     int(a.get('available_bike_stands')), a.get('status'), int(a.get('number')))
        # # update
        # engine.execute("UPDATE availability SET last_update = %s, available_bikes = %s, available_bike_stands = %s, "
        #                "status = %s WHERE number = %s", vals)
        # insert
        vals = (
            int(a.get('number')),
            a.get('last_update'),
            int(a.get('available_bikes')),
            int(a.get('available_bike_stands')),
            weather.get('weather')[0]['main'],
            weather.get('main').get('temp'),
            weather.get('main').get('humidity'),
            weather.get('wind').get('speed'))
        engine.execute(
            "INSERT INTO history_stations_and_weather_datum(number, last_update_date, available_bikes, available_bike_stands, weather, temp, humidity, wind_speed"
            ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", vals)
    return None


def updatingHistoryDatum():
    while True:
        try:
            a_stations = requests.get(Project_Info.STATIONS_URL, params={
                                      "apiKey": Project_Info.JCKEY, "contract": Project_Info.NAME})
            weather = requests.get(Project_Info.WEATHER_URL, params={
                                   "q": Project_Info.WEATHER_CITY, "appid": Project_Info.WEATHER_KEY})

            station_weather_to_db(a_stations.text, weather.text)

            time.sleep(5 * 60)  # update per 5 minutes
        except:
            print(traceback.format_exc())
            if engine is None:
                return None


# Execute the method for scraper of weather datum
# updatingHistoryDatum()
