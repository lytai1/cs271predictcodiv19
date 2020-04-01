import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os


def weather_process(location, month):

    http_url = "https://en.tutiempo.net/climate/" + month + "/ws-" + location[1] +".html"
    retreived_data = requests.get(http_url).text

    soup = BeautifulSoup(retreived_data, "lxml")

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
    row_location = []
    row_date = []
    for i in range(len(df)):
        row_location.append(location[0])
        row_date.append("{0:0=2d}".format(i + 1) + '-' + month)
    df.insert(0, "Date", row_date, True)
    df.insert(0, "Location", row_location, True)

    return df


def main():
    ## use small size of locations and months to test.
    ## To avoid scraping too many data the website at one time, devide locations set into multiple sets
    ## Sleep for a while after processing each set
    
    #locations = [['Wuhan, China', "574940"]]  # test
    #months = ['01-2020']                      # test
    locations = [['Wuhan, China', "574940"], ['Beijing, China', '545110']]  ## TO DO: get more location and ID
    months = ['01-2020', '02-2020']
    for location in locations:
        for month in months:
            df = weather_process(location, month)
            if not os.path.isfile('../../processed_data/04_Weather.csv'):
                df.to_csv('../../processed_data/04_Weather.csv', index=False, header=True)
            else:
                df.to_csv('../../processed_data/04_Weather.csv', mode='a', index=False, header=False)


if __name__== "__main__":
    main()
