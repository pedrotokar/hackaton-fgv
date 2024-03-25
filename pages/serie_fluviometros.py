import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit as st


df = pd.read_csv(r"dados/tabelas/fluviometro_inea2.csv")

df['data_medicao'] = pd.to_datetime(df['data_medicao'])
df = df.sort_values(by="data_medicao")

fig = px.line(df, x='data_medicao', y='altura_agua', color='id_estacao')

fig.update_layout(title='Altura da Lâmina D\'Água nos Fluviômetros do INEA',
    xaxis_title='Data',
    yaxis_title='Altura da Água (m)',
    legend_title='Estação',
    barmode='overlay',
    plot_bgcolor='white',
    template='ygridoff'
)

fig.update_xaxes(ticks='outside')

st.plotly_chart(fig)