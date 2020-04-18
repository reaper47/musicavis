from pathlib import Path

from app.models.practice import Instrument


def populate_db():
    instruments = Instrument.objects.all()
    if not instruments:
        all_instruments = gather_instruments()
        Instrument.objects.bulk_create(
            [
                Instrument(
                    name=name.replace("\n", "").replace("\r", "").strip().lower()
                )
                for name in all_instruments
            ]
        )
    else:
        print("Instruments already pushed in the database.")


def gather_instruments():
    instruments_file = f"{Path(__file__).resolve().parent}/instruments.txt"
    with open(instruments_file) as f:
        instruments = f.readlines()
    return set(instruments)
