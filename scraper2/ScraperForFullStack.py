import Project_Info
import sqlalchemy as sqla
import pandas as pd
from datetime import datetime
import json

# stationDic = {
#     'number': 0,
#     'address': "address",
#     'banking': "banking",
#     'bikeStands': 0,
#     'name': "name",
#     'positionLat': 0,
#     'positionLng': 0,
#     'lastUpdate': 0,
#     'availableBikes': 0,
#     'availableBikeStands': 0,
#     'status': 0
# }

def stationsDatum():
    # The following snippet is to create database engine
    engine = sqla.create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}".format(Project_Info.RDS_USERNAME,
                                                Project_Info.RDS_PASSWORD,
                                                Project_Info.RDS_URL,
                                                Project_Info.RDS_PORT,
                                                Project_Info.RDS_SCHEMA), echo=True)
    df = pd.read_sql_table("Dublin_Bikes_Stations", engine)

    # SQL to select station
    sql = """
        select * from
        (select available_bikes, available_bike_stands, status, last_update, number
        from availability
        group by number) a1
        JOIN
        (select number, name,address, bike_stands, banking, position_lat,position_lng from Dublin_Bikes_Stations) a2
        on a1.number = a2.number;
        """

    # get the results
    results = engine.execute(sql)

    # To store each result in the Dublin Bikes Stations
    # this one are stored in a list
    dublinBikesStations = []
    for row in results:
        dublinBikesStationsDic = {}
        dublinBikesStationsDic['number'] = row.number
        dublinBikesStationsDic['address'] = row.address
        dublinBikesStationsDic['banking'] = row.banking
        dublinBikesStationsDic['bikeStands'] = row.bike_stands
        dublinBikesStationsDic['name'] = row.name
        dublinBikesStationsDic['positionLat'] = row.position_lat
        dublinBikesStationsDic['positionLng'] = row.position_lng
        # convert timestamp to datetime
        datumUpdated = datetime.fromtimestamp(float(row.last_update) / 1000)
        dublinBikesStationsDic['lastUpdate'] = str(datumUpdated)
        dublinBikesStationsDic['availableBikes'] = row.available_bikes
        dublinBikesStationsDic['availableBikeStands'] = row.available_bike_stands
        dublinBikesStationsDic['status'] = row.status
        # print(stationDic)
        dublinBikesStations.append(dublinBikesStationsDic)
        # print(stations)
        # stationData = json.dumps(stations)
        # print(stations)

    return dublinBikesStations

print(stationsDatum())