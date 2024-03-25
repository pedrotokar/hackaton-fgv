import pandas as pd
import pandas_gbq
import geopandas as gpd
import rtree
import pygeos
import mapclassify
from shapely.geometry import Point
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import folium
from folium import plugins
from core.scripts import get_data
from streamlit_folium import st_folium

import streamlit as st

from default import default_style

default_style()

st.write("""
        # Monitoramento de Chuvas no Rio de Janeiro
         
         A visualização acima apresenta um mapa interativo que exibe diferentes estações de monitoramento de chuvas em cores distintas, permitindo uma análise espacial das precipitações em tempo real provenientes de diferentes fontes, como WEBSIRENE, Alertário, INEA e CEMADEN. Essa visão integrada é essencial para entender a distribuição das chuvas na região e auxiliar na tomada de decisões em situações de risco, como prevenção de enchentes e deslizamentos de terra.
        """)

query_inea = """
        WITH mais_recentes AS (
        SELECT id_estacao, MAX(data_medicao) AS data_mais_recente
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_inea
        GROUP BY id_estacao
        )
        SELECT t.*
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_inea t
        JOIN mais_recentes m
        ON t.id_estacao = m.id_estacao AND t.data_medicao = m.data_mais_recente;
        """

query_cemaden = """
        WITH mais_recentes AS (
        SELECT id_estacao, MAX(data_medicao) AS data_mais_recente
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_cemaden
        GROUP BY id_estacao
        )

        SELECT t.*
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_cemaden t
        JOIN mais_recentes m
        ON t.id_estacao = m.id_estacao AND t.data_medicao = m.data_mais_recente;
        """

query_websirene = """
        WITH mais_recentes AS (
        SELECT id_estacao, MAX(primary_key) AS data_mais_recente
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_websirene
        GROUP BY id_estacao
        )

        SELECT t.*
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_websirene t
        JOIN mais_recentes m
        ON t.id_estacao = m.id_estacao AND t.primary_key = m.data_mais_recente;
        """

query_alertario = """
        WITH mais_recentes AS (
        SELECT id_estacao, MAX(data_medicao) AS data_mais_recente
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_alertario_5min
        GROUP BY id_estacao
        )

        SELECT DISTINCT t.*
        FROM rj-cor.clima_pluviometro.taxa_precipitacao_alertario_5min t
        JOIN mais_recentes m
        ON t.id_estacao = m.id_estacao AND t.data_medicao = m.data_mais_recente;
        """

# Organizando os datasets
# INEA

st.write("""
        #
         
        """)


result_dataframe_inea = get_data(query_inea, project_id = "hackaton-fgv")
result_dataframe_inea['id_estacao'] = result_dataframe_inea['id_estacao'].astype(str)

df_inea = pd.read_csv('dados/tabelas/df_inea.csv')
df_inea['id_estacao'] = df_inea['id_estacao'].astype(str)
df_inea = pd.merge(df_inea, result_dataframe_inea, on='id_estacao', how='left')

novas_colunas_inea = ['acumulado_chuva_15_min', 'acumulado_chuva_1_h', 'acumulado_chuva_24_h']
for coluna in novas_colunas_inea:
    df_inea[coluna] = df_inea[coluna].apply(lambda x: str(x) + ' mm' if pd.notna(x) else x)
df_inea[novas_colunas_inea] = df_inea[novas_colunas_inea].fillna('Não há dados')

# WEBSIRENE
result_dataframe_websirene = get_data(query_websirene, project_id = "hackaton-fgv")
result_dataframe_websirene['id_estacao'] = result_dataframe_websirene['id_estacao'].astype(str)
df_websirene = pd.read_csv('dados/tabelas/df_websirene.csv')
df_websirene['id_estacao'] = df_websirene['id_estacao'].astype(str)
df_websirene = pd.merge(df_websirene, result_dataframe_websirene, on='id_estacao', how='left')
novas_colunas_websirene = ['acumulado_chuva_15_min', 'acumulado_chuva_1_h', 'acumulado_chuva_24_h']
for coluna in novas_colunas_websirene:
    df_websirene[coluna] = df_websirene[coluna].apply(lambda x: str(x) + ' mm' if pd.notna(x) else x)
df_websirene[novas_colunas_websirene] = df_websirene[novas_colunas_websirene].fillna('Não há dados')

# ALERTÁRIO
result_dataframe_alertario = get_data(query_alertario, project_id = "hackaton-fgv")
result_dataframe_alertario['id_estacao'] = result_dataframe_alertario['id_estacao'].astype(str)
df_alertario = pd.read_csv('dados/tabelas/df_alertario.csv')
df_alertario['id_estacao'] = df_alertario['id_estacao'].astype(str)
df_alertario = pd.merge(df_alertario, result_dataframe_alertario, on='id_estacao', how='left')
novas_colunas_alertario = ['acumulado_chuva_5min', 'acumulado_chuva_1h', 'acumulado_chuva_24h']
for coluna in novas_colunas_alertario:
    df_alertario[coluna] = df_alertario[coluna].apply(lambda x: str(x) + ' mm' if pd.notna(x) else x)
df_alertario[novas_colunas_alertario] = df_alertario[novas_colunas_alertario].fillna('Não há dados')

