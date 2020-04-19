import csv
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

df1 = pd.read_csv("04_Region_Country.csv")
df1["Country"].replace({"Iran": "Islamic Republic of Iran", "Viet Nam": "Vietnam", \
                       "Columbia": "Colombia", "USA": "United States", \
                       "Bosnia and Herzegowina": "Bosnia and Herzegovina", "Russian Federation": "Russia", \
                       "Slovakia (Slovak Republic)": "Slovakia", "Syrian Arab Republic": "Syria"}, inplace=True)

df2 = pd.read_csv("04_Weather_Station.csv")
df2["Country"].replace({"Iran": "Islamic Republic of Iran", "Viet Nam": "Vietnam", \
                       "Columbia": "Colombia", "USA": "United States", \
                       "Bosnia and Herzegowina": "Bosnia and Herzegovina", "Russian Federation": "Russia", \
                       "Slovakia (Slovak Republic)": "Slovakia", "Syrian Arab Republic": "Syria"}, inplace=True)

df3 = pd.read_csv("04_Weather.csv")
df3["Country"].replace({"Iran": "Islamic Republic of Iran", "Viet Nam": "Vietnam", \
                       "Columbia": "Colombia", "USA": "United States", \
                       "Bosnia and Herzegowina": "Bosnia and Herzegovina", "Russian Federation": "Russia", \
                       "Slovakia (Slovak Republic)": "Slovakia", "Syrian Arab Republic": "Syria"}, inplace=True)

df1.to_csv('04_Region_Country_fixed.csv', index=True, header=True)
df2.to_csv('04_Weather_Station_fixed.csv', index=True, header=True)
df3.to_csv('04_Weather_fixed.csv', index=True, header=True)




'''
not found
Africa,Libyan Arab Jamahiriya,LBY
Asia,Macau,MAC
Asia,Russian Federation,RUS
North and Central America,Virgin Islands (U.S.),VIR 
Southwest Pacific,United States Minor Outlying Islands,UMI 
Europe,Russian Federation,RUS
Asia,Russian Federation,RUS



to fix
Iran --- Islamic Republic of Iran
Korea?
Asia,Korea,KOR 
Asia,Korea,PRK
Viet Nam ----  Vietnam
Columbia -----   Colombia
USA ----  United States
Bosnia and Herzegowina  ----  Bosnia and Herzegovina
Russian Federation   ---- Russia
Slovakia (Slovak Republic) -----  Slovakia
Syrian Arab Republic  -- Syria



00_country to fix
Korea
Taiwan
Bosnia and Herzegovina




'''