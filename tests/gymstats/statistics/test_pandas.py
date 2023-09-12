import unittest
import pandas as pd

from gymstats.statistics.pandas import df_flashes, df_tops, df_hard_tops, df_attempts, df_zones, df_fails, df_tops_all
from gymstats.helper.names import ATPS, ZONE_ATPS, TOP_ATPS, RANK, PREV


class TestPandas(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame as test fixture
        columns = [ATPS, ZONE_ATPS, TOP_ATPS, RANK, PREV]
        data = {
            1: [1, 1, 1, -1, -1],  # flash, never tried before
            43: [1, 1, 1, 1, -1],  # flash, never tried before
            23: [100, 1, 1, -1, -1],  # flash, never tried before
            3: [1, 1, 1, 0, 1],  # flash, zoned before
            7: [1, 1, 1, 1, 0],  # flash, failed before
            8: [1, 1, 1, 0, 2],  # flash, topped before
            9: [8, 1, 2, -1, -1],  # top, never tried before
            11: [3, 3, 3, 2, -1],  # top, never tried before
            2: [4, 2, 2, 0, 1],  # top, zoned before
            76: [59, 58, 59, 2, 1],  # top, many tries, zoned before 
            123: [12, 8, 10, 2, 2],  # top, topped before
            12: [2, 2, 2, -1, 2],  # top, topped before
            14: [3, 3, -1, -1, -1],  # zone, never tried before
            87: [2, 1, -1, 0, 2],  # zone, topped before
            100: [15, 8, -1, 2, 1],  # zone, zoned before
            4: [1, 1, -1, 1, 0],  # zone, failed before
            101: [1, -1, -1, -1, -1],  # fail: never tried before
            99: [10, -1, -1, -1, -1],  # fail: never tried before
            50: [1, -1, -1, 0, 2],  # fail: topped before
            54: [3, -1, -1, 1, 2],  # fail: topped before
            51: [12, -1, -1, 2, 0],  # fail: failed before
            57: [4, -1, -1, -1, 1],  # fail: zoned before
            52: [5, -1, -1, 1, 1],  # fail, zoned before
            }
        self.df = pd.DataFrame(data).transpose()
        self.df.columns = columns

    def test_flashes(self):
        flashes = df_flashes(self.df)
        self.assertEqual(flashes, 3)

    def test_tops(self):
        tops = df_tops(self.df)
        self.assertEqual(tops, 9)

    def test_tops_all(self):
        tops_all = df_tops_all(self.df)
        self.assertEqual(tops_all, 12)

    def test_zones(self):
        zones = df_zones(self.df)
        self.assertEqual(zones, 2)

    def test_hard_tops(self):
        hard_tops = df_hard_tops(self.df)
        self.assertEqual(hard_tops, 4)

    def test_fails(self):
        fails = df_fails(self.df)
        self.assertEqual(fails, 2)
    
    def test_attempts(self):
        attempts = df_attempts(self.df)
        self.assertEqual(attempts, 250)


if __name__ == '__main__':
    unittest.main()