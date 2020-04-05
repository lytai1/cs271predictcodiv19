import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_country_list(region):
    http_url = "https://energyplus.net/weather-region/" + region[1]
    retrieved_data = requests.get(http_url).text

    soup = BeautifulSoup(retrieved_data, "lxml")
    #print(soup.text)
    collected_data = soup.text.split('Select a country.')[1].lstrip().split('Learn more about Weather Data Sources.')[0]
    collected_data = collected_data.rstrip('-')
    print(collected_data)
    lst = collected_data.split('-')
    lst = [s.strip() for s in lst]
    lst = [s[:-3] + ', ' + s[-3:] for s in lst ]
    lst = [s.strip() for s in lst]

    #del lst[0]
    #lst = [s.strip().split(',') for s in lst]

    print(lst)


def weather_station_process(country):
    print(country)
    regions = {'Africa':'africa_wmo_region_1', 'Asia': 'asia_wmo_region_2',
               'South America': 'south_america_wmo_region_3', \
                'North and Central America': 'north_and_central_america_wmo_region_4', \
                 'Southwest Pacific': 'southwest_pacific_wmo_region_5', 'Europe': 'europe_wmo_region_6'}
    my_region = regions[country[0]]
    http_url = "https://energyplus.net/weather-region/" + my_region +"/" + country[2] + "%20%20"
    retrieved_data = requests.get(http_url).text

    soup = BeautifulSoup(retrieved_data, "lxml")
    #print(soup.text)
    collected_data = soup.text.split('Select a location.')[1].lstrip().split('Learn more about Weather Data Sources')[0]
    #cities_data = collected_data
    collected_data = re.sub("[\(\[].*?[\)\]]", ",", collected_data)
    collected_data = collected_data.rstrip(',')
    collected_data.replace('-', ' ')
    #print(collected_data)

    lst = collected_data.split(',')
    #print(len(lst))
    #lst = list(chunks(lst, 2))
    
    lst = [s.strip().split(' ') for s in lst]
    lst = [[' '.join(s[:-1]), s[-1]] for s in lst]
    #print(lst)
    df = pd.DataFrame(lst, columns=['Location',  'StationID'])
    col_region = []
    col_rep = []
    col_country = []
    for i in range(len(df)):
        col_region.append(country[0])
        col_country.append(country[1])
        col_rep.append(country[2])
    df.insert(0, "Rep", col_rep, True)
    df.insert(0, "Country", col_country, True)
    df.insert(0, "Region", col_region, True)
    #print(type(df))
    #print(df)


    return df


def main():
    #regions = [['Africa', 'africa_wmo_region_1'], ['Asia', 'asia_wmo_region_2'], ['South America', 'south_america_wmo_region_3'], \
    #           ['North and Central America', 'north_and_central_america_wmo_region_4'], \
    #           ['Southwest Pacific', 'southwest_pacific_wmo_region_5'], ['Europe', 'europe_wmo_region_6]]

    #regions = [['Europe', 'europe_wmo_region_6']]
    #for region in regions:
     #   get_country_list(region)
    #countries = [['China', 'CHN']]

    with open('04_Region_Country.csv', newline='') as f:
        reader = csv.reader(f)
        countries = list(reader)
    countries.remove(countries[0])

    #countries = countries[56:]      # test
    #countries = [['Asia', 'ARE', 'United Arab Emirates']] # test

    countries =[]         # pause append to weather_station.csv
    # TODO:
    # Canada station and CS


    for country in countries:
        country = [c.strip() for c in country]
        #print(country)
        df = weather_station_process(country)

        if not os.path.isfile('04_Weather_Station.csv'):
            df.to_csv('04_Weather_Station.csv', index=False, header=True)
        else:
            df.to_csv('04_Weather_Station.csv', mode='a', index=False, header=False)


if __name__ == "__main__":
    main()
