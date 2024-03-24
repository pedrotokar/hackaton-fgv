import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv(r"C:\Users\laris\OneDrive\Documentos\hackaton-fgv\dados\drenagem_reservatorios.csv")

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
fig.show()


