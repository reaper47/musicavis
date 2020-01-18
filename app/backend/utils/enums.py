from enum import Enum


class TokenType(Enum):
    RESET = 'reset'
    CONFIRM = 'confirm'
    UNSUBSCRIBE = 'unsubscribe'


class FileType(Enum):
    PDF = 'pdf'
    DOCX = 'docx'
    XLSX = 'xlsx'
    CSV = 'csv'
    TXT = 'txt'
    JSON = 'json'
    XML = 'xml'
    ODT = 'odt'
    ODS = 'ods'

    @staticmethod
    def from_string(filetype):
        if filetype == 'pdf':
            return FileType.PDF
        elif filetype == 'docx':
            return FileType.DOCX
        elif filetype == 'xlsx':
            return FileType.XLSX
        elif filetype == 'csv':
            return FileType.CSV
        elif filetype == 'txt':
            return FileType.TXT
        elif filetype == 'json':
            return FileType.JSON
        elif filetype == 'xml':
            return FileType.XML
        elif filetype == 'odt':
            return FileType.ODT
        elif filetype == 'ods':
            return FileType.ODS
        else:
            raise NotImplementedError

    @staticmethod
    def description(filetype):
        if filetype == FileType.PDF:
            return 'Portable Document Format (.pdf)'
        elif filetype == FileType.DOCX:
            return 'Microsoft Word (.docx)'
        elif filetype == FileType.XLSX:
            return 'Microsoft Excel (.xlsx)'
        elif filetype == FileType.CSV:
            return 'Comma-Separated Values (.csv)'
        elif filetype == FileType.TXT:
            return 'Text (.txt)'
        elif filetype == FileType.JSON:
            return 'JavaScript Object Notation (.json)'
        elif filetype == FileType.XML:
            return 'Extensible Markup Language (.xml)'
        elif filetype == FileType.ODT:
            return 'ODF Text Document (.odt)'
        elif filetype == FileType.ODS:
            return 'ODF Spreadsheet Document (.ods)'
        else:
            raise NotImplementedError


class NewLine(Enum):
    UNIX = '\n'
    WINDOWS = '\r\n'

    @staticmethod
    def from_string(os):
        if any(k in os.lower() for k in ['linux', 'mac', 'x11']):
            return NewLine.UNIX
        else:
            return NewLine.WINDOWS
