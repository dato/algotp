import time
import threading

from dataclasses import dataclass
from typing import List, Dict

from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

__all__ = ["Config", "PullDb", "TimedDB", "PushDB"]


@dataclass
class Config:
    spreadsheet_id: str
    credentials: Dict
    fetch_sheets: List[str]


class PullDB:
    """
    """

    def __init__(self, config: Config, initial_fetch=False):
        # TODO: retry request
        service = discovery.build("sheets", "v4", credentials=config.credentials)
        spreadsheets = service.spreadsheets()
        self._query = spreadsheets.values().batchGet(
            spreadsheetId=config.spreadsheet_id,
            ranges=config.fetch_sheets,
            valueRenderOption="UNFORMATTED_VALUE",
        )
        self._lock = threading.Lock()
        self._credentials = config.credentials  # For PushDB
        self.__data = None
        if initial_fetch:
            self.refresh()

    @property
    def data(self):
        return self.get()

    def get(self, force_refresh=False):
        """
        """
        if force_refresh or self.__data is None:
            self.refresh()
        return self.__data

    def refresh(self):
        """
        """
        result = self._query.execute()
        sheets = parse_values(result["valueRanges"])
        try:
            new_data = super(PullDB, self).parse_sheets(sheets)
        except NotImplementedError:
            new_data = tuple((sheet, tuple(data)) for sheet, data in sheets.items())
            # new_data = tuple((sheet, values_list_to_tuple(data)) for sheet, data in sheets.items())
        with self._lock:
            self.__data = new_data

    def parse_sheets(self, data):
        """
        """
        raise NotImplementedError


def parse_values(sheet_ranges: List[Dict]) -> Dict[str, List[List[str]]]:
    """Segrega por hoja la lista de rango/valores obtenidos.

    Args:
      sheet_ranges: el resultado "valueRanges" de batchGet(), esto es,
          una lista de diccionarios con las celdas de cada hoja.

    Returns:
      un diccionario con los valores asociados a cada hoja.
    """
    hojas_dict = {}

    for sheet_data in sheet_ranges:
        sheet_rows = sheet_data["values"]
        sheet_name, _ = sheet_data["range"].split("!", 1)
        hojas_dict[sheet_name] = sheet_rows

    return hojas_dict


def freeze_values(values):
    """
    """
    return tuple(tuple(row) for row in values)
