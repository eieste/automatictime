import datetime
import functools
import locale
import logging

from google.oauth2 import service_account
from googleapiclient.discovery import build

log = logging.getLogger(__name__)


class ColNames:
    TOPIC = "C"
    START = "D"
    END = "E"
    PAUSE = "F"


class GoogleSheet:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    COL_START = "A"
    COL_END = "F"
    ROW_START = 2
    ROW_END = 32 + ROW_START

    def __init__(self, config):
        self.config = config
        self.service = build("sheets", "v4", credentials=self.login())

    def login(self):
        log.debug("Use keyfile from path {}".format(self.config.key_file))
        return service_account.Credentials.from_service_account_file(self.config.key_file,
                                                                     scopes=GoogleSheet.SCOPES)

    def get_sheet(self):
        return self.service.spreadsheets()

    def get_sheet_range(self, row_start=None, row_end=None, col_start=None, col_end=None):
        if not row_start:
            row_start = GoogleSheet.ROW_START
        if not row_end:
            row_end = GoogleSheet.ROW_END
        if not col_start:
            col_start = GoogleSheet.COL_START
        if not col_end:
            col_end = GoogleSheet.COL_END

        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
        d = datetime.datetime.now()
        TABLE_NAME = "{} {}".format(d.strftime("%B"), d.strftime("%Y"))
        return "'{}'!{}{}:{}{}".format(TABLE_NAME, col_start, row_start, col_end, row_end)

    def find_line(self):
        d = datetime.datetime.now()
        i = GoogleSheet.ROW_START - 1
        for line in self.get_sheet_value(col_start="B", col_end="B").get("values", []):
            i = i + 1
            if line[0] == d.strftime("%d.%m.%Y"):
                return i

    @functools.cache
    def get_sheet_value(self, row_start=None, row_end=None, col_start=None, col_end=None):
        range = self.get_sheet_range(row_start=row_start, row_end=row_end, col_start=col_start, col_end=col_end)
        log.debug("Load data from {}".format(range))
        log.debug("Get Sheet Range")
        return self.get_sheet().values().get(spreadsheetId=self.config.sheet_id,
                                             range=range).execute()

    def update(self, linenr, col, value):
        log.debug("Request {} Update".format(col))

        cell_pos = {"row_start": linenr,
                    "row_end": linenr,
                    "col_start": getattr(ColNames, col),
                    "col_end": getattr(ColNames, col)
                    }
        cell_value = self.get_sheet_value(**cell_pos).get(
            "values", [])

        payload = [None]
        log.debug("Request {} Update {}".format(col, value))
        if len(cell_value) <= 0:
            log.debug("Update {} = {}".format(col, value))
            payload[0] = value

        self.get_sheet().values().update(
            spreadsheetId=self.config.sheet_id,
            range=self.get_sheet_range(**cell_pos),
            body={
                "values": [
                    payload
                ]
            },
            valueInputOption="RAW"
        ).execute()
