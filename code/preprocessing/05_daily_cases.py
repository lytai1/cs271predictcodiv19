from datetime import timedelta
import datetime
import pandas as pd


path = "../../raw_data/COVID-19-master/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/"

start = datetime.date(2020,1,22)
end = datetime.date(2020,2,4)

def get_daily_cases(start, end , filename):
    day_count = (end - start).days +1
    totaldf = pd.DataFrame()

    for single_date in (start + timedelta(n) for n in range(day_count)):
        date = single_date.strftime("%m-%d-%Y")
        filepath = path + date + ".csv"
        df = pd.read_csv(filepath)
        df.pop('Last Update')
        df.pop("Deaths")
        df.pop("Recovered")
        # df.pop("Province/State")
        df.rename(columns={'Confirmed': str(single_date), "Province/State":"City", "Country/Region" : "Country"}, inplace=True)
        # df = df.groupby(["Country/Region"]).sum()
        df.set_index(["Country", "City"], inplace=True)
        if(single_date == start):
            totaldf = df
        else:
            totaldf = pd.concat([totaldf, df], axis=1)
    totaldf['mean'] = totaldf.mean(numeric_only=True, axis=1)
    totaldf['max'] = totaldf.max(numeric_only=True, axis=1)
    totaldf['outbreak'] = totaldf['max'].apply(lambda x: True if x>10 else False)

    totaldf.to_csv('../../processed_data/'+ filename + '.csv')

def main():
    start = datetime.date(2020,1,22)
    end = datetime.date(2020,2,4)

    # get_daily_cases(start, end, "05_daily_cases")
    
    start = datetime.date(2020,2,5)
    end = datetime.date(2020,2,19)

    # get_daily_cases(start, end, "05_daily_cases2")

    #compare outbreak of the two weeks
    df1 = pd.read_csv("../../processed_data/05_daily_cases.csv", index_col=[0,1])
    df2 = pd.read_csv("../../processed_data/05_daily_cases2.csv", index_col=[0,1])
    print(df1[df1['outbreak']])
    print(df2[df2['outbreak']])

    #write country to csv
    country = pd.DataFrame(df1.index.get_level_values(0).drop_duplicates())
    country.rename(columns={0: "Country"}, inplace=True)
    country['daily cases'] = True
    country.set_index(keys='Country', inplace=True)
    print(country)

    countrycsv = pd.read_csv("../../processed_data/00_Country.csv")
    countrycsv.pop('Unnamed: 0')
    countrycsv.set_index(keys='Country', inplace=True)

    print(countrycsv)
    countrycsv = pd.concat([countrycsv, country], axis=1)
    countrycsv.sort_index(inplace=True)
    countrycsv.reset_index(inplace=True)
    countrycsv.rename(columns={'index': "Country"}, inplace=True)
    print(countrycsv)
    # countrycsv.to_csv("../../processed_data/00_Country.csv")

main()