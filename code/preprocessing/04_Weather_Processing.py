import csv
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

skip = 0

def weather_process(location, month):
    global skip
    http_url = "https://en.tutiempo.net/climate/" + month + "/ws-" + location[4] +".html"
    retrieved_data = requests.get(http_url).text
    soup = BeautifulSoup(retrieved_data, "lxml")

    if 'Error 404' in soup.text:
        skip += 1
        print(skip, ' Errors found')
        return pd.DataFrame()

    hiddenData = str(soup.find_all('style')[1])
    hiddenSpan = {}
    for group in re.findall(r'span\.(.+?)}',hiddenData):
        class_attr = group.split('span.')[-1].split('::')[0]
        content = group.split('"')[1]
        hiddenSpan[class_attr] = content

    climate_table = str(soup.find("table", attrs={"class": "medias mensuales numspan"}))
    for k, v in hiddenSpan.items():
        climate_table = climate_table.replace('<span class="%s"></span>' %(k), hiddenSpan[k])

    df = pd.read_html(climate_table)[0]
    df = df.drop(df.index[[-2, -1]])
    df = df.drop('Day', axis=1)

    col_date = []
    col_region = []
    col_country = []
    col_location = []
    col_stationID = []
    for i in range(len(df)):
        col_date.append("{0:0=2d}".format(i + 1) + '-' + month)
        col_stationID.append(location[4])
        col_location.append(location[3])
        col_country.append(location[1])
        col_region.append(location[0])
    df.insert(0, "Date", col_date, True)
    df.insert(0, "StationID", col_stationID, True)
    df.insert(0, "Location", col_location, True)
    df.insert(0, "Country", col_country, True)
    df.insert(0, "Region", col_region, True)

    print(location[3], ' weather get!')
    return df


def main():
    ## use small size of locations and months to test.
    ## To avoid scraping too many data the website at one time, devide locations set into multiple sets
    ## Sleep for a while after processing each set
    
    #locations = [['Wuhan, China', "574940"]]  # test
    #months = ['01-2020']                      # test
    #locations = [['Wuhan, China', "574940"], ['Beijing, China', '545110']]  ## TO DO: get more location and ID

    df = pd.read_csv("04_Weather_Station.csv")
    locations = df.values.tolist()

    # To remove duplicated station
    """
    print(df.shape)
    df["StationID"].duplicated()

    df.drop_duplicates(subset="StationID", keep="first", inplace=True)
    print(df.shape)
    df.to_csv('04_Weather_Station.csv', index=False, header=True)

    locations = df.values.tolist()
    """
    
    locations = locations[452:]

    months = ['01-2020', '02-2020']

    for i in range(len(locations)):
        location = locations[i]
        print(location)
        time.sleep(1)
        for month in months:
            df = weather_process(location, month)
            if not os.path.isfile('04_Weather.csv'):
                df.to_csv('04_Weather.csv', index=False, header=True)
            else:
                df.to_csv('04_Weather.csv', mode='a', index=False, header=False)


if __name__== "__main__":
    main()
