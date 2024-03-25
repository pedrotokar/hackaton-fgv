import pandas as pd
from numpy import nan
import pandas_gbq
import matplotlib as mpl
import pydeck as pdk
import json

import streamlit as st

query = """SELECT *
    FROM datario.adm_central_atendimento_1746.chamado
    WHERE tipo in ('Drenagem e Saneamento', 'Alagamento','Drenagem ou Esgoto','Esgoto')
    AND subtipo NOT LIKE 'Reposição%' AND subtipo NOT LIKE 'Renivelamento%' 
    AND subtipo NOT LIKE '%Zona Oeste Mais Saneamento%' AND subtipo NOT LIKE '%CEDAE' 
    AND data_particao > DATE("2023-06-01")""" # Coloquei um limite pra não gastar 3GB do google quando for puxar

@st.cache_data
def get_data(query, project_id):
     
    data = pandas_gbq.read_gbq(query, project_id = "hackaton-fgv")
    # data.to_csv("chamados_1746.csv")

    return data

chamados_1746 = get_data(query, "hackaton-fgv")
#chamados_1746 = pd.read_csv("chamados_1746.csv") # Num ambiente de produção nós puxariamos na hora mas esse n é o caso pq isso é pra demonstrar apenas


chamados_1746["id_bairro"] = pd.to_numeric(chamados_1746["id_bairro"]) #Fazendo isso pq volta como string

chamados_por_bairro = chamados_1746["id_bairro"].value_counts(dropna = False)

with open("dados/Limite_de_Bairros.geojson","r") as f:
    bairros_rj = json.load(f)
for item in bairros_rj["features"]:
    try:
        item["properties"]["contagem_1746"] = int(chamados_por_bairro[item["properties"]["codbnum"]])
    except KeyError:
        item["properties"]["contagem_1746"] = 0
    item["properties"]["área"] = f"{(item['properties']['área']/1000000):2f}"

chamados_1746.groupby("id_bairro")["dentro_prazo"].value_counts()

cores = mpl.colormaps["Reds"].resampled(256)
contagem_max = max([bairro["properties"]["contagem_1746"] for bairro in bairros_rj["features"]])
for item in bairros_rj["features"]:
        item["properties"]["coloracao_1746"] = list(cores(item["properties"]["contagem_1746"]/contagem_max)[0:3])
        item["properties"]["coloracao_1746"][0] *= 255
        item["properties"]["coloracao_1746"][1] *= 255
        item["properties"]["coloracao_1746"][2] *= 255

query = """SELECT *
    FROM datario.adm_cor_comando.ocorrencias
    WHERE data_particao > DATE("2023-06-01")""" # Coloquei um limite pra não gastar 3GB do google quando for puxar

# chamados_rjcor = pandas_gbq.read_gbq(query, project_id = "hackaton-fgv")
# chamados_rjcor.to_csv("rjcor.csv")
#chamados_rjcor = pd.read_csv("rjcor.csv")

chamados_rjcor = get_data(query, "hackaton-fgv")

