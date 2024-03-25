import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from default import default_style

default_style()

st.write("""
        # Altura Relativa da Água em Reservatórios de Drenagem
         
        O Instituto Estadual do Ambiente (INEA) do Rio de Janeiro monitora a altura da água nos fluviômetros para diversas finalidades, incluindo o acompanhamento de cheias e inundações, a previsão de eventos climáticos extremos, a gestão dos recursos hídricos, o controle da qualidade da água e o planejamento de infraestrutura hidráulica. Essa análise é crucial para alertar sobre riscos, planejar intervenções e garantir a sustentabilidade ambiental e a segurança da população.
        """)

df = pd.read_csv(r"dados/tabelas/drenagem_reservatorios.csv")

df['data_hora'] = pd.to_datetime(df['data_particao'] + ' ' + df['horario'])

for i in range(2):
    df.loc[df['altura_agua'] > 30, 'altura_agua'] /= 100
    
df.loc[df['nome_reservatorio'] == 'Bandeira', 'altura_agua'] /= 18
df.loc[df['nome_reservatorio'] == 'Varnhagen', 'altura_agua'] /= 21.50
df.loc[df['nome_reservatorio'] == 'Niteroi', 'altura_agua'] /= 22.25

df = df.drop(df[df['altura_agua'] > 1].index)
df = df.sort_values(by="data_hora")

fig = px.line(df, x='data_hora', y='altura_agua', color='nome_reservatorio')

fig.update_layout(title='Altura da Relativa da Água em Reservatórios de Drenagem',
    xaxis_title='Data',
    yaxis_title='Altura Relativa da Água',
    legend_title='Reservatório',
    barmode='overlay',
    plot_bgcolor='white',
    template='ygridoff'
)

fig.update_xaxes(ticks='outside')

# Exibindo os gráficos lado a lado
st.plotly_chart(fig)

st.dataframe(df, width=1000, height=300)