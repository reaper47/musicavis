from pathlib import Path

from app.models.practice import Instrument


def gather_instruments():
    instruments_file = f'{Path(__file__).resolve().parent}/instruments.txt'
    with open(instruments_file) as f:
        instruments = f.readlines()
    return set(instruments)


def populate_db():
    instruments = Instrument.objects.all()
    if not instruments:
        all_instruments = gather_instruments()
        for name in all_instruments:
            instrument = Instrument(name=name.replace('\n', '').replace('\r', '').strip().lower())
            instrument.save()
    else:
        print('Instruments already pushed in the database.')
