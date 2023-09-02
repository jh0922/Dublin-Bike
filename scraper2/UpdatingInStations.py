import Project_Info
import json
import sqlalchemy as sqla
import traceback
import requests
import time
import datetime

# Here is applying to mysql + pymysql
engine = sqla.create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(Project_Info.RDS_USERNAME,
                                            Project_Info.RDS_PASSWORD,
                                            Project_Info.RDS_URL,
                                            Project_Info.RDS_PORT,
                                            Project_Info.RDS_SCHEMA), echo=True)

# The following is to scrape stations datum into database


def static_stations_to_db(stationstext):
    stationsInfo = json.loads(stationstext)
    for station in stationsInfo:
        # print(type(station), len(station))
        # print(station)
        vals = (
            int(station.get('number')),
            station.get('address'),
            int(station.get('banking')),
            station.get('bike_stands'),
            station.get('name'),
            station.get('position').get('lat'),
            station.get('position').get('lng'))
        # engine.execute("INSERT INTO stations_static_datum(number, address, banking, bike_stands, name, position_lat, position_lng"
        # ") VALUES (%s,%s,%s,%s,%s,%s,%s)", vals)
        engine.execute("UPDATE stations_static_datum SET address=%s, banking = %s, bike_stands = %s, name = %s, position_lat = %s, "
                       "position_lng = %s WHERE number = %s", vals)
    return None

# update availability information into database


def dynamic_stations_to_db(stationstext):
    dynamicStations = json.loads(stationstext)
    # print(type(dynamicStations), len(dynamicStations))
    for d in dynamicStations:
        # print(a)
        vals = (
            int(d.get('number')),
            d.get('last_update'),
            int(d.get('available_bikes')),
            int(d.get('available_bike_stands')),
            d.get('status'))
        # The following is to update the stations datum
        # engine.execute("INSERT INTO stations_dynamic_datum(number, last_update, available_bikes, available_bike_stands, status"
        # ") VALUES (%s,%s,%s,%s,%s)", vals)
        engine.execute("UPDATE stations_dynamic_datum SET last_update = %s, available_bikes = %s, available_bike_stands = %s, "
                       "status = %s WHERE number = %s", vals)
        # insert values in RDS
        # vals = (
        #     int(d.get('number'))
        #     d.get('last_update'),
        #     int(d.get('available_bikes')),
        #     int(d.get('available_bike_stands')),
        #     d.get('status'))
        # engine.execute("INSERT INTO stations_dynamic_datum(number, last_update, available_bikes, available_bike_stands, status"
        #         ") VALUES (%s,%s,%s,%s,%s)", vals)
    return None


def updatingStationsDatum():
    while True:
        try:
            # now = datetime.datetime.now()
            stations = requests.get(Project_Info.STATIONS_URL, params={
                                    "apiKey": Project_Info.JCKEY, "contract": Project_Info.NAME})
            # print(stations, now)
            # write_to_file(stations.text)
            static_stations_to_db(stations.text)
            dynamic_stations_to_db(stations.text)
            # print(a)
            time.sleep(5 * 60)  # update per 2 minutes
        except:
            print(traceback.format_exc())
            if engine is None:
                return None


# Execute the method for scraper of weather datum
# updatingStationsDatum()

#stations = requests.get(Project_Info.STATIONS_URL, params={"apiKey": Project_Info.JCKEY, "contract": Project_Info.NAME})
# static_stations_to_db(stations.text)
# dynamic_stations_to_db(stations.text)
