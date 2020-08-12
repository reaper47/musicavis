from django.test import TestCase
from app.backend.utils.enums import FileType, NewLine, FormType


class EnumsTests(TestCase):
    def test_filetype_fromstring(self):
        file_types_expected = [FileType.from_string(x.value) for x in FileType]

        self.assertEqual(file_types_expected, [x for x in FileType])

    def test_filetype_fromstring_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            FileType.from_string("gif")

    def test_filetype_description_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            FileType.description("gif")

    def test_newline_fromstring(self):
        unix = ["linux", "mac", "x11"]
        windows = ["windows", "vista", "10"]

        self.assertTrue(all(NewLine.from_string(x) == NewLine.UNIX for x in unix))
        self.assertTrue(all(NewLine.from_string(x) == NewLine.WINDOWS for x in windows))

    def test_formtype_from_keys(self):
        keys = [["new_password"], ["new_email"], ["new_username"]]
        types_expected = [
            FormType.CHANGE_PASSWORD,
            FormType.CHANGE_EMAIL,
            FormType.CHANGE_USERNAME,
        ]

        self.assertTrue(
            all([FormType.get_form_type(k) == t for k, t in zip(keys, types_expected)])
        )
