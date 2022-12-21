import datetime
import unittest

from src.stats.data_analysis_stats import *
from src.stats.data_load import load_data


class TestingStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_data()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_avg_max_temp(self):
        res = avg_max_temp()
        assert res['Status'] == 200

    def test_avg_min_temp(self):
        res = avg_min_temp()
        assert  res['Status'] == 200

    def test_total_accum_prec(self):
        res = total_accum_prec()
        assert res['Status'] == 200

    def test_get_weather_on_date(self):
        date = datetime.datetime.strptime('01/01/1987','%d/%m/%Y').date()
        res = get_weather_on_date(date, 'USC00110072')
        assert res == [{'date': 19870101, 'temp_max': 11, 'temp_min': -39, 'precipitation_amount': 36}]

    def test_get_yield_on_date(self):
        date = datetime.datetime.strptime('01/01/1987','%d/%m/%Y').date()
        res = get_yield_on_date(date)
        assert res == [{'date': 1987, 'yield': 181143}]

    def test_get_weather_stats(self):
        res = get_weather_stats('USC00110072')
        assert len(res) == 10865


if __name__ == '__main__':
    unittest.main()
