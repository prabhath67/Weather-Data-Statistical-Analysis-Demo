import unittest

from src.stats.data_analysis_stats import *


class TestingStats(unittest.TestCase):

    def test_avg_max_temp(self):
        res = avg_max_temp(None)
        assert res == None

    def test_avg_min_temp(self):
        res = avg_min_temp(None)
        assert res == None

    def test_total_accum_prec(self):
        res = total_accum_prec(None)
        assert res == None

    def test_get_weather_on_date(self):
        res = get_weather_on_date(None, None)
        assert res == None

    def test_get_yield_on_date(self):
        res = get_yield_on_date(None)
        assert res == None

    def test_get_weather_stats(self):
        res = get_weather_stats(None)
        assert res == None


if __name__ == '__main__':
    unittest.main()
