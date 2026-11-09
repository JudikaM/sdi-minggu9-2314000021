import unittest
from app import biaya


class TestBiaya(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(biaya(0), 0)

    def test_below_threshold(self):
        self.assertEqual(biaya(49_999), 0)

    def test_at_threshold(self):
        self.assertEqual(biaya(50_000), 500)

    def test_normal(self):
        self.assertEqual(biaya(275_550), 2_755)

    def test_round_down(self):
        self.assertEqual(biaya(123_456), 1_234)

    def test_cap_boundary(self):
        self.assertEqual(biaya(500_000), 5_000)

    def test_above_cap(self):
        self.assertEqual(biaya(900_000), 5_000)

    def test_one_above_threshold(self):
        # 50.001 sudah di atas ambang, jadi tidak gratis. 1% = 500,01 dan
        # dibulatkan ke bawah menjadi 500 (bukan 501). Kasus ini juga
        # memastikan kondisi gratis hanya berlaku untuk amount < 50.000.
        self.assertEqual(biaya(50_001), 500)

    def test_one_below_cap(self):
        # 499.999 satu rupiah di bawah titik cap 500.000. 1% = 4.999,99 dan
        # dibulatkan ke bawah menjadi 4.999, bukan 5.000. Ini membuktikan
        # pembulatan adalah floor (//), bukan round, dan cap belum aktif.
        self.assertEqual(biaya(499_999), 4_999)

    def test_negative(self):
        with self.assertRaises(ValueError):
            biaya(-1)

    def test_wrong_types(self):
        for value in ["50000", 50000.0, True, None]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    biaya(value)


if __name__ == "__main__":
    unittest.main()
