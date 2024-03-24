import pandas as pd
import plotly.express as px

df = pd.read_csv(r"dados\fluviometro_inea2.csv")
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

fig.show()