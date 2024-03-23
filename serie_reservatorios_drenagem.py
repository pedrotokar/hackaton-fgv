import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv(r"C:\Users\laris\OneDrive\Documentos\hackaton-fgv\dados\drenagem_reservatorios.csv")

df['data_hora'] = pd.to_datetime(df['data_particao'] + ' ' + df['horario'])

for i in range(3):
    df.loc[df['altura_agua'] > 30, 'altura_agua'] /= 100

df = df.drop(df[df['altura_agua'] > 3].index)
df = df.sort_values(by="data_hora")

fig = px.line(df, x='data_hora', y='altura_agua', color='nome_reservatorio')

fig.update_layout(title='Altura da Água em Reservatórios de Drenagem',
    xaxis_title='Data',
    yaxis_title='Altura da Água (m)',
    legend_title='Reservatório',
    barmode='overlay',
    plot_bgcolor='white',
    template='ygridoff'
)

fig.update_xaxes(ticks='outside')

fig.add_shape(type="line", x0=df['data_hora'].min(), x1=df['data_hora'].max(), y0=1, y1=1,
              line=dict(color="lightskyblue", width=2))
fig.add_shape(type="line", x0=df['data_hora'].min(), x1=df['data_hora'].max(), y0=1.5, y1=1.5,
              line=dict(color="pink", width=2))
fig.add_shape(type="line", x0=df['data_hora'].min(), x1=df['data_hora'].max(), y0=2.5, y1=2.5,
              line=dict(color="black", width=2))

# Adicionar rótulos
fig.add_annotation(x=df['data_hora'].min(), y=1, text="Atenção", showarrow=False, yshift=13, xshift=31, font=dict(
            size=10
            ),
        borderwidth=1,
        bgcolor="white",
        opacity=0.9)
fig.add_annotation(x=df['data_hora'].min(), y=1.5, text="Alerta", showarrow=False, yshift=13, xshift=23, font=dict(
            size=10
            ),
        borderwidth=1,
        bgcolor="white",
        opacity=0.9)
fig.add_annotation(x=df['data_hora'].min(), y=2.5, text="Extravasamento", showarrow=False, yshift=13, xshift=49 , font=dict(
            size=10
            ),
        borderwidth=1,
        bgcolor="white",
        opacity=0.9)

# Exibindo os gráficos lado a lado
fig.show()


