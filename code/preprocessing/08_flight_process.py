import pandas as pd
from datetime import timedelta
import datetime

#combine the 08_flights_from_ csv into one csv
def combine():
    path = "../../processed_data/08_flights_from/08_flights_from_"
    start = datetime.date(2020,1,22)
    end = datetime.date(2020,2,4)
    day_count = (end - start).days +1

    df1 = pd.DataFrame()

    for single_date in (start + timedelta(n) for n in range(day_count)):
        date = single_date.strftime("%Y%m%d")
        df = pd.read_csv(path + date + ".csv", index_col=0)
        print(df)

        df1 = pd.concat([df1, df], ignore_index=True, sort=True)
        print(df1)

    df1 = df1.apply(pd.Series.value_counts)
    df1.to_csv("../../processed_data/08_flights_no.csv")

def analyse():
    df = pd.read_csv("../../processed_data/08_flights_no.csv", index_col=0)

    airports = pd.read_csv("../../processed_data/08_airports.csv", index_col='iata')
    print(airports)

    # df.rename(columns=airports['countryName'].to_dict(), inplace=True)
    df['Country'] = df.index.map(airports['countryName'].to_dict())
    df.dropna(subset=['Country'], inplace=True)
    df.set_index(['Country'], inplace=True)
    df = df.groupby(level="Country").sum()
    
    df = df.T
    df['Country'] = df.index.map(airports['countryName'].to_dict())
    df['City'] = df.index.map(airports['city'].to_dict())
    df.set_index(['Country', 'City'], inplace=True)
    df.sort_index(inplace=True)

    df["National flights"] = df.apply(lambda x: (x[x.name[0]] if x.name[0] in df.columns else 0), axis=1)
    df["international flights"] = df.sum(axis=1)- 2 * df["National flights"]

    print(df)
    df.to_csv("../../processed_data/08_flights_no_countries.csv")

def match_countries():
    df = pd.read_csv("../../processed_data/08_flights_no_countries.csv", index_col=0)
    country = pd.read_csv('../../processed_data/00_Country.csv', index_col=0)
    print(country)
    df = df[df.index.isin(country["Country"])]
    print(df)

    #add country name to csv
    country = pd.DataFrame(df.index)
    country.drop_duplicates(inplace=True)
    country.set_index(keys='Country', inplace=True)
    country["flights"] = True
    print(country)
    countrycsv = pd.read_csv("../../processed_data/00_Country.csv")
    countrycsv.pop('Unnamed: 0')
    countrycsv.set_index(keys='Country', inplace=True)

    print(countrycsv)
    countrycsv = pd.concat([countrycsv, country], axis=1)
    countrycsv.reset_index(inplace=True)
    countrycsv.rename(columns={'index': "Country"}, inplace=True)
    print(countrycsv)
    countrycsv.to_csv("../../processed_data/00_Country_test.csv")


def main():
    match_countries()

main()