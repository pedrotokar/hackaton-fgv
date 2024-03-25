import pandas as pd
from numpy import nan
import pandas_gbq
import altair as alt
import matplotlib as mpl
import pydeck as pdk
import json

query = """SELECT *
    FROM rj-rioaguas.saneamento_drenagem.ponto_supervisionado_alagamento""" # Coloquei um limite pra não gastar 3GB do google quando for puxar
drenagem = pandas_gbq.read_gbq(query, project_id = "hackaton-fgv")


drenagem[drenagem["classe"] == "Ponto observado"]["eliminado"].value_counts()


classes = {
    "Ponto critico": [0, 0, 190],
    "Ponto monitorado": [0, 255, 0],
    "Ponto observado": [100, 100, 255]
}
drenagem["coloracao"] = drenagem.apply(lambda linha: classes[linha["classe"]], axis=1)


def arruma_descricao(linha):
    if linha["causa_alagamento"] == " " or linha["causa_alagamento"] is None:
        return "Não foi fornecida descrição para esse ponto"
    else:
        return linha["causa_alagamento"]
drenagem["descricao"] = drenagem.apply(arruma_descricao, axis=1)

def arruma_medida(linha):
    if linha["medida_cor"] == "_" or linha["medida_cor"] is None:
        return "Não foi fornecida medida planejada ou tomada para esse ponto"
    else:
        return linha["medida_cor"]
drenagem["medida"] = drenagem.apply(arruma_medida, axis=1)

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
    drenagem[["latitude", "longitude", "coloracao", "endereco_ponto_supervisionado", "bairro", 
        "sub_bacia_hidrografica", "medida", "descricao", "eliminado"]][drenagem["classe"] == "Ponto critico" | drenagem["classe"] == "Ponto observado"],
    get_position = ["longitude", "latitude"],
    auto_highlight = True,
    get_radius = 200,
    get_fill_color = "coloracao",
    pickable = True
)

drenagens_resolvidas = pdk.Layer(
    "ScatterplotLayer",
    drenagem[["latitude", "longitude", "coloracao", "endereco_ponto_supervisionado", "bairro", 
        "sub_bacia_hidrografica", "medida", "descricao", "eliminado"]][drenagem["classe"] == "Ponto monitorado"],
    get_position = ["longitude", "latitude"],
    auto_highlight = True,
    get_radius = 200,
    get_fill_color = "coloracao",
    pickable = True
)


mapa = pdk.Deck(
    layers = [base, drenagens], 
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
    map_style = "dark_no_labels"
)

mapa.to_html("geojson_layer.html")