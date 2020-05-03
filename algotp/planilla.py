import enum
import itertools

from frozendict import frozendict

from .typ import *
from .sheets import freeze_values

__all__ = ["Mixin", "Planilla"]


class DB(enum.Enum):
    LEGAJO = 0
    NOTAS_RAW = 1


class Mixin:
    """
    """

    def parse_sheets(self, sheet_dict):
        try:
            alu = sheet_dict[Alumne.SHEET_NAME]
            notas = sheet_dict["Notas"]
        except KeyError:
            raise NotImplementedError

        alu_list = parse_rows(alu, Alumne, Alumne.SHEET_COLUMNS)
        alu_dict = frozendict({alu.legajo: alu for alu in alu_list})
        raw_notas = freeze_values(notas)

        return frozendict({DB.LEGAJO: alu_dict, DB.NOTAS_RAW: raw_notas})

    @property
    def alu_map(self):
        return self.data[DB.LEGAJO]

    @property
    def notas_raw(self):
        return self.data[DB.NOTAS_RAW]


def parse_rows(rows, klass, fields):
    """TODO
    """
    indices = []
    objects = []
    headers = rows[0]

    for field in fields:
        indices.append(headers.index(field))

    for row in itertools.islice(rows, 1, None):
        try:
            # XXX str()
            objects.append(klass(*[str(row[i]) for i in indices]))
        except (IndexError, IncompleteError):
            continue

    return objects
