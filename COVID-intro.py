"""
Researching COVID

To get data from cmd line use following:

git clone https://github.com/CSSEGISandData/COVID-19
"""

import pandas as pd
import glob

path = '/Users/jasonrubenstein/Desktop/Python/covid/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/*.csv'
covid_files = glob.glob(path)


def get_csvs(files):
    datas = pd.concat([
                         pd.read_csv(datas,
                                     dtype=str,
                                     error_bad_lines=False,
                                     delimiter=',')
        for datas in files], axis=0)
    df = datas.drop_duplicates(keep='first').reset_index(drop=True)
    return df


covid_data = get_csvs(covid_files)
covid_data = covid_data[covid_data['Last_Update'].notna()]
covid_data = covid_data.sort_values(by="Last_Update")
covid_data = covid_data.fillna(0)


# Adjust dtype as necessary
def to_ints(df):
    df['Confirmed'] = df['Confirmed'].astype("int")
    df['Deaths'] = df['Deaths'].astype("int")
    df['People_Tested'] = df['People_Tested'].astype("int")
    df['People_Hospitalized'] = df['People_Hospitalized'].astype("int")
    return df


def shift_data(df):
    df['Prev_Cases'] = df.groupby("Province_State")["Confirmed"].shift(1)
    df['Prev_Deaths'] = df.groupby("Province_State")["Deaths"].shift(1)
    df['Prev_Tests'] = df.groupby("Province_State")["People_Tested"].shift(1)
    df['Prev_Hospitalizations'] = df.groupby("Province_State")["People_Hospitalized"].shift(1)
    df = df.fillna(0)
    return df


def daily_data(df):
    df['Daily_Cases'] = df['Confirmed'] - df['Prev_Cases']
    df['Daily_Deaths'] = df['Deaths'] - df['Prev_Deaths']
    df['Daily_Tests'] = df['People_Tested'] - df['Prev_Tests']
    df['Daily_Hospitalizations'] = df['People_Hospitalized'] - df['Prev_Hospitalizations']
    del df['Prev_Hospitalizations'], df['Prev_Deaths'], df['Prev_Cases'], df['Prev_Tests']
    df = df[(df['Last_Update'] > "2020-04-13")]
    return df

