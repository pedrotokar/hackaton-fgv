import pandas as pd
from numpy import nan
import pandas_gbq
import altair as alt
import matplotlib as mpl
import pydeck as pdk
import json
import streamlit as st

from default import default_style

default_style()

st.write("""
         # Pontos críticos de alagamento e drenagem do Rio de Janeiro
         
         A visualização abaixo apresenta um mapa interativo que permite a análise dos pontos críticos de alagamento e drenagem da cidade do Rio de Janeiro. Através da identificação desses pontos, é possível planejar ações preventivas e de resposta a eventos como inundações, contribuindo para a proteção da população e dos recursos urbanos.
         """)

import streamlit as st

query = """SELECT *
FROM rj-rioaguas.saneamento_drenagem.ponto_supervisionado_alagamento"""

dados_drenagem = pandas_gbq.read_gbq(query, project_id = "hackaton-fgv")
dados_drenagem[dados_drenagem["classe"] == "Ponto observado"]["eliminado"].value_counts()

classes = {
    "Ponto critico": [0, 0, 190],
    "Ponto monitorado": [0, 255, 0],
    "Ponto observado": [100, 100, 255]
}
dados_drenagem["coloracao"] = dados_drenagem.apply(lambda linha: classes[linha["classe"]], axis=1)

def arruma_descricao(linha):
    if linha["causa_alagamento"] == " " or linha["causa_alagamento"] is None:
        return "Não foi fornecida descrição para esse ponto"
    else:
        return linha["causa_alagamento"]
dados_drenagem["descricao"] = dados_drenagem.apply(arruma_descricao, axis=1)

def arruma_medida(linha):
    if linha["medida_cor"] == "_" or linha["medida_cor"] is None:
        return "Não foi fornecida medida planejada ou tomada para esse ponto"
    else:
        return linha["medida_cor"]
dados_drenagem["medida"] = dados_drenagem.apply(arruma_medida, axis=1)

def arruma_resolvido(linha):
    if linha["eliminado"] == " " or linha["eliminado"] is None:
        return "Ainda não foi eliminado"
    else:
        return linha["eliminado"]
dados_drenagem["eliminado"] = dados_drenagem.apply(arruma_resolvido, axis=1)

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

drenagens_nao_resolvidas = pdk.Layer(
    "ScatterplotLayer",
    dados_drenagem[["latitude", "longitude", "coloracao", "endereco_ponto_supervisionado", "bairro",
        "sub_bacia_hidrografica", "medida", "descricao", "eliminado"]][(dados_drenagem["classe"] == "Ponto critico") | (dados_drenagem["classe"] == "Ponto observado")],
    get_position = ["longitude", "latitude"],
    auto_highlight = True,
    get_radius = 200,
    get_fill_color = "coloracao",
    pickable = True
)

drenagens_resolvidas = pdk.Layer(
    "ScatterplotLayer",
    dados_drenagem[["latitude", "longitude", "coloracao", "endereco_ponto_supervisionado", "bairro",
        "sub_bacia_hidrografica", "medida", "descricao", "eliminado"]][dados_drenagem["classe"] == "Ponto monitorado"],
    get_position = ["longitude", "latitude"],
    auto_highlight = True,
    get_radius = 200,
    get_fill_color = "coloracao",
    pickable = True
)

st.write("Selecione quais tipos de pontos você quer analisar.")
chamados_abertos = st.checkbox("Pontos observados e críticos (não foram resolvidos)")
chamados_fechados = st.checkbox("Pontos monitorados (já foram resolvidos)")
layer = []
if chamados_abertos:
    layer.append(drenagens_nao_resolvidas)
if chamados_fechados:
    layer.append(drenagens_resolvidas)

mapa = pdk.Deck(
    layers = [base, *layer],
    initial_view_state = camera_inicial,
    tooltip = {"html": "<b>Endereço:</b> {endereco_ponto_supervisionado} - {bairro}"\
               "<br><b>Sub bacia hidrografica:</b> {sub_bacia_hidrografica}<br>"\
               "<b>Descrição do ponto:</b> {descricao}<br><b>Medida planejada:</b> {medida}"\
               "<br><b>Eliminado em:</b> {eliminado}",
               "style": {
                  "backgroundColor": "steelblue",
                  "color": "white"
                        }
              },
    map_style = "light_no_labels"
)

st.pydeck_chart(mapa)
