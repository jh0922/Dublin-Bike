import json
import config
from sqlalchemy import create_engine
import datetime
import traceback
import requests


def station_to_db(engine, text):
    stations = json.loads(text)
    for station in stations:
        vals = station.get("number"), station.get("name"), station.get("address"), station.get("position").get("lat"), station.get(
            "position").get("lng"), station.get("bike_stands"), int(station.get("banking")), int(station.get("bonus"))
        engine.execute(
            "insert into station values(%s,%s,%s,%s,%s,%s,%s,%s)", vals)
    return


def main():
    if True:
        b_engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.format(
            config.b_USER, config.b_PASSWORD, config.b_URL, config.b_PORT, config.b_DB), echo=True)

        sql_1 = """
        CREATE DATABASE IF NOT EXISTS b_dbikes
        """

        sql_2 = """
        CREATE TABLE IF NOT EXISTS station (
        number INTEGER,
        name VARCHAR(256),
        address VARCHAR(256),
        position_lat REAL,
        position_lng REAL,
        bike_stands INTEGER,
        banking INTEGER,
        bonus INTEGER,
        PRIMARY KEY (number)
        )
        """

        try:
            res = b_engine.execute(sql_1)
            res = b_engine.execute("DROP TABLE IF EXISTS station")
            res = b_engine.execute(sql_2)
            print(res.fetchall())
        except Exception as e:
            print(e, traceback.format_exc())

        sql = """
        CREATE TABLE IF NOT EXISTS availability(
        number INTEGER,
        status VARCHAR(256),
        available_bikes_stands INTEGER,
        available_bikes INTEGER,
        last_update DATETIME,
        PRIMARY KEY (number, last_update),
        FOREIGN KEY (number) REFERENCES station(number)
        )
        """
        try:
            res = b_engine.execute("DROP TABLE IF EXISTS availability")
            res = b_engine.execute(sql)
            print(res.fetchall())
        except Exception as e:
            print(e, traceback.format_exc())

        r = requests.get(config.STATIONS_URL,
                         params={"apiKey": config.JCKEY,
                                 "contract": config.NAME})
        station_to_db(b_engine, r.text)


if __name__ == "__main__":
    main()