# CEMADEN
result_dataframe_cemaden = get_data(query_cemaden, project_id = "hackaton-fgv")
result_dataframe_cemaden['id_estacao'] = result_dataframe_cemaden['id_estacao'].astype(str)
df_cemaden = pd.read_csv('dados/tabelas/df_cemaden.csv')
df_cemaden['id_estacao'] = df_cemaden['id_estacao'].astype(str)
df_cemaden = pd.merge(df_cemaden, result_dataframe_cemaden, on='id_estacao', how='left')
novas_colunas_cemaden = ['acumulado_chuva_10_min', 'acumulado_chuva_1_h', 'acumulado_chuva_24_h']
for coluna in novas_colunas_cemaden:
    df_cemaden[coluna] = df_cemaden[coluna].apply(lambda x: str(x) + ' mm' if pd.notna(x) else x)
df_cemaden[novas_colunas_cemaden] = df_cemaden[novas_colunas_cemaden].fillna('Não há dados')


# Datasets com as coordenadas
geometry_websirene = [Point(lon, lat) for lon, lat in zip(df_websirene['longitude'], df_websirene['latitude'])]
gdf_websirene = gpd.GeoDataFrame(df_websirene, geometry = geometry_websirene, crs = 'EPSG:4326')

geometry_alertario = [Point(lon, lat) for lon, lat in zip(df_alertario['longitude'], df_alertario['latitude'])]
gdf_alertario = gpd.GeoDataFrame(df_alertario, geometry = geometry_alertario, crs = 'EPSG:4326')

geometry_inea = [Point(lon, lat) for lon, lat in zip(df_inea['longitude'], df_inea['latitude'])]
gdf_inea = gpd.GeoDataFrame(df_inea, geometry = geometry_inea, crs = 'EPSG:4326')

geometry_cemaden = [Point(lon, lat) for lon, lat in zip(df_cemaden['longitude'], df_cemaden['latitude'])]
gdf_cemaden = gpd.GeoDataFrame(df_cemaden, geometry = geometry_cemaden, crs = 'EPSG:4326')

# Criando um mapa interativo com Folium
m = folium.Map(location=[-22.9068, -43.1729], zoom_start=10)

# Adicionando pontos ao mapa
for idx, row in gdf_websirene.iterrows():
    popup_text = f"<div style='white-space: nowrap;'><b>{row['estacao'].title()}</b><br>"
    popup_text += f"Acumulado de chuva (10 min): {row[novas_colunas_websirene[0]]}<br>"
    popup_text += f"Acumulado de chuva (1 hora): {row[novas_colunas_websirene[1]]}<br>"
    popup_text += f"Acumulado de chuva (1 dia): {row[novas_colunas_websirene[2]]}<br>"
    popup_text += "</div>"
    folium.Marker([row['latitude'], row['longitude']], popup=popup_text, icon=folium.Icon(color='blue')).add_to(m)

for idx, row in gdf_alertario.iterrows():
    popup_text = f"<div style='white-space: nowrap;'><b>{row['estacao'].title()}</b><br>"
    popup_text += f"Acumulado de chuva (10 min): {row[novas_colunas_alertario[0]]}<br>"
    popup_text += f"Acumulado de chuva (1 hora): {row[novas_colunas_alertario[1]]}<br>"
    popup_text += f"Acumulado de chuva (1 dia): {row[novas_colunas_alertario[2]]}<br>"
    popup_text += "</div>"
    folium.Marker([row['latitude'], row['longitude']], popup=popup_text, icon=folium.Icon(color='red')).add_to(m)

for idx, row in gdf_inea.iterrows():
    popup_text = f"<div style='white-space: nowrap;'><b>{row['estacao'].title()}</b><br>"
    popup_text += f"Acumulado de chuva (10 min): {row[novas_colunas_inea[0]]}<br>"
    popup_text += f"Acumulado de chuva (1 hora): {row[novas_colunas_inea[1]]}<br>"
    popup_text += f"Acumulado de chuva (1 dia): {row[novas_colunas_inea[2]]}<br>"
    popup_text += "</div>"
    folium.Marker([row['latitude'], row['longitude']], popup=popup_text, icon=folium.Icon(color='orange')).add_to(m)

for idx, row in gdf_cemaden.iterrows():
    popup_text = f"<div style='white-space: nowrap;'><b>{row['estacao'].title()}</b><br>"
    popup_text += f"Acumulado de chuva (10 min): {row[novas_colunas_cemaden[0]]}<br>"
    popup_text += f"Acumulado de chuva (1 hora): {row[novas_colunas_cemaden[1]]}<br>"
    popup_text += f"Acumulado de chuva (1 dia): {row[novas_colunas_cemaden[2]]}<br>"
    popup_text += "</div>"
    folium.Marker([row['latitude'], row['longitude']], popup=popup_text, icon=folium.Icon(color='green')).add_to(m)

legend_html = '''
    <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; font-size: 16px; background-color: rgba(255, 255, 255, 0.8); padding: 10px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);">
        <p style="margin-bottom: 5px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: blue; border-radius: 3px; margin-right: 5px;"></span><span style="font-weight: bold; color: blue;">Websirene</span></p>
        <p style="margin-bottom: 5px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: red; border-radius: 3px; margin-right: 5px;"></span><span style="font-weight: bold; color: red;">Alertário</span></p>
        <p style="margin-bottom: 5px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: orange; border-radius: 3px; margin-right: 5px;"></span><span style="font-weight: bold; color: orange;">INEA</span></p>
        <p style="margin-bottom: 0;"><span style="display: inline-block; width: 15px; height: 15px; background-color: green; border-radius: 3px; margin-right: 5px;"></span><span style="font-weight: bold; color: green;">CEMADEN</span></p>
    </div>

     '''

m.get_root().html.add_child(folium.Element(legend_html))
st.markdown(legend_html, unsafe_allow_html=True)
st_folium(m, width=1000)

