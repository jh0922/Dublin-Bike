
import Project_Info
import json
import sqlalchemy as sqla
import traceback
import requests
import datetime

# The following is for database building
engine = sqla.create_engine(
    "mysql+mysqldb://{}:{}@{}:{}/{}".format(Project_Info.RDS_USERNAME, Project_Info.RDS_PASSWORD, Project_Info.RDS_URL, Project_Info.RDS_PORT,
                                            Project_Info.RDS_SCHEMA), echo=True)


def updating_weather_to_db(weathertext):
    weatherInfo = json.loads(weathertext)
    current_time = datetime.datetime.now()

    vals = (
        current_time,
        float(weatherInfo.get('coord').get('lon')),
        float(weatherInfo.get('coord').get('lat')),
        float(weatherInfo.get('main').get('temp')),
        float(weatherInfo.get('main').get('feels_like')),
        float(weatherInfo.get('main').get('humidity')),
        float(weatherInfo.get('wind').get('speed')))

    engine.execute(
        "INSERT INTO history_weather_datum(time, longitude, latitude, temp, temp_feels_like,  humidity, wind_speed"
        ") VALUES (%s,%s,%s,%s,%s,%s,%s)", vals)
    return None


def updatingWeatherDatum():
    if True:
        try:
            weather = requests.get(Project_Info.WEATHER_URL, params={
                                   "q": Project_Info.WEATHER_CITY, "appid": Project_Info.WEATHER_KEY})

            updating_weather_to_db(weather.text)

            time.sleep(5 * 60)  # The datum will be updated per 5 minutes
        except:
            print(traceback.format_exc())
            if engine is None:
                return None


# Execute the method for scraper of weather datum
# updatingWeatherDatum()
