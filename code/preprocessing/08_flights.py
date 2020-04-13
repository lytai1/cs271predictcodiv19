import requests
import pandas as pd
import json
from datetime import timedelta
import datetime


# get airport info
api = "https://api.flightstats.com/flex/airports/rest/v1/json/active?appId="
appID = "ce8ac023"
appKey = "bbc12d4c908a7c257bf778d7ef46b890"

callAdr = api + appID + "&appKey=" + appKey

resp = requests.get(callAdr)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
airportApi = resp.json()
# print(airportApi)
airports = json.dumps(airportApi["airports"])

# save in pd dataframe and export as CSV
df = pd.read_json(airports)
print(df)

df.to_csv(("../../processed_data/08_airports.csv"))

# print to csv file
df = pd.read_csv("../../processed_data/08_airports.csv")
df = df[['countryName', 'city','name','fs',  'iata', 'icao', 'faa']]
print(df)
df.to_csv(("../../processed_data/08_airports_full.csv"))

# remove airports without iata or icao code
# df = pd.read_csv("../../processed_data/08_airports.csv")
# df.dropna(subset=['iata', 'icao'], inplace=True)
# df = df[df['name'].str.contains("International")]

# df.set_index("countryName", inplace=True)
# print(df)
# df.to_csv(("../../processed_data/08_airports.csv"))

#pull data from api to get flight detail
# start = datetime.date(2020,1,25)
# end = datetime.date(2020,2,4)
# day_count = (end - start).days +1

# for single_date in (start + timedelta(n) for n in range(day_count)):
#     date = single_date.strftime("%Y/%m/%d")
#     print(date)
#     df = pd.DataFrame()
#     country = pd.read_csv("../../processed_data/08_airports.csv")
#     airport_code = country['iata']
#     for a in airport_code:
#         print(a)
#         departure = []

#         for hour in range(0, 24, 6):
#             apicall = "https://api.flightstats.com/flex/flightstatus/historical/rest/v3/json/airport/status/"
#             apicall += a
#             apicall += "/arr/"
#             apicall += date
#             apicall += "/" + str(hour) + "?appId="
#             apicall += appID
#             apicall += "&appKey="
#             apicall += appKey +"&utc=false&numHours=6"


#             resp = requests.get(apicall)
#             if resp.status_code != 200:
#                 # This means something went wrong.
#                 raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#             airportApi = resp.json()
#             flights = airportApi['flightStatuses']
#             for f in flights:
#                 departure.append(f["departureAirportFsCode"])
#                 # print(f["departureAirportFsCode"])
#         if len(departure) > 0:
#             print(a)
#             df1 = pd.DataFrame({a: departure})
#             df = pd.concat([df,df1], axis=1)

#     print(df)
#     df.to_csv("../../processed_data/08_flights_from_" +single_date.strftime("%Y%m%d")+ ".csv")


