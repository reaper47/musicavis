import os
import csv
from decimal import Decimal
from datetime import timedelta
from pathlib import Path
import json
from difflib import SequenceMatcher

import docx
import pandas as pd
import odf.opendocument as opendoc
from django.utils import timezone
from django.test import TestCase

from musicavis.settings import EXPORTS_DIR
from app.models.profile import Profile
from app.backend.utils.export import ExportPractices, FileDeleteWrapper
from app.backend.utils.enums import FileType, NewLine
from app.models.practice import Instrument, Goal, Improvement, Positive, Exercise
from app.tests.conftest import create_user_with_a_practice, delete_users

a_date = timezone.now()
other_date = a_date + timedelta(days=1)
a_goal = Goal(name='eat')
other_goal = Goal(name='sleep')
a_positive = Positive(name='good picking')
other_positive = Positive(name='was able to focus this time')
an_improvement = Improvement(name='hold pick lighter')
other_improvement = Improvement(name='practice slower ex8 next time')
an_exercise = Exercise(name='C-Arpeggio', bpm_start=60, bpm_end=80, minutes=Decimal('6.00'))
other_exercise = Exercise(name='D-Arpeggio', bpm_start=90, bpm_end=80, minutes=Decimal('4.00'))
an_instrument = Instrument(name='paper mills')
other_instrument = Instrument(name='harp')
some_notes = 'the brim was held like a champ'


def export_practices(profile: Profile) -> ExportPractices:
    practice = profile.practices.first()
    practice.notes = some_notes
    practice.date = a_date

    an_instrument.save()
    practice.instrument = an_instrument

    for goal in [a_goal, other_goal]:
        goal.save()
        practice.goals.add(goal)

    for exercise in [an_exercise, other_exercise]:
        exercise.save()
        practice.exercises.add(exercise)

    for positive in [a_positive, other_positive]:
        positive.save()
        practice.positives.add(positive)

    for improvement in [an_improvement, other_improvement]:
        improvement.save()
        practice.improvements.add(improvement)

    return ExportPractices('test', [practice], NewLine.UNIX)


class ExportsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.a_user = create_user_with_a_practice()
        cls.export_practices = export_practices(cls.a_user.profile)

    @classmethod
    def tearDownClass(cls):
        files = [f for f in os.listdir(EXPORTS_DIR)]
        for f in files:
            os.remove(f'{EXPORTS_DIR}/{f}')
        delete_users()

    def test_export_csv(self):
        data_expected = (f'{a_date},{an_instrument.name.title()}\n'
                         f'goals: {a_goal.name},{other_goal.name}\n'
                         f'exercises: {an_exercise.name},{an_exercise.bpm_start}bpm,{an_exercise.bpm_end}bpm,'
                         f'{an_exercise.minutes}m,\n\t\t\t{other_exercise.name},{other_exercise.bpm_start}bpm,'
                         f'{other_exercise.bpm_end}bpm,{other_exercise.minutes}m\n'
                         f'improvements: {an_improvement.name},{other_improvement.name}\n'
                         f'positives: {a_positive.name},{other_positive.name}\n'
                         f'notes: {some_notes}\n\n')

        file_actual = self.export_practices.export(FileType.CSV)

        self.assertTrue(are_files_equivalent(data_expected, file_actual, FileType.CSV))

    def test_export_docx(self):
        text_expected = (f'Practice Sessions for Test\nPaper Mills ({a_date:%a, %B %m %Y})\nGoals\neat\nsleep\n'
                         'Exercises\nC-Arpeggio at 60-80bpm for 6.00m\nD-Arpeggio at 90-80bpm for 4.00m\nImprovements\n'
                         'hold pick lighter\npractice slower ex8 next time\nPositives\ngood picking\n'
                         'was able to focus this time\nNotes\nthe brim was held like a champ')

        fname = self.export_practices.export(FileType.DOCX)
        text = '\n'.join([p.text for p in docx.Document(f'{EXPORTS_DIR}/{fname}').paragraphs])

        self.assertEqual(text_expected, text)

    def test_export_xlsx(self):
        data_expected = (f'Practice#1-PaperMills-{a_date:%a,%B%m%Y}Unnamed:1Unnamed:2Unnamed:3Unnamed:4Unnamed:5'
                         'Unnamed:6Unnamed:70NaNGoalsExerciseNameBpmRangeTime(minutes)ImprovementsPositives'
                         'Notes10.0eatC-Arpeggio60-806holdpicklightergoodpickingthebrimwasheldlikeachamp21.0'
                         'sleepD-Arpeggio90-804practiceslowerex8nexttimewasabletofocusthistimeNaN')

        fname = self.export_practices.export(FileType.XLSX)
        df = pd.read_excel(f'{EXPORTS_DIR}/{fname}', sheet_name='Practices')
        data_actual = str(df).replace(' ', '').replace('\n', '').replace('[3rowsx8columns]', '')

        self.assertGreaterEqual(SequenceMatcher(None, data_expected, data_actual).ratio(), 0.85)

    def test_export_xml(self):
        data_expected = (f'<?xml version="1.0" ?>\n'
                         f'<Practices>\n'
                         f'  <Practice>\n'
                         f'    <Metadata>\n'
                         f'      <Number>1</Number>\n'
                         f'      <Date>{a_date}</Date>\n'
                         f'      <Instrument>{an_instrument.name.title()}</Instrument>\n'
                         f'    </Metadata>\n'
                         f'    <Goals>\n'
                         f'      <Name>{a_goal.name}</Name>\n'
                         f'      <Name>{other_goal.name}</Name>\n'
                         f'    </Goals>\n'
                         f'    <Exercises>\n'
                         f'      <Exercise>\n'
                         f'        <Name>{an_exercise.name}</Name>\n'
                         f'        <BpmRange>{an_exercise.bpm_start}-{an_exercise.bpm_end}</BpmRange>\n'
                         f'        <Minutes>{an_exercise.minutes}</Minutes>\n'
                         f'      </Exercise>\n'
                         f'      <Exercise>\n'
                         f'        <Name>{other_exercise.name}</Name>\n'
                         f'        <BpmRange>{other_exercise.bpm_start}-{other_exercise.bpm_end}</BpmRange>\n'
                         f'        <Minutes>{other_exercise.minutes}</Minutes>\n'
                         f'      </Exercise>\n'
                         f'    </Exercises>\n'
                         f'    <Improvements>\n'
                         f'      <Name>{an_improvement.name}</Name>\n'
                         f'      <Name>{other_improvement.name}</Name>\n'
                         f'    </Improvements>\n'
                         f'    <Positives>\n'
                         f'      <Name>{a_positive.name}</Name>\n'
                         f'      <Name>{other_positive.name}</Name>\n'
                         f'    </Positives>\n'
                         f'    <Notes>{some_notes}</Notes>\n'
                         f'  </Practice>\n'
                         f'</Practices>\n')

        file_actual = self.export_practices.export(FileType.XML)

        self.assertTrue(are_files_equivalent(data_expected, file_actual, FileType.XML))

    def test_export_txt(self):
        data_expected = (f'{an_instrument.name.title()} ({a_date})\n'
                         f'goals -> {a_goal.name}, {other_goal.name}\n'
                         f'exercises ->\n\t{an_exercise.name} {an_exercise.bpm_start}-{an_exercise.bpm_end}bpm '
                         f'{an_exercise.minutes}m\n\t{other_exercise.name} {other_exercise.bpm_start}-'
                         f'{other_exercise.bpm_end}bpm {other_exercise.minutes}m\n'
                         f'improvements -> {an_improvement.name}, {other_improvement.name}\n'
                         f'positives -> {a_positive.name}, {other_positive.name}\n'
                         f'notes -> {some_notes}\n\n')

        file_actual = self.export_practices.export(FileType.TXT)

        self.assertTrue(are_files_equivalent(data_expected, file_actual, FileType.TXT))

    def test_export_pdf(self):
        fname = self.export_practices.export(FileType.PDF)

        path = Path(f'{EXPORTS_DIR}/{fname}')
        self.assertTrue(path.is_file())
        self.assertGreater(path.stat().st_size, 0)

    def test_export_json(self):
        json_expected = {
            'practice-1': {
                'metadata': {
                    'date': str(a_date),
                    'instrument': an_instrument.name.title()
                },
                'goals': [a_goal.name, other_goal.name],
                'exercises': [
                    {
                        'name': an_exercise.name,
                        'bpm_range': f'{an_exercise.bpm_start}-{an_exercise.bpm_end}',
                        'minutes': float(an_exercise.minutes)
                    },
                    {
                        'name': other_exercise.name,
                        'bpm_range': f'{other_exercise.bpm_start}-{other_exercise.bpm_end}',
                        'minutes': float(other_exercise.minutes)
                    }
                ],
                'improvements': [an_improvement.name, other_improvement.name],
                'positives': [a_positive.name, other_positive.name],
                'notes': some_notes
            }
        }

        json_file = self.export_practices.export(FileType.JSON)

        with open(f'{EXPORTS_DIR}/{json_file}') as f:
            assert json.dumps(json_expected, indent=2) == f.read()

    def test_export_odt(self):
        text_expected = (f'[{a_date:%a, %d %B %Y}] Practice #1 - {an_instrument.name.title()}Goals:{a_goal.name}'
                         f'{other_goal.name}Exercises:{an_exercise.name} - {an_exercise.bpm_start} to '
                         f'{an_exercise.bpm_end} bpm - {an_exercise.minutes}m{other_exercise.name} - '
                         f'{other_exercise.bpm_start} to {other_exercise.bpm_end} bpm - '
                         f'{other_exercise.minutes}mImprovements:{an_improvement.name}{other_improvement.name}'
                         f'Positives:{a_positive.name}{other_positive.name}Notes: {some_notes}')

        fname = self.export_practices.export(FileType.ODT)
        text = str(opendoc.load(f'{EXPORTS_DIR}/{fname}').text)

        self.assertEqual(text_expected, text)

    def test_export_ods(self):
        text_expected = (f'Practice #1{an_instrument.name.title()}{a_date:%a, %d %B %Y}Goals:{a_goal.name}'
                         f'{other_goal.name}Exercises:{an_exercise.name}{an_exercise.bpm_start}-'
                         f'{an_exercise.bpm_end} bpm{an_exercise.minutes}m{other_exercise.name}'
                         f'{other_exercise.bpm_start}-{other_exercise.bpm_end} bpm{other_exercise.minutes}m'
                         f'Improvements:{an_improvement.name}{other_improvement.name}Positives:'
                         f'{a_positive.name}{other_positive.name}Notes:{some_notes}')

        fname = self.export_practices.export(FileType.ODS)
        text = str(opendoc.load(f'{EXPORTS_DIR}/{fname}').spreadsheet)

        self.assertEqual(text_expected, text)

    def test_open_then_delete_deletes_file(self):
        """
        GIVEN an exported file stored under the exports dir
        WHEN the file is open
        THEN delete it
        """
        fname = self.export_practices.export(FileType.TXT)
        filepath = f'{EXPORTS_DIR}/{fname}'

        chunkSize = 16384
        wrapper = FileDeleteWrapper(filepath=filepath, filelike=open(filepath, 'rb'), blksize=chunkSize)

        del wrapper
        self.assertFalse(os.path.isfile(filepath))


def are_files_equivalent(expected, actual, filetype: FileType):
    expected = expected.split('\n')
    with open(f'{EXPORTS_DIR}/{actual}', newline=NewLine.UNIX.value) as f:
        if filetype == FileType.CSV:
            rows = csv.reader(f)
            for row_expected, row in zip(expected, rows):
                if row_expected != ','.join(row).replace(':,', ': '):
                    return False
        elif filetype in [FileType.TXT, FileType.XML]:
            for line_expected, line in zip(expected, f):
                if line_expected + '\n' != line:
                    return False
    return True
