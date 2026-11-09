"""Modul biaya layanan sesuai kontrak project UTS SDI."""
import argparse


def biaya(amount):
    if type(amount) is not int or amount < 0:
        raise ValueError("amount harus integer nonnegatif")
    if amount <= 50_000:
        return 0
    return min(amount // 100, 5_000)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Hitung biaya layanan koperasi")
    parser.add_argument("amount", type=int, help="Nominal rupiah integer nonnegatif")
    args = parser.parse_args(argv)
    try:
        result = biaya(args.amount)
    except ValueError as exc:
        parser.error(str(exc))
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