corrige_bairros = {
    "FAZENDA BOTAFOGO": "ACARI",
    "AV. DAS AMÉRICAS": "BARRA DA TIJUCA",
    "B TIJUCA": "BARRA DA TIJUCA",
    "BARRA": "BARRA DA TIJUCA",
    ". DAS AMÉRICAS": "BARRA DA TIJUCA",
    "BARRA GUARATIBA": "BARRA DE GUARATIBA",
    "CIDADE UNIVERSITÁRIA DA UNIVERSIDADE FEDERAL DO RIO DE JANEIRO": "CIDADE UNIVERSITÁRIA",
    "FUNDÃO": "CIDADE UNIVERSITÁRIA",
    "CIDADE ALTA": "CORDOVIL",
    "FREGUESIA (JACARÉPAGUA)": "FREGUESIA (JACAREPAGUÁ)",
    "FREGUESIA DE JACARÉPAGUÁ": "FREGUESIA (JACAREPAGUÁ)",
    "GALEAO": "GALEÃO",
    "GRAJAU": "GRAJAÚ",
    "HONORIO GURGEL": "HONÓRIO GURGEL",
    "INHAUMA": "INHAÚMA",
    "COLÔNIA": "JACAREPAGUÁ",
    "JARDIM AMERICA": "JARDIM AMÉRICA",
    "LARANJ": "LARANJEIRAS",
    "LARANJEIRAS ": "LARANJEIRAS",
    "MARACANÃ ": "MARACANÃ",
    "MAL. HERMES": "MARECHAL HERMES",
    "PARQUE UNIÃO": "MARÉ",
    "OSWALDO CRUZ": "OSVALDO CRUZ",
    "OSWALDO CRUZ ": "OSVALDO CRUZ",
    "PACIENCIA": "PACIÊNCIA",
    "PRACA DA BANDEIRA": "PRAÇA DA BANDEIRA",
    "QUINTINO BOCAIUVA": "QUINTINO BOCAIÚVA",
    "RECREIO ": "RECREIO DOS BANDEIRANTES",
    "REC. BANDEIRANT": "RECREIO DOS BANDEIRANTES",
    "STA TERESA": "SANTA TERESA",
    "SEN. VASCONCELOS": "SENADOR VASCONCELOS",
    "ALT. VILA KENNEDY": "VILA KENNEDY",
    "VILA COSMOS": "VILA KOSMOS"
}

def arruma_nomes(linha):
    if type(linha) == str:
        try:
            return corrige_bairros[linha.upper()]
        except KeyError:
            return linha.upper()
        
contagem_rjcor = chamados_rjcor["bairro"].apply(arruma_nomes).value_counts()
contagem_rjcor

for item in bairros_rj["features"]:
    try:
        item["properties"]["contagem_rjcor"] = int(contagem_rjcor[item["properties"]["nome"].upper()])
    except KeyError:
        item["properties"]["contagem_rjcor"] = 0

cores = mpl.colormaps["Blues"].resampled(256)
contagem_max = max([bairro["properties"]["contagem_rjcor"] for bairro in bairros_rj["features"]])
for item in bairros_rj["features"]:
        item["properties"]["coloracao_rjcor"] = list(cores(item["properties"]["contagem_rjcor"]/contagem_max)[0:3])
        item["properties"]["coloracao_rjcor"][0] *= 255
        item["properties"]["coloracao_rjcor"][1] *= 255
        item["properties"]["coloracao_rjcor"][2] *= 255

camera_inicial = pdk.ViewState(
    latitude = -22.9035, 
    longitude = -43.4096, 
    zoom = 9.3, 
    max_zoom = 16, 
    pitch = 30, 
    bearing = 0
)

base = pdk.Layer(
    "PolygonLayer",
    stroked = False,
    get_polygon = "-",
    get_fill_color = [0, 0, 0, 20],
)

bairros_rjcor = pdk.Layer(
    "GeoJsonLayer",
    bairros_rj,
    opacity = 0.6,
    stroked = False,
    filled = True,
    extruded = True,
    wireframe = True,
    pickable = True,
    get_elevation = "properties.contagem_rjcor",
    get_fill_color = "properties.coloracao_rjcor",
    get_line_color = [0, 0, 0],
)

bairros_1746 = pdk.Layer(
    "GeoJsonLayer",
    bairros_rj,
    opacity = 0.6,
    stroked = False,
    filled = True,
    extruded = True,
    wireframe = True,
    pickable = True,
    get_elevation = "properties.contagem_1746",
    get_fill_color = "properties.coloracao_1746",
    get_line_color = [0, 0, 0],
)

mapa = pdk.Deck(
    layers = [base, bairros_1746], 
    initial_view_state = camera_inicial, 
    tooltip = {"html": "<b>Bairro:</b> {properties.nome}<br><b>Ocorrencias RJCOR:</b> {properties.contagem_rjcor}"\
               "<br><b>Chamados 1746: </b> {properties.contagem_1746}<br><b>Área:</b> {properties.área} km²",
               "style": {
                  "backgroundColor": "steelblue",
                  "color": "white"
                        }
              },
    map_style = "dark"
)

st.pydeck_chart(mapa)