# Code for ingestion.

import os
import sqlite3
import logging
import sys
from datetime import datetime

import pandas as pd

conn = sqlite3.connect('wx_yld_data.db')

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_data():
    """
    params: wx_dir and yld_dir are the directory locations for weather and yield datas respectively.
    This function will load data from file to desired tables in sqlite db
    """
    start = datetime.now()
    res_code = 200
    logger.info(f'Start time : {str(start)}')
    try:
        main_dir = os.getcwd().rsplit('\\', 2)[0]
        if 'unittest' in sys.modules.keys():
            main_dir = os.getcwd().rsplit('\\', 1)[0]
        region_records = 0
        for region_file in os.listdir(main_dir + '\\wx_data\\'):
            if region_file.endswith(".txt"):
                table_name = region_file.split('.')[0]
                region_data_df = pd.read_csv(main_dir + '\\wx_data\\' + region_file, sep="\t",
                                             names=['date', 'temp_max', 'temp_min', 'precipitation_amount'],
                                             header=None)
                region_data_df = region_data_df.drop_duplicates()
                region_data_df.to_sql(table_name, con=conn, if_exists='replace')
                region_records = region_records + region_data_df.shape[0]
                # logger.info(f'No of records inserted for {region_file} is {region_data_df.shape[0]}')
            else:
                logger.info(f'Not a valid region file {region_file}')
                continue
        logger.info(f'Total inserted records for all regions is {region_records}')

        for yld_file in os.listdir(main_dir + '\\yld_data\\'):
            if yld_file.endswith(".txt"):
                table_name = yld_file.split('.')[0]
                yld_data_df = pd.read_csv(main_dir + '\\yld_data\\' + yld_file, sep="\t", names=['date', 'yield'],
                                          header=None)
                yld_data_df = yld_data_df.drop_duplicates()
                yld_data_df.to_sql(table_name, con=conn, if_exists='replace')
                logger.info(f'No of records inserted for {yld_file} is {yld_data_df.shape[0]}')
                break
            else:
                logger.info(f'Not a valid yield file {yld_file}')
                continue
    except Exception as e:
        logger.error(e)
        res_code = 400
    end = datetime.now()
    logger.info(f'End time : {str(end)}')
    logger.info(f'Time taken to load data is {end - start}')
    return {'Status': res_code}


if __name__ == '__main__':
    load_data()
