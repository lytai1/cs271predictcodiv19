from datetime import timedelta
import datetime
import pandas as pd


path = "../../raw_data/COVID-19-master/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/"

start = datetime.date(2020,1,22)
end = datetime.date(2020,2,4)



def main():
    day_count = (end - start).days +1
    totaldf = pd.DataFrame()

    for single_date in (start + timedelta(n) for n in range(day_count)):
        date = single_date.strftime("%m-%d-%Y")
        filepath = path + date + ".csv"
        df = pd.read_csv(filepath)
        df.pop('Last Update')
        df.pop("Deaths")
        df.pop("Recovered")
        df.pop("Province/State")
        df.rename(columns={'Confirmed': str(single_date)}, inplace=True)
        df = df.groupby(["Country/Region"]).sum()
        if(single_date == start):
            totaldf = df
        else:
            totaldf = pd.concat([totaldf, df], axis=1)
    totaldf['mean'] = totaldf.mean(numeric_only=True, axis=1)
    totaldf['max'] = totaldf.max(numeric_only=True, axis=1)
    totaldf['outbreak'] = totaldf['max'].apply(lambda x: True if x>10 else False)

    totaldf.to_csv('../../processed_data/05_daily_cases.csv')
    
    #write country to csv
    country = pd.DataFrame(totaldf.index)
    country.rename(columns={0: "Country"}, inplace=True)
    country['daily cases'] = True
    country.set_index(keys='Country', inplace=True)
    print(country)

    countrycsv = pd.read_csv("../../processed_data/00_Country.csv")
    countrycsv.pop('Unnamed: 0')
    countrycsv.set_index(keys='Country', inplace=True)

    print(countrycsv)
    countrycsv = pd.concat([countrycsv, country], axis=1)
    countrycsv.reset_index(inplace=True)
    countrycsv.rename(columns={'index': "Country"}, inplace=True)
    print(countrycsv)
    countrycsv.to_csv("../../processed_data/00_Country.csv")


main()