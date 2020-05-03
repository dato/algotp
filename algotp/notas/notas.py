import itertools
import os

from . import notas_oauth

from algotp import sheets, planilla

# Constantes
COL_EMAIL = "Email"
COL_PADRON = "Padrón"

SHEET_NOTAS = "Notas"
SHEET_ALUMNOS = "DatosAlumnos"

# Configuración externa.
SPREADSHEET_KEY = os.environ["NOTAS_SPREADSHEET_KEY"]


class Planilla(sheets.PullDB, planilla.Mixin):
    def __init__(self):
        creds = notas_oauth.get_credenciales()
        config = sheets.Config(SPREADSHEET_KEY, creds, [SHEET_NOTAS, SHEET_ALUMNOS])
        super(Planilla, self).__init__(config)

    def verificar(self, padron, email):
        """Verifica que hay un alumno con el padrón y e-mail indicados.
        """
        try:
            alu = self.alu_map[padron]
        except KeyError:
            return False
        else:
            return email.lower() == alu.correo.lower()

    def notas(self, padron):
        notas = self.notas_raw
        headers = notas[0]
        idx_padron = headers.index(COL_PADRON)

        for alumno in itertools.islice(notas, 1, None):
            if padron.lower() == str(alumno[idx_padron]).lower():
                return zip(headers, alumno)

        raise IndexError(f"Padrón {padron} no encontrado")


if __name__ == "__main__":
    planilla = Planilla()
    print(planilla.verificar("942039", "aaa"))
