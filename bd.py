# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 22:44:16 2023

@author: Carlos Camilo Caro
"""
import mysql.connector as mariadb
from datetime import datetime
import streamlit as st
import pandas as pd
from io import BytesIO

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

mariadb_conexion = mariadb.connect(host='127.0.0.1', port='3306',user='root', password='Tunja2021', database='casablanca')
cursor = mariadb_conexion.cursor()
now = datetime.now()

st.title("REGISTROS CASABLANCA MUEBLES") 

st.write("Ingrese gasto nuevo")
lista_tipos = ["Muebles","Casa","Tapiceria"]
lista_tipos.insert(0, "-")
if st.checkbox("Agregar gasto"):
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
            sql = "INSERT INTO registros_gastos (Gasto,Costo,Tipo,fecha) VALUES (%s, %s, %s,%s)"
            val = (gasto, costo,tipo,now)
            cursor.execute(sql, val)
            mariadb_conexion.commit()
            print(cursor.rowcount, "registro insertado")
            st.success('Registro insertado')

if st.checkbox("Ver tabla"):
    df = pd.read_sql_query("SELECT * FROM registros_gastos", mariadb_conexion)
    st.dataframe(df)
    st.download_button(label='📥 Descargar DATAFRAME GENERADO', data=to_excel(df) ,file_name= "df.xlsx")
    
mariadb_conexion.close()

# cursor1=conexion1.cursor()
# cursor.execute("select * from registros_gastos")
# for fila in cursor:
#     print(fila)
# conexion.close()

# try:
#     cursor.execute("SELECT ID,USERNAME,PASSWORD,NOMBRE FROM Usuarios")
#     for id_usuario, username, password, nombre in cursor:
#         print("id: " + str(id_usuario))
#         print("username: " + username)
#         print("password: " + password)
#         print("nombre: " + nombre)
