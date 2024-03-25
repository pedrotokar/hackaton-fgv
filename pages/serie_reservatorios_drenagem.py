import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.write("""
        # Altura da Água em Reservatórios de Drenagem
         
         O Instituto Estadual do Ambiente (INEA) do Rio de Janeiro monitora a altura da água nos fluviômetros para diversas finalidades, incluindo o acompanhamento de cheias e inundações, a previsão de eventos climáticos extremos, a gestão dos recursos hídricos, o controle da qualidade da água e o planejamento de infraestrutura hidráulica. Essa análise é crucial para alertar sobre riscos, planejar intervenções e garantir a sustentabilidade ambiental e a segurança da população.
        """)

df = pd.read_csv(r"dados/tabelas/drenagem_reservatorios.csv")

df['data_hora'] = pd.to_datetime(df['data_particao'] + ' ' + df['horario'])

for i in range(2):
    df.loc[df['altura_agua'] > 30, 'altura_agua'] /= 100

df = df.drop(df[df['altura_agua'] > 30].index)
df = df.sort_values(by="data_hora")

fig = px.line(df, x='data_hora', y='altura_agua', color='nome_reservatorio')

fig.update_layout(title='Altura da Água em Reservatórios de Drenagem',
    xaxis_title='Data',
    yaxis_title='Altura da Água (m)',
    legend_title='Reservatório e Nível de Alerta',
    barmode='overlay',
    plot_bgcolor='white',
    template='ygridoff',
)

fig.update_xaxes(ticks='outside')

fig.add_shape(type="line", showlegend=True, legendgroup="Níveis de Alerta", name="Atenção", x0=df['data_hora'].min(), x1=df['data_hora'].max(), y0=1, y1=1,
              line=dict(color="lightskyblue", width=2, dash="dashdot",))
fig.add_shape(type="line", showlegend=True, legendgroup="Níveis de Alerta", name="Alerta",x0=df['data_hora'].min(), x1=df['data_hora'].max(), y0=1.5, y1=1.5,
              line=dict(color="yellow", width=2, dash="dashdot",))
fig.add_shape(type="line", showlegend=True, legendgroup="Níveis de Alerta", name="Extravasamento", x0=df['data_hora'].min(), x1=df['data_hora'].max(), y0=2.5, y1=2.5,
              line=dict(color="black", width=2, dash="dashdot",))


st.plotly_chart(fig)

st.dataframe(df, width=1000, height=300)