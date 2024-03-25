import pandas as pd
from numpy import nan
import pandas_gbq
import matplotlib as mpl
import pydeck as pdk
import json

import streamlit as st
from datetime import date

from default import default_style

default_style()

st.write("""
        # Ocorrências do Centro de Operações Rio (COR)
         
        A visualização abaixo apresenta um mapa interativo que permite a análise comparativa da distribuição geográfica de chamados de dois sistemas distintos de atendimento a ocorrências na cidade do Rio de Janeiro: o sistema 1746 e o sistema RJcor. Isso pode ser crucial para identificar padrões de demanda, áreas com maior incidência de problemas e disparidades no atendimento entre diferentes regiões, fornecendo insights valiosos para melhorias nos serviços municipais e no planejamento urbano.
        """)

def retorna_query_1746(data):
    return f"""SELECT *
    FROM datario.adm_central_atendimento_1746.chamado
    WHERE tipo in ('Drenagem e Saneamento', 'Alagamento','Drenagem ou Esgoto','Esgoto')
    AND subtipo NOT LIKE 'Reposição%' AND subtipo NOT LIKE 'Renivelamento%'
    AND subtipo NOT LIKE '%Zona Oeste Mais Saneamento%' AND subtipo NOT LIKE '%CEDAE'
    AND data_particao > DATE("{data}")"""

def retorna_query_rjcor(data):
    return f"""SELECT *
    FROM datario.adm_cor_comando.ocorrencias
    WHERE data_particao > DATE("{data}")"""

def monta_layer_1746(dados):
    return pdk.Layer(
    "GeoJsonLayer",
    dados,
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

def monta_layer_rjcor(dados):
    return pdk.Layer(
    "GeoJsonLayer",
    dados,
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

@st.cache_data
def get_data(query, project_id):
     
    data = pandas_gbq.read_gbq(query, project_id = "hackaton-fgv")
    # data.to_csv("chamados_1746.csv")

    return data

def retorna_dados_pela_data(data):
    query_1746 = retorna_query_1746(data)
    query_rjcor = retorna_query_rjcor(data)
    chamados_1746 = get_data(query_1746, "hackaton-fgv")
    chamados_rjcor = get_data(query_rjcor, "hackaton-fgv")
    with open("dados/Limite_de_Bairros.geojson","r") as f:
        bairros_rj = json.load(f)

    chamados_1746["id_bairro"] = pd.to_numeric(chamados_1746["id_bairro"]) #Fazendo isso pq volta como string
    chamados_por_bairro_1746 = chamados_1746["id_bairro"].value_counts(dropna = False)

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
    chamados_por_bairro_rjcor = chamados_rjcor["bairro"].apply(arruma_nomes).value_counts()

    for item in bairros_rj["features"]:
        try:
            item["properties"]["contagem_1746"] = int(chamados_por_bairro_1746[item["properties"]["codbnum"]])
        except KeyError:
            item["properties"]["contagem_1746"] = 0
        try:
            item["properties"]["contagem_rjcor"] = int(chamados_por_bairro_rjcor[item["properties"]["nome"].upper()])
        except KeyError:
            item["properties"]["contagem_rjcor"] = 0
        item["properties"]["área"] = f"{(item['properties']['área']/1000000):2f}"

    cores = mpl.colormaps["Reds"].resampled(256)
    contagem_max = max([bairro["properties"]["contagem_1746"] for bairro in bairros_rj["features"]])
    for item in bairros_rj["features"]:
            item["properties"]["coloracao_1746"] = list(cores(item["properties"]["contagem_1746"]/contagem_max)[0:3])
            item["properties"]["coloracao_1746"][0] *= 255
            item["properties"]["coloracao_1746"][1] *= 255
            item["properties"]["coloracao_1746"][2] *= 255


    cores = mpl.colormaps["Blues"].resampled(256)
    contagem_max = max([bairro["properties"]["contagem_rjcor"] for bairro in bairros_rj["features"]])
    for item in bairros_rj["features"]:
            item["properties"]["coloracao_rjcor"] = list(cores(item["properties"]["contagem_rjcor"]/contagem_max)[0:3])
            item["properties"]["coloracao_rjcor"][0] *= 255
            item["properties"]["coloracao_rjcor"][1] *= 255
            item["properties"]["coloracao_rjcor"][2] *= 255

    return bairros_rj

def monta_mapa(layers):
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

    mapa = pdk.Deck(
        layers = [base, *layers],
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
    return mapa

data = st.date_input("A partir de", value = date(2024, 1, 1), min_value = date(2014, 1, 1), max_value = date.today(), format="DD/MM/YYYY")

dados = retorna_dados_pela_data(data.strftime("%Y-%m-%d"))

selecionados = st.radio("Selecione o tipo de chamado para ver os dados", ["Chamados 1746", "Chamados RJcor"])
layer = []
if "Chamados 1746" in selecionados:
    layer.append(monta_layer_1746(dados))
if "Chamados RJcor" in selecionados:
    layer.append(monta_layer_rjcor(dados))

mapa = monta_mapa([layer])

st.pydeck_chart(mapa)
