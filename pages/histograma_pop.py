import pandas as pd
import pandas_gbq
import plotly.graph_objs as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 

df = pd.read_csv(r"dados\gravidade_pops.csv")

# Mapeando os valores numéricos para os nomes correspondentes
mapa_nomes = {6.0: "Alagamento", 5.0: "Bolsão D'Água", 31.0: "Alagamento", 32.0: "Enchente", 33.0: "Enchente"}
df['id_pop'] = df['id_pop'].map(mapa_nomes)

df['gravidade'].replace({'Medio': 'Média', 'Médio': 'Média',
                                        'Normal': 'Média', 'Baixo':'Baixa', 'Critico':'Crítica', 'Alto': 'Alta'}, inplace=True)

quantificacao_gravidade = df['gravidade']
df.insert(1, "quantificacao_gravidade", quantificacao_gravidade)
df['quantificacao_gravidade'].replace({'Baixa': 1, 'Média': 2, 'Alta': 3, 'Crítica' : 4}, inplace=True)

# Criar o gráfico com o filtro interativo
fig = px.histogram(df, x='data_inicio', color='id_pop', marginal='rug', nbins=120)

# Adicionar filtro interativo
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="Todas",
                     method="update",
                     args=[{"visible": [True, True, True, True]},
                           {"title": "Distribuição de ocorrências POP por semestre"}]),
                dict(label="Baixa",
                     method="update",
                     args=[{"visible": [True, False, False, False]},
                           {"title": "Distribuição de ocorrências POP por semestre - Gravidade: Baixa"}]),
                dict(label="Média",
                     method="update",
                     args=[{"visible": [False, True, False, False]},
                           {"title": "Distribuição de ocorrências POP por semestre - Gravidade: Média"}]),
                dict(label="Alta",
                     method="update",
                     args=[{"visible": [False, False, True, False]},
                           {"title": "Distribuição de ocorrências POP por semestre - Gravidade: Alta"}]),
                dict(label="Crítica",
                     method="update",
                     args=[{"visible": [False, False, False, True]},
                           {"title": "Distribuição de ocorrências POP por semestre - Gravidade: Crítica"}]),
            ]),
            direction="down",
            showactive=True,
        )
    ]
)

# Atualizar layout
fig.update_layout(title='Distribuição de ocorrências POP',
    xaxis_title='Data de início',
    yaxis_title='Contagem',
    legend_title='Tipo de Procedimento Operacional Padrão',
    barmode='overlay',
    plot_bgcolor='white',
    template='ygridoff'
)

fig.update_xaxes(ticks='outside')

fig.show()
