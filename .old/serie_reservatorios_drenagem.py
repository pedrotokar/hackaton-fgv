import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv(r"C:\Users\laris\OneDrive\Documentos\hackaton-fgv\dados\drenagem_reservatorios.csv")

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




# Exibindo os gráficos lado a lado
fig.show()


