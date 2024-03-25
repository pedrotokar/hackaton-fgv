import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit as st

st.write("""
         # Altura da Água em Fluviômetros do INEA
         
         O Instituto Estadual do Ambiente (INEA) do Rio de Janeiro monitora a altura da água nos fluviômetros para diversas finalidades, incluindo o acompanhamento de cheias e inundações, a previsão de eventos climáticos extremos, a gestão dos recursos hídricos, o controle da qualidade da água e o planejamento de infraestrutura hidráulica. Essa análise é crucial para alertar sobre riscos, planejar intervenções e garantir a sustentabilidade ambiental e a segurança da população.
         """)

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

st.dataframe(df, width=1000, height=300)