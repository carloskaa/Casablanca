# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:44:43 2023

@author: Automate
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
#%%  CONEXION CON BASES DE DATOS
class Conexion_google_sheets():
  def __init__(self):
    self.SERVICE_ACCOUNT_FILE = 'keys_casablanca.json'
    self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    self.creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
    self.service = build('sheets', 'v4', credentials=self.creds)
    self.sheet = self.service.spreadsheets()
    self.gc = gspread.authorize(self.creds)
  def conexion_sheets(self,idd,hsheet):
    result = self.sheet.values().get(spreadsheetId=idd,
                                range=hsheet).execute()   
    values = result.get('values',[])
    
    gs = self.gc.open_by_key(idd)
    # worksheet1 = gs.worksheet(hsheet)
    return [values,gs] 


# open a google sheet

# select a work sheet from its name


# class Carpetas():
# import time
# inicio = time.time()

# fin = time.time()
# print(fin-inicio) # 1.5099220275878906                                                                                            