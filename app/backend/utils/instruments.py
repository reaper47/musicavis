from pathlib import Path


def gather_instruments():
    instruments_file = f'{Path(__file__).resolve().parent}/instruments.txt'
    with open(instruments_file) as f:
        instruments = f.readlines()
    return set(instruments)
