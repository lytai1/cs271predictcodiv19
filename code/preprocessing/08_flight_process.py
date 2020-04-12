import pandas as pd
from datetime import timedelta
import datetime

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

