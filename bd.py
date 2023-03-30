# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 22:44:16 2023

@author: Carlos Camilo Caro
"""

from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from io import BytesIO
from Clases import Conexion_google_sheets
from PIL import Image
import plotly.express as px
import plotly.graph_objs as go
st.set_page_config(page_title="Casablanca",page_icon=Image.open("Logo.ico"))

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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

def streamlit_menu():
    selected = option_menu(
        menu_title=None,  # required
        options=["Home", "Gastos", "Ingresos","Otros"],  # required
        icons=["house", "book", "archive fill"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "blue", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",},
            "nav-link-selected": {"background-color": "red"},} ,)
    return selected

selected = streamlit_menu()

if selected == "Home":
    st.title("REGISTROS CASABLANCA MUEBLES")
    a1, a2, a3 = st.columns(3)
    b1, b2, b3 = st.columns(3)
    connection = Conexion_google_sheets()
    lista= connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','gastos')
    lista2= connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','ingresos')
    list_gastos = lista[0]
    list_ingresos = lista2[0]
    
    df_gastos = pd.DataFrame(list_gastos[1:], columns= list_gastos[0], index = None)
    df_gastos['Costo'] = pd.to_numeric(df_gastos['Costo'], downcast="integer")
    df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'],format="%d/%m/%Y, %H:%M:%S",errors='coerce')
    
    df_ingreso = pd.DataFrame(list_ingresos[1:], columns= list_ingresos[0], index = None)
    df_ingreso['Costo'] = pd.to_numeric(df_ingreso['Costo'], downcast="integer")
    df_ingreso['fecha'] = pd.to_datetime(df_ingreso['fecha'],format="%d/%m/%Y, %H:%M:%S",errors='coerce')
    
    now = datetime.now()

    a1.metric("Año",'$'+'{:,}'.format(df_gastos.groupby(df_gastos['fecha'].dt.year)['Costo'].sum()[now.year]), "-0%")
    a2.metric("Mes",'$'+'{:,}'.format(df_gastos.groupby(df_gastos['fecha'].dt.month)['Costo'].sum()[now.month]), "-0%")
    a3.metric("Dia",'$'+'{:,}'.format(df_gastos['Costo'][df_gastos['fecha'].dt.strftime('%d-%m-%Y')== now.strftime("%d-%m-%Y")].sum()), "-0%")
    b1.metric("Año",'$'+'{:,}'.format(df_ingreso.groupby(df_ingreso['fecha'].dt.year)['Costo'].sum()[now.year]), "0%")
    b2.metric("Mes",'$'+'{:,}'.format(df_ingreso.groupby(df_ingreso['fecha'].dt.month)['Costo'].sum()[now.month]), "0%")
    b3.metric("Dia",'$'+'{:,}'.format(df_ingreso['Costo'][df_ingreso['fecha'].dt.strftime('%d-%m-%Y')== now.strftime("%d-%m-%Y")].sum()), "0%")
    
    
    # df['Precio'] = pd.to_numeric(df['Precio'].str.replace('[^\d.]', ''))
    gastostipo = pd.pivot_table(df_gastos, values='Costo', columns=['Tipo'], aggfunc=sum)
    gastospago = pd.pivot_table(df_gastos, values='Costo', columns=['pago'], aggfunc=sum)
    
    # fig = go.Figure(data=[go.Table(
    # header=dict(values=list(gastostipo.columns),
    #             fill_color='paleturquoise',
    #             align='left'),
    # cells=dict(values=[gastostipo['Casa']],
    #            fill_color='lavender',
    #            align='left'))])

    # st.plotly_chart(fig)
    
    # fig = go.Figure(data=[go.Table(
    # header=dict(values=list(gastospago.columns),
    #             fill_color='paleturquoise',
    #             align='left'),
    # cells=dict(values=[gastospago['Casa']],
    #            fill_color='lavender',
    #            align='left'))])

    # st.plotly_chart(fig)
    
    
    
    
if selected == "Gastos":
    st.write("Ingrese gasto nuevo")
    lista_tipos = ["Muebles","Casa","Tapiceria"]
    lista_tipos.insert(0, "-")
    lista_pagos = ["Efectivo","Bancolombia Casablanca","Bancolombia Carlos","Davivienda Carlos"]
    lista_pagos.insert(0, "-")
    if st.checkbox("Agregar gasto"):
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            gasto = st.text_input('Gasto',"-")
        with col2:
            costo = st.text_input('Costo',"-")
        with col3:
            tipo=st.selectbox("Tipo", ((lista_tipos)))
        with col4:
            pago=st.selectbox("Pago", ((lista_pagos)))
            
        if st.button("Agregue registro"):
            if tipo == "-" or gasto == "-" or costo == "-" or pago == "-":
                st.error('Por favor ingrese datos')
            else:
                connection = Conexion_google_sheets()
                lista= connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','gastos')
                now = datetime.now()
                gs = lista[1]
                df = pd.DataFrame({'Gasto': [gasto], 'Costo':[float(costo)],  'Tipo': [tipo],'Pago': [pago],'fecha':[now.strftime("%d/%m/%Y, %H:%M:%S")]})
                gs.values_append('gastos', {'valueInputOption': 'RAW'}, {'values': df.values.tolist()})
                st.success('Registro insertado')

    if st.checkbox("Ver tabla"):
        connection = Conexion_google_sheets()
        lista = connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','gastos')
        list_gastos = lista[0]  
        df_gastos = pd.DataFrame(list_gastos[1:], columns= list_gastos[0], index = None)
        df_gastos['Costo'] = pd.to_numeric(df_gastos['Costo'], downcast="integer")
        df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'],format="%d/%m/%Y, %H:%M:%S",errors='coerce')
        df_gastos['fecha'] = df_gastos['fecha'].dt.strftime('%d-%m-%Y, %H:%M')
        df_gastos.loc[:, 'Precio'] ='$'+ df_gastos['Costo'].map('{:,.0f}'.format)
        dff =df_gastos[['Gasto', 'Precio', 'Tipo','pago' ,'fecha']]
        st.dataframe(dff)
        st.download_button(label='📥 Descargar DATAFRAME GENERADO', data=to_excel(df_gastos) ,file_name= "df_gastos.xlsx")
        
if selected == "Ingresos":
    st.write("Ingrese ingreso de dinero nuevo")
    lista_persona = ["Carlos","Henry A","Marlenciaga","Davidcito"]
    lista_persona.insert(0, "-")
    lista_medios = ["Efectivo","Consignacion Bancolombia","Consignacion Davivienda"]
    lista_medios.insert(0, "-")
    if st.checkbox("Agregar ingreso"):
        
        col1, col2, col3, col4= st.columns(4)
        with col1:
            ingreso = st.text_input('Ingreso',"-")
        with col2:
            costo = st.text_input('Costo',"-")
        with col3:
            persona=st.selectbox("Persona", ((lista_persona)))
        with col4:
            medio=st.selectbox("Medio", ((lista_medios)))
            
        if st.button("Agregue registro"):
            if persona == "-" or ingreso == "-" or costo == "-":
                st.error('Por favor ingrese datos')
            else:
                connection = Conexion_google_sheets()
                lista= connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','ingresos')
                now = datetime.now()
                gs = lista[1]
                df = pd.DataFrame({'Ingreso': [ingreso], 'Costo':[float(costo)], 'Persona': [persona], 'Medio': [medio],'fecha':[now.strftime("%d/%m/%Y, %H:%M:%S")]})
                gs.values_append('ingresos', {'valueInputOption': 'RAW'}, {'values': df.values.tolist()})
                st.success('Registro insertado')

    if st.checkbox("Ver tabla"):
        connection = Conexion_google_sheets()
        lista = connection.conexion_sheets('1Zf73U-ERuCjlRe13_APyY7sCjzXzZX6kVaXJfU51gdI','ingresos')
        list_gastos = lista[0]  
        df_gastos = pd.DataFrame(list_gastos[1:], columns= list_gastos[0], index = None)
        df_gastos['Costo'] = pd.to_numeric(df_gastos['Costo'], downcast="integer")
        df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'],format="%d/%m/%Y, %H:%M:%S",errors='coerce')
        df_gastos['fecha'] = df_gastos['fecha'].dt.strftime('%d-%m-%Y, %H:%M')
        df_gastos.loc[:, 'Precio'] ='$'+ df_gastos['Costo'].map('{:,.0f}'.format)
        dff =df_gastos[['Ingreso', 'Precio', 'Persona','Medio','fecha']]
        st.dataframe(dff)
        st.download_button(label='📥 Descargar DATAFRAME GENERADO', data=to_excel(df_gastos) ,file_name= "df_gastos.xlsx")




    

