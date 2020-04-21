import pandas as pd

def main():
    countries = pd.read_csv("../../processed_data/00_Country_training.csv", index_col=0)
    countries.set_index(keys='Country', inplace=True)
    print(countries)

    df = pd.DataFrame(countries.index)
    df.set_index(keys='Country', inplace=True)

    gpp = pd.read_csv("../../processed_data/01_GDP.csv", index_col=0)
    df["GDP"] = gpp["2020"]

    ppp = pd.read_csv("../../processed_data/02_PPP.csv", index_col=0)
    df["PPP"] = gpp["2020"]

    population = pd.read_csv("../../processed_data/03_World_Population_density.csv", index_col=0)
    df["Population"] = population["PopTotal"]
    df["Population density"] = population["PopDensity"]

    daily_cases = pd.read_csv("../../processed_data/05_daily_cases.csv", index_col=0)
    daily_cases = daily_cases[["mean", "max"]]
    daily_cases.fillna(0, inplace=True)
    grouped = daily_cases.groupby(daily_cases.index).mean()
    df["daily cases mean"] = grouped["mean"]
    grouped = daily_cases.groupby(daily_cases.index).max()
    df["daily cases max"] = grouped["max"]
    df.fillna(0, inplace=True)

    daily_cases2 = pd.read_csv("../../processed_data/05_daily_cases2.csv", index_col=0)
    daily_cases2 = daily_cases[["mean", "max"]]
    daily_cases2.fillna(0, inplace=True)
    grouped2 = daily_cases2.groupby(daily_cases2.index).mean()
    df["daily cases2 mean"] = grouped2["mean"]
    grouped2 = daily_cases2.groupby(daily_cases2.index).max()
    df["daily cases2 max"] = grouped2["max"]
    df.fillna(0, inplace=True)
    df["outbreak"] = df["daily cases2 max"].apply(lambda x: True if x>10 else False)

    df.pop("daily cases2 mean")
    df.pop("daily cases2 max")


    lat_lng = pd.read_csv("../../processed_data/06_lat_lng.csv", index_col=0)
    lat_lng = lat_lng.groupby(lat_lng.index).mean()
    df["lat"] = lat_lng["lat"]
    df["lng"] = lat_lng["lng"]

    education = pd.read_csv("../../processed_data/07_education.csv", index_col=0)
    df["education level"] = education["Gross enrolment ratio, tertiary, both sexes (%) (%)"]

    flights = pd.read_csv("../../processed_data/08_flights_no_countries.csv", index_col=0)
    flights = flights[["National flights", "international flights"]]
    flights = flights.groupby(flights.index).sum()
    df["national flights"] = flights["National flights"]
    df["international flights"] = flights["international flights"]

    weather = pd.read_csv("../../processed_data/04_Weather_fixed.csv", index_col=0)
    weather = weather[['Country', 'Location', 'Date', 'T']]
    pd.set_option('display.max_rows', None)  # display all rows
    indexNames = weather[weather['T'] == '-'].index  # Delete these row indexes from dataFrame
    weather.drop(indexNames, inplace=True)
    weather = weather.dropna()
    weather['T'] = weather['T'].astype(float)
    weather = weather.groupby('Country', as_index=False)['T'].mean()
    weather = weather.rename(columns={"T": "Mean_Weather"})
    # print("weather mean:\n", weather)
    df = pd.merge(df, weather[['Country', 'Mean_Weather']], on='Country', how='left')

    #remove all with nan data
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    df.pop("index")
    print(df)

    df.to_csv("../../processed_data/ZZ_final_processed_data.csv")
    

main()