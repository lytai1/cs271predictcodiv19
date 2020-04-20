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
    
    # weather = pd.read_csv("../../processed_data/04_Weather_fixed.csv", index_col=0)
    # weather.set_index(keys='Country', inplace=True)
    # weather = weather[["Date","T","SLP","H","PP","VV","V","VM","VG","RA","SN","TS"]]
    # weather = weather[weather["Date"] == "01-01-2020"]
    # weather = weather.groupby(weather.index).mean()
    # print(weather)

    daily_cases = pd.read_csv("../../processed_data/05_daily_cases.csv", index_col=0)
    daily_cases = daily_cases[["mean", "max"]]
    daily_cases.fillna(0, inplace=True)
    grouped = daily_cases.groupby(daily_cases.index).mean()
    df["daily cases mean"] = grouped["mean"]
    grouped = daily_cases.groupby(daily_cases.index).max()
    df["daily cases max"] = grouped["max"]
    df.fillna(0, inplace=True)

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

    print(df)

    df.to_csv("../../processed_data/ZZ_final_processed_data.csv")
    

main()