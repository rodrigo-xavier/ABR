# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 11/03/2020

@description: PyDash Project

Everything always starts from somewhere =)
"""

from dash_client import DashClient
from debug import debug_requests_on

debug_requests_on()
dash_client = DashClient()
dash_client.run_application()