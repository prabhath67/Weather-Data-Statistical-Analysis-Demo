import unittest

from prabjat.src.stats.data_load import load_data


class TestingLoad(unittest.TestCase):

    def test_load_data(self):
        res = load_data(None, None)
        assert res == None


if __name__ == '__main__':
    unittest.main()
