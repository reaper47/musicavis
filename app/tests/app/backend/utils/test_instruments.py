from django.test import TestCase

from app.backend.utils.instruments import gather_instruments


class InstrumentsTests(TestCase):

    def test_gather_instruments(self):
        """
        WHEN the instruments are parsed
        THEN all of the 44 instruments are stored in a set
        """
        instruments = gather_instruments()

        self.assertTrue(type(instruments) is set)
        self.assertEqual(len(instruments), 44)
