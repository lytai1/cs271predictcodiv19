import pandas as pd
from datetime import timedelta
import datetime

path = "../../processed_data/08_flights_from/08_flights_from_"
start = datetime.date(2020,1,22)
end = datetime.date(2020,2,4)
day_count = (end - start).days +1

# for single_date in (start + timedelta(n) for n in range(day_count)):
#     date = single_date.strftime("%Y%m%d")
#     df = pd.read_csv(path + date + ".csv")
#     df.pop("Unnamed: 0")
#     df = df.apply(pd.Series.value_counts)
#     print(df)
#     df.to_csv("../../processed_data/08_flights_no_" +date+ ".csv")

path = "../../processed_data/08_flights_no_"
day_count = 2
df = pd.read_csv(path + "20200124" + ".csv", index_col=0)
df = pd.DataFrame(df['SFO'])
df.dropna(inplace=True)
df.drop(index="ZRH", inplace=True)
print("20200124")
print(df)

for single_date in (start + timedelta(n) for n in range(day_count)):
    date = single_date.strftime("%Y%m%d")
    df1 = pd.read_csv(path + date + ".csv", index_col=0)
    df1 = pd.DataFrame(df['SFO'])
    df1.dropna(inplace=True)
    print(date)
    print(df1)
    df += df1

print("total")
print(df)

