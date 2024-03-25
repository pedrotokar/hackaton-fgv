import pandas as pd
from numpy import nan
import pandas_gbq
import matplotlib as mpl
import pydeck as pdk
import json
import datetime

import streamlit as st

query = """SELECT *
    FROM datario.adm_cor_comando.ocorrencias
    WHERE data_particao > DATE("2023-06-01")""" # Coloquei um limite pra não gastar 3GB do google quando for puxar
chamados_rjcor = pandas_gbq.read_gbq(query, project_id = "hackaton-fgv")
#chamados_rjcor.to_csv("rjcor.csv")
#chamados_rjcor = pd.read_csv("rjcor.csv")

chamados_rjcor["data_inicio"] = pd.to_datetime(chamados_rjcor["data_inicio"])
chamados_rjcor["data_inicio_string"] = chamados_rjcor.apply(lambda linha: linha["data_inicio"].strftime("%d/%m/%Y, %H:%M:%S"), axis=1)

chamados_rjcor["gravidade"].value_counts(dropna = False)


gravidades = {
    "Normal": [100, 255, 0],
    "Média": [255, 200, 0],
    "Alta": [255, 0, 0],
    None: [200, 200, 200],
    "nan": [200, 200, 200],
    "Baixo": [255, 255, 0],
    "Medio": [255, 200, 0],
    "Alto": [255, 0, 0]
}
def aplica_cores(linha):
    if linha["status"] == "Fechado":
        return [0, 255, 0]
    else:
        return gravidades[linha["gravidade"]]
chamados_rjcor["coloracao"] = chamados_rjcor.apply(aplica_cores, axis=1)



camera_inicial = pdk.ViewState(
    latitude = -22.9035, 
    longitude = -43.4096, 
    zoom = 9.3, 
    max_zoom = 16, 
    pitch = 0, 
    bearing = 0
)

base = pdk.Layer(
    "PolygonLayer",
    stroked = False,
    get_polygon = "-",
    get_fill_color = [0, 0, 0, 20],
)

ocorrencias_acontecendo = pdk.Layer(
    "ScatterplotLayer",
    chamados_rjcor[["latitude", "longitude", "coloracao", "bairro", "data_inicio_string", 
        "gravidade", "descricao", "status"]][chamados_rjcor["status"] == "Aberto"],
    get_position = ["longitude", "latitude"],
    auto_highlight = True,
    get_radius = "200",
    get_fill_color = "coloracao",
    pickable = True
)

ocorrencias_fechadas = pdk.Layer(
    "ScatterplotLayer",
    chamados_rjcor[["latitude", "longitude", "coloracao", "bairro", "data_inicio_string", 
        "gravidade", "descricao", "status"]][chamados_rjcor["status"] == "Fechado"],
    get_position = ["longitude", "latitude"],
    auto_highlight = True,
    get_radius = "100",
    get_fill_color = "coloracao",
    pickable = True
)

r = pdk.Deck(
    layers = [base, ocorrencias_acontecendo], 
    initial_view_state = camera_inicial,
    tooltip = {"html": "<b>Bairro:</b> {bairro}<br><b>Data de inicio:</b> {data_inicio_string}"\
               "<br><b>Gravidade:</b> {gravidade}<br><b>Endereço:</b> {descricao}"\
               "<br><b>Situação:</b> {status}",
               "style": {
                  "backgroundColor": "steelblue",
                  "color": "white"
                        }
              },
    map_style = "dark_no_labels"
)

st.pydeck_chart(r)