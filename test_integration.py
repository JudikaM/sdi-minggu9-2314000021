import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class TestCLI(unittest.TestCase):
    def run_cli(self, value):
        return subprocess.run(
            [sys.executable, str(ROOT / "app.py"), value],
            capture_output=True, text=True, timeout=10, cwd=ROOT,
        )

    def test_cli_at_threshold(self):
        result = self.run_cli("50000")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "500")
        self.assertEqual(result.stderr, "")

    def test_cli_free_fee_is_success(self):
        # 49.999 di bawah ambang: biaya 0 adalah hasil SAH, bukan error.
        # Proses harus keluar dengan status 0, mencetak "0", dan stderr kosong.
        # Ini membedakan "gratis" (status 0) dari "input ditolak" (status 2).
        result = self.run_cli("49999")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "0")
        self.assertEqual(result.stderr, "")

    def test_cli_negative(self):
        result = self.run_cli("-1")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("integer nonnegatif", result.stderr)

    def test_cli_non_numeric(self):
        result = self.run_cli("abc")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.strip())


if __name__ == "__main__":
    unittest.main()
