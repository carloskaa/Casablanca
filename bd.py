    # -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 22:44:16 2023

@author: Carlos Camilo Caro Mora
"""

from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from io import BytesIO
from Clases import Conexion_google_sheets
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Casablanca",page_icon=Image.open("Logo.ico"),layout="centered")
st.markdown("<h1 style='color: black; text-align: center;'>REGISTROS CASABLANCA MUEBLES</h1>", unsafe_allow_html=True)


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
    st.markdown(
    """
    <style>
    .reportview-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .css-1aumxhk {
        max-width: 80%;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
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
    

# chart = alt.Chart(gastostipo).mark_bar().encode(
#     x=alt.X('Tipo', title='Tipo de gasto'),
#     y=alt.Y('Costo', title='Gastos totales por tipo'),
#     color=alt.Color('Tipo', scale=alt.Scale(scheme='tableau10')),
#     tooltip=['Tipo', 'Costo'])
# st.altair_chart(chart2, use_container_width=True)  
    

    option = st.selectbox('GRAFICOS DE GASTOS',('FORMA EN QUE SE REALIZO EL GASTO', 'TIPO DE GASTO'))
    if option == 'FORMA EN QUE SE REALIZO EL GASTO':
        gastospago = pd.pivot_table(df_gastos, values='Costo', columns=['pago'], aggfunc=sum)
        gastospago = gastospago.transpose()
        gastospago = gastospago.reset_index()
        fig = px.bar(gastospago, x='pago', y='Costo', color='pago')
        fig.update_layout(title="Gastos acumulados por tipo", title_x=0.5, height=600, width=800)
        st.plotly_chart(fig)

    elif option ==  'TIPO DE GASTO':
        gastostipo = pd.pivot_table(df_gastos, values='Costo', columns=['Tipo'], aggfunc=sum)
        gastostipo = gastostipo.transpose()
        gastostipo = gastostipo.reset_index()
        fig = px.bar(gastostipo, x='Tipo', y='Costo', color='Tipo')
        fig.update_layout(title="Gastos acumulados por tipo de pago", title_x=0.5, height=600, width=800)
        st.plotly_chart(fig)

    option2 = st.selectbox('GRAFICOS DE INGRESOS',('FORMA EN QUE SE REALIZO EL INGRESO', 'TIPO DE INGRESO'))
    if option2 == 'FORMA EN QUE SE REALIZO EL INGRESO':
        ingresotipo = pd.pivot_table(df_ingreso, values='Costo', columns=["Medio"], aggfunc=sum)
        ingresotipo = ingresotipo.transpose()
        ingresotipo = ingresotipo.reset_index()
        fig = px.bar(ingresotipo, x='Medio', y='Costo', color='Medio')
        fig.update_layout(title="Ingresos acumulados por tipo de pago", title_x=0.5, height=600, width=800)
        st.plotly_chart(fig)
    elif option2 =='TIPO DE INGRESO':
        ingresopago = pd.pivot_table(df_ingreso, values='Costo', columns=["Persona"], aggfunc=sum)
        ingresopago = ingresopago.transpose()
        ingresopago = ingresopago.reset_index()
        fig = px.bar(ingresopago, x='Persona', y='Costo', color='Persona')
        fig.update_layout(title="Ingresos acumulados por tipo de pago", title_x=0.5, height=600, width=800)
        st.plotly_chart(fig)
    
    lin_gastos = pd.pivot_table(df_gastos, values='Costo', columns=['fecha'], aggfunc=sum)
    lin_gastos  = lin_gastos.transpose()
    lin_gastos  = lin_gastos.reset_index()
    lin_ingresos = pd.pivot_table(df_ingreso, values='Costo', columns=['fecha'], aggfunc=sum)
    lin_ingresos = lin_ingresos.transpose()
    lin_ingresos = lin_ingresos.reset_index()

    lin_gastos = lin_gastos.sort_values('fecha')
    lin_gastos = lin_gastos.rename(columns={'Costo': 'gasto'})

    lin_ingresos = lin_ingresos.sort_values('fecha')
    lin_ingresos= lin_ingresos.rename(columns={'Costo': 'ingreso'})

    df_linea = pd.DataFrame({'fecha': pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')})
    df_linea2 = pd.DataFrame({'fecha': pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')})
    lin_gastos['fecha'] = pd.to_datetime(lin_gastos['fecha']).dt.date
    lin_gastos['fecha'] = pd.to_datetime(lin_gastos['fecha'])
    df_linea  = pd.merge(df_linea , lin_gastos, on='fecha', how='left')
    df_linea['gasto'] = df_linea['gasto'].fillna(0)
    df_linea['gastos_acumulados'] = df_linea['gasto'].cumsum()
    df_linea['gastos_acumulados'] = df_linea['gastos_acumulados'].fillna(0)

    lin_ingresos['fecha'] = pd.to_datetime(lin_ingresos['fecha']).dt.date
    lin_ingresos['fecha'] = pd.to_datetime(lin_ingresos['fecha'])
    df_linea2  = pd.merge(df_linea2 , lin_ingresos, on='fecha', how='left')
    df_linea2['ingreso'] = df_linea2['ingreso'].fillna(0)
    df_linea2['ingresos_acumulados'] = df_linea2['ingreso'].cumsum()
    df_linea2['ingresos_acumulados'] = df_linea2['ingresos_acumulados'].fillna(0)

    df_linea  = pd.merge(df_linea , df_linea2, on='fecha', how='left')

    fecha_minima = df_linea['fecha'].min().date()
    fecha_maxima = df_linea['fecha'].max().date()
    fecha_minima2 = df_linea['fecha'][(df_linea['ingresos_acumulados']!=0)|(df_linea['gastos_acumulados']!=0)].min().date()
    fecha_maxima2 = df_linea['fecha'][-(df_linea['ingreso']==0)&(df_linea['gasto']==0)].max().date()
    fecha_seleccionada = st.slider('Selecciona un rango de fechas', fecha_minima, fecha_maxima, (fecha_minima2, fecha_maxima2))
    df_linea = df_linea[(df_linea['fecha'].dt.date >= fecha_seleccionada[0]) & (df_linea['fecha'].dt.date <= fecha_seleccionada[1])]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_linea['fecha'], y=df_linea['ingresos_acumulados'], name='ingresos_acumulados'))
    fig.add_trace(go.Scatter(x=df_linea['fecha'], y=df_linea['gastos_acumulados'], name='gastos_acumulados'))
    fig.add_trace(go.Bar(x=df_linea['fecha'], y=df_linea['ingreso'], name='ingreso'))
    fig.add_trace(go.Bar(x=df_linea['fecha'], y=df_linea['gasto'], name='gasto'))
    st.plotly_chart(fig)

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
    st.write("Ingrese de dinero nuevo")
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




    

