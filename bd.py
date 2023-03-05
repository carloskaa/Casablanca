# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 22:44:16 2023

@author: Carlos Camilo Caro
"""

from datetime import datetime
import streamlit as st
import pandas as pd
from io import BytesIO
from Clases import Conexion_google_sheets

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

st.title("REGISTROS CASABLANCA MUEBLES TUNJA BOYACA") 
connection = Conexion_google_sheets()


st.write("Ingrese gasto nuevo")
lista_tipos = ["Muebles","Casa","Tapiceria"]
lista_tipos.insert(0, "-")
if st.checkbox("Agregar gasto"):
    lista= connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','gastos')
    now = datetime.now()
    col1, col2, col3= st.columns(3)
    with col1:
        gasto = st.text_input('Gasto',"-")
    with col2:
        costo = st.text_input('Costo',"-")
    with col3:
        tipo=st.selectbox("Tipo", ((lista_tipos)))
        
    if st.button("Agregue registro"):
        if tipo == "-" or gasto == "-" or costo == "-":
            st.error('Por favor ingrese datos')
        else:
            gs = lista[1]
            df = pd.DataFrame({'Gasto': [gasto], 'Costo':[float(costo)],  'Tipo': [tipo],'fecha':[now.strftime("%m/%d/%Y, %H:%M:%S")]})
            gs.values_append('gastos', {'valueInputOption': 'RAW'}, {'values': df.values.tolist()})
            st.success('Registro insertado')

if st.checkbox("Ver tabla"):
    lista = connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','gastos')
    list_gastos = lista[0]  
    df_gastos = pd.DataFrame(list_gastos[1:], columns= list_gastos[0], index = None)
    df_gastos['Costo'] = pd.to_numeric(df_gastos['Costo'], downcast="integer")
    df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'])
    df_gastos.loc[:, 'Precio'] ='$'+ df_gastos['Costo'].map('{:,.0f}'.format)
    dff =df_gastos[['Gasto', 'Precio', 'Tipo', 'fecha']]
    st.dataframe(dff)
    st.download_button(label='📥 Descargar DATAFRAME GENERADO', data=to_excel(df_gastos) ,file_name= "df_gastos.xlsx")
    

