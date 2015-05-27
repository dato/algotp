# -*- coding: utf-8 -*-

"""Módulo para autenticación con OAuth2."""

import datetime
import httplib2
import os
import sys

import oauth2client.client

_CLIENT_ID = os.environ["NOTAS_OAUTH_CLIENT"]
_CLIENT_SECRET = os.environ["NOTAS_OAUTH_SECRET"]
_OAUTH_REFRESH = os.environ["NOTAS_REFRESH_TOKEN"]

_creds = oauth2client.client.OAuth2Credentials(
    "", _CLIENT_ID, _CLIENT_SECRET, _OAUTH_REFRESH,
    datetime.datetime(2015, 1, 1),
    "https://accounts.google.com/o/oauth2/token", "notasweb/1.0")


def access_token():
    """Devuelve el token OAuth, refrescando las credenciales si es necesario.
    """
    # TODO: en lugar de refrescar cuando expire, refrescar quizá cinco minuts
    # antes para evitar race conditions.
    # TODO: locking?
    if _creds.access_token_expired:
        print >>sys.stderr, "Generando nuevo token de acceso."
        _creds.refresh(httplib2.Http())

    return _creds.access_token