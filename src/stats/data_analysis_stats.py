# Code for ingestion.
import json
import os
import sqlite3
import logging

import pandas as pd


conn = sqlite3.connect('wx_yld_data.db')


def avg_max_temp():
    """
    params: Avg max temp for each region for every year will be stored in table with suffix _avg_max_temp
    """
    res_code = 200
    try:
        main_dir = os.getcwd().rsplit('\\', 1)[0]
        for table_name in os.listdir(main_dir + '\\wx_data\\'):
            if table_name.endswith(".txt"):
                table_name = table_name.split('.')[0]
                df = pd.read_sql('SELECT date,temp_max FROM ' + table_name, conn,
                                 parse_dates={"date": {"format": "%Y%m%d"}})
                max_temp_df = df.groupby(lambda x: df['date'][x].year)["temp_max"].max()
                max_temp_df = max_temp_df.drop_duplicates()
                max_temp_df.to_sql(table_name + '_avg_max_temp', con=conn, if_exists='replace')
                logging.info(f'loaded avg max temp stats to  {table_name}_avg_max_temp')
    except Exception as e:
        logging.error(e)
        res_code = 400
    return {'Status': res_code}


def avg_min_temp():
    """
    params: Avg min temp for each region for every year will be stored in table with suffix _avg_min_temp
    """
    res_code = 200
    try:
        main_dir = os.getcwd().rsplit('\\', 1)[0]
        for table_name in os.listdir(main_dir + '\\wx_data\\'):
            if table_name.endswith(".txt"):
                table_name = table_name.split('.')[0]
                df = pd.read_sql('SELECT date,temp_min FROM ' + table_name, conn,
                                 parse_dates={"date": {"format": "%Y%m%d"}})
                min_temp_df = df.groupby(lambda x: df['date'][x].year)["temp_min"].min()
                min_temp_df = min_temp_df.drop_duplicates()
                min_temp_df.to_sql(table_name + '_avg_min_temp', con=conn, if_exists='replace')
                logging.info(f'loaded avg min temp stats to  {table_name}_avg_min_temp')
    except Exception as e:
        logging.error(e)
        res_code = 400
    return {'Status': res_code}


def total_accum_prec():
    """
    params: precipitation_amount for each region for every year will be stored in table with suffix _precipitation_amount
    """
    res_code = 200
    try:
        main_dir = os.getcwd().rsplit('\\', 1)[0]
        for table_name in os.listdir(main_dir + '\\wx_data\\'):
            if table_name.endswith(".txt"):
                table_name = table_name.split('.')[0]
                df = pd.read_sql('SELECT date,precipitation_amount FROM ' + table_name, conn,
                                 parse_dates={"date": {"format": "%Y%m%d"}})
                prec_df = df.groupby(lambda x: df['date'][x].year)["precipitation_amount"].sum()
                prec_df = prec_df.drop_duplicates()
                prec_df.to_sql(table_name + '_precipitation_amount', con=conn, if_exists='replace')
                logging.info(f'loaded prec total stats to  {table_name}_precipitation_amount')
    except Exception as e:
        logging.error(e)
        res_code = 400
    return {'Status': res_code}


def get_weather_on_date(date, station_id):
    date_string = date.strftime("%Y%m%d")
    df = pd.read_sql('SELECT * FROM  ' + station_id  + ' where date = '+ date_string, conn)
    return json.loads(df.drop(['index'], axis=1).to_json(orient ='records'))


def get_yield_on_date(date):
    date_string = date.strftime("%Y")
    df = pd.read_sql('SELECT * FROM US_corn_grain_yield where date = ' + date_string, conn)
    return json.loads(df.drop(['index'], axis=1).to_json(orient ='records'))


def get_weather_stats(station_id):
    df = pd.read_sql('SELECT * FROM ' + station_id,conn)
    return json.loads(df.drop(['index'], axis=1).to_json(orient ='records'))


if __name__ == '__main__':
    avg_min_temp()
