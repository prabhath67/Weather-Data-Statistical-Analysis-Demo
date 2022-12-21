import unittest

from src.stats.data_load import load_data


class TestingLoad(unittest.TestCase):

    def test_load_data(self):
        res = load_data()
        assert res['Status'] == 200


if __name__ == '__main__':
    unittest.main()
