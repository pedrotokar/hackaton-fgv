import pandas as pd
import plotly.express as px
import streamlit as st

from default import default_style

default_style()

st.write("""
        # Altura Máxima da Lâmina D'Água em Via por Dia

        Monitorar o nível da água em vias é fundamental por várias razões: garantir a segurança viária ao evitar acidentes causados por águas acumuladas, prevenir danos estruturais e erosão, prever e alertar sobre inundações, e facilitar o planejamento urbano sustentável. Essa prática é crucial para proteger vidas, propriedades e promover cidades resilientes diante de desafios hidrológicos.
        """)

df = pd.read_csv(r"dados/tabelas/lamina_agua_via.csv")

#df['data_hora'] = pd.to_datetime(df['data_particao'] + ' ' + df['horario'])

df = df.groupby('data_particao')['altura_agua'].max().reset_index()
df = df.sort_values(by="data_particao")

fig = px.line(df, x='data_particao', y='altura_agua')

fig.update_layout(title='Altura Máxima da Lâmina D\'Água em Via por Dia',
    xaxis_title='Data',
    yaxis_title='Altura Máxima da Água (mm)',
    legend_title='Estação',
    barmode='overlay',
    plot_bgcolor='white',
    template='ygridoff'
)

fig.update_xaxes(ticks='outside')

st.plotly_chart(fig)

st.dataframe(df, width=1000, height=300)