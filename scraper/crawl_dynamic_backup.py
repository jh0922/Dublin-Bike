import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import json
import requests
import time
from IPython.display import display
import config
import datetime
import pandas as pd


def availability_to_db(engine, text):
    availabilities = json.loads(text)
    now = datetime.datetime.now()
    for availability in availabilities:
        vals = availability.get("number"), availability.get("status"), availability.get(
            "available_bike_stands"), availability.get("available_bikes"), now

        engine.execute("insert into availability values(%s,%s,%s,%s,%s)", vals)


def main():
    engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.format(config.b_USER,
                           config.b_PASSWORD, config.b_URL, config.b_PORT, config.b_DB), echo=True)
    r = requests.get(config.STATIONS_URL,
                     params={"apiKey": config.JCKEY,
                             "contract": config.NAME})

    try:
        availability_to_db(engine, r.text)
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
