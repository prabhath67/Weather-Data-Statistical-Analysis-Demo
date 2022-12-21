# Code for ingestion.

import os
import sqlite3
import logging
from datetime import datetime

import pandas as pd

conn = sqlite3.connect('wx_yld_data.db')


def avg_max_temp(wx_dir):
    """
    params: Avg max temp for each region for every year will be stored in table with suffix _avg_max_temp
    """
    try:
        for table_name in os.listdir(wx_dir):
            if table_name.endswith(".txt"):
                df = pd.read_sql('SELECT date,temp_max FROM ' + table_name, conn,
                                 parse_dates={"date": {"format": "%y%m%d"}})
                max_temp_df = df.groupby(lambda x: df['date'][x].year)["temp_max"].max()
                max_temp_df = max_temp_df.drop_duplicates()
                max_temp_df.to_sql(table_name + '_avg_max_temp', con=conn, index=False, if_exists='replace')
                logging.info(f'loaded avg max temp stats to  {table_name}_avg_max_temp')
    except Exception as e:
        raise e


def avg_min_temp(wx_dir):
    """
    params: Avg min temp for each region for every year will be stored in table with suffix _avg_min_temp
    """
    try:
        for table_name in os.listdir(wx_dir):
            if table_name.endswith(".txt"):
                df = pd.read_sql('SELECT date,temp_min FROM ' + table_name, conn,
                                 parse_dates={"date": {"format": "%y%m%d"}})
                min_temp_df = df.groupby(lambda x: df['date'][x].year)["temp_min"].min()
                min_temp_df = min_temp_df.drop_duplicates()
                min_temp_df.to_sql(table_name + '_avg_min_temp', con=conn, index=False, if_exists='replace')
                logging.info(f'loaded avg min temp stats to  {table_name}_avg_min_temp')
    except Exception as e:
        raise e


def total_accum_prec(wx_dir):
    """
    params: precipitation_amount for each region for every year will be stored in table with suffix _precipitation_amount
    """
    try:
        for table_name in os.listdir(wx_dir):
            if table_name.endswith(".txt"):
                df = pd.read_sql('SELECT date,precipitation_amount FROM ' + table_name, conn,
                                 parse_dates={"date": {"format": "%y%m%d"}})
                prec_df = df.groupby(lambda x: df['date'][x].year)["precipitation_amount"].sum()
                prec_df = prec_df.drop_duplicates()
                prec_df.to_sql(table_name + '_precipitation_amount', con=conn, index=False, if_exists='replace')
                logging.info(f'loaded prec total stats to  {table_name}_precipitation_amount')
    except Exception as e:
        raise e


def get_weather_on_date(date, station_id):
    date_string = date.strftime("%y%m%d")
    df = pd.read_sql('SELECT * FROM ' + station_id + ' where date = ' + date_string, conn)
    return df.to_json()


def get_yield_on_date(date):
    date_string = date.strftime("%y%m%d")
    df = pd.read_sql('SELECT * FROM yld_data where date = ' + date_string, conn)
    return df.to_json()


def get_weather_stats(station_id):
    df = pd.read_sql('SELECT * FROM ' + station_id,conn)
    return df.to_json()


if __name__ == '__main__':
    avg_min_temp("/location_of_wx_files/")
