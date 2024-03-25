import pandas as pd
from numpy import nan
import pandas_gbq
import matplotlib as mpl
import pydeck as pdk
import json
import datetime
from core.scripts import get_data

import streamlit as st

st.write("""
         # Ocorrências do Centro de Operações Rio (COR)

         O Centro de Operações Rio (COR) desempenha um papel vital na gestão de crises e tomada de decisões em situações de emergência na cidade do Rio de Janeiro, especialmente no contexto hidrológico. Integrando informações de diversas fontes e utilizando tecnologias avançadas de monitoramento, o COR fornece dados precisos e em tempo real sobre condições hidrológicas, permitindo ações preventivas e de resposta a eventos como inundações e deslizamentos, contribuindo assim para a proteção da vida e da propriedade dos cidadãos cariocas.
         """)


def retorna_query(data):
    return f"""SELECT *
    FROM datario.adm_cor_comando.ocorrencias
    WHERE data_particao > DATE("{data}")""" # Coloquei um limite pra não gastar 3GB do google quando for puxar

def retorna_dados_pela_data(data):
    query = retorna_query(data)
    chamados_rjcor = get_data(query, project_id = "hackaton-fgv")

    chamados_rjcor["data_inicio"] = pd.to_datetime(chamados_rjcor["data_inicio"])
    chamados_rjcor["data_inicio_string"] = chamados_rjcor.apply(lambda linha: linha["data_inicio"].strftime("%d/%m/%Y, %H:%M:%S"), axis=1)

    gravidades = {
        "Normal": [255, 255, 0],
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

    return chamados_rjcor

def monta_layer_abertos(dados):
     return pdk.Layer(
        "ScatterplotLayer",
        dados[["latitude", "longitude", "coloracao", "bairro", "data_inicio_string",
            "gravidade", "descricao", "status"]][dados["status"] == "Aberto"],
        get_position = ["longitude", "latitude"],
        auto_highlight = True,
        get_radius = "200",
        get_fill_color = "coloracao",
        pickable = True
    )

def monta_layer_fechados(dados):
    return pdk.Layer(
        "ScatterplotLayer",
        dados[["latitude", "longitude", "coloracao", "bairro", "data_inicio_string",
            "gravidade", "descricao", "status"]][dados["status"] == "Fechado"],
        get_position = ["longitude", "latitude"],
        auto_highlight = True,
        get_radius = "100",
        get_fill_color = "coloracao",
        pickable = True
    )

def monta_mapa(layers):
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

    return pdk.Deck(
    layers = [base,*layers],
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

dados = retorna_dados_pela_data("2023-06-01")
st.write("Selecione quais tipos de chamado você quer visualizar.")
chamados_abertos = st.checkbox("Chamados Abertos")
chamados_fechados = st.checkbox("Chamados fechados")
layer = []
if chamados_abertos:
    layer.append(monta_layer_abertos(dados))
if chamados_fechados:
    layer.append(monta_layer_fechados(dados))

mapa = monta_mapa(layer)

st.pydeck_chart(mapa)
