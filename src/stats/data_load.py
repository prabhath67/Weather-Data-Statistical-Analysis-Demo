# Code for ingestion.

import os
import sqlite3
import logging
from datetime import datetime

import pandas as pd

conn = sqlite3.connect('wx_yld_data.db')


def load_data(wx_dir, yld_dir):
    """
    params: wx_dir and yld_dir are the directory locations for weather and yield datas respectively.
    This function will load data from file to desired tables in sqlite db
    """
    start = datetime.now()
    logging.info(f'Start time : {str(start)}')
    try:
        for region_file in os.listdir(wx_dir):
            if region_file.endswith(".txt"):
                region_data_df = pd.read_csv(region_file, sep="\t", header=None)
                region_data_df = region_data_df.drop_duplicates()
                region_data_df.to_sql(region_file, con=conn, index=False, if_exists='replace')
                logging.info(f'No of records inserted for {region_file} is {region_data_df.shape[0]}')
            else:
                logging.info(f'Not a valid region file {region_file}')
                continue

        for yld_file in os.listdir(yld_dir):
            if yld_file.endswith(".txt"):
                yld_data_df = pd.read_csv(yld_file, sep="\t", header=None)
                yld_data_df = yld_data_df.drop_duplicates()
                yld_data_df.to_sql(yld_file, con=conn, index=False, if_exists='replace')
                logging.info(f'No of records inserted for {yld_file} is {yld_data_df.shape[0]}')
                break
            else:
                logging.info(f'Not a valid yield file {yld_file}')
                continue
    except Exception as e:
        raise e
    end = datetime.now()
    logging.info(f'End time : {str(end)}')
    logging.info(f'Time taken to load data is {end - start}')


if __name__ == '__main__':
    load_data("/location_of_wx_files/", "/location_of_yld_file/")
