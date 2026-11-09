import argparse
import hashlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Verifikasi checksum satu ZIP kandidat")
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    expected = Path(str(args.archive) + ".sha256").read_text(encoding="utf-8").split()[0]
    actual = hashlib.sha256(args.archive.read_bytes()).hexdigest()
    matched = actual == expected
    print("MATCH" if matched else "MISMATCH")
    return 0 if matched else 1


if __name__ == "__main__":
    raise SystemExit(main())
