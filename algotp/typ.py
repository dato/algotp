from typing import ClassVar
from dataclasses import dataclass


__all__ = ["Alumne", "Docente", "IncompleteError"]


class IncompleteError(Exception):
    """TODO
    """


@dataclass
class Alumne:
    legajo: str
    nombre: str
    correo: str

    def __post_init__(self):
        if not self.legajo:
            raise IncompleteError

    SHEET_NAME: ClassVar = "DatosAlumnos"
    SHEET_COLUMNS: ClassVar = ("Padrón", "Alumno", "Email")
