import streamlit as st
import pandas as pd
import pandas as pd
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json

from default import default_style

default_style()

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)


st.write("""# Introdução

O presente trabalho é o resultado de um hackathon de programação organizado pela Fundação Getúlio Vargas e a Prefeitura do Rio de Janeiro. Nosso objetivo era construir uma plataforma que concentrasse todos os dados das chuvas da área metropolitana do Rio de Janeiro de maneira lúdica e interativa. A solução apresentada consiste em uma plataforma web com gráficos interativos sobre alguns dos pontos mais críticos para o entendimento da situação hidrológica da cidade, com textos explicativos para cada um desses.
Os Gráficos

## Gráficos COR

O Centro de Operações Rio (COR) desempenha um papel fundamental na compreensão e na resposta a eventos relacionados à água, como inundações, deslizamentos de terra e outros desastres naturais. A cidade do Rio de Janeiro enfrenta desafios significativos relacionados à gestão de água devido à sua topografia complexa, com áreas de alta densidade populacional propensas a inundações e deslizamentos em caso de chuvas intensas.

### Série histórica de Procedimentos Operacionais Padrão

Cada cor representa um tipo de Procedimento Operacional Padrão (POP), e a altura de cada barra mostra quantos foram realizados naquele momento. É possível filtrar tanto pela gravidade dos procedimentos realizados, à esquerda, quanto pelo seu tipo.

### Estações de Monitoramento de Eventos Hidrológicos

O mapa é interativo: ao clicar sobre uma das estações, aparecem as informações sobre o nome desta e o acumulado da chuva nos últimos 10 minutos, 1 hora e 1 dia.

### Agregado do Número de Chamados

O mapa mostra uma relação entre os bairros de acordo com a quantidade de chamados em cada. O mapa é interativo de acordo com o tipo de chamado: COR ou 1746.

### Localização Exata dos Chamados

Nesse mapa, são mostrados todos os chamados registrados em seu local específico. A gravidade dos chamados (normal, média ou alta) é separada por cores. Duas opções de filtro estão disponíveis: chamados em aberto e fechados.

### Problemas de Enchente

Nesse mapa, é possível ver todos os pontos que geram ou já geraram problemas de enchentes. É possível ver a sua gravidade de acordo com uma escala de cores, onde temos situações críticas, observadas e monitoradas.

### Gráficos Águas do Rio

Águas do Rio é uma instituição fundamental para a compreensão e gestão dos dados hidrológicos na cidade do Rio de Janeiro.

### Nível da lâmina d’água em via

Monitorar o nível da lâmina d'água em vias é de extrema importância por diversas razões, entre elas: segurança viária, prevenção de acidentes, erosão e danos estruturais, previsão e alerta de inundações, e planejamento urbano.

### Altura da lâmina d’água nos fluviômetros

Este gráfico mostra a altura da lâmina d’água nos fluviômetros do INEA a partir de março de 2024.

### Altura da água em reservatórios de drenagem

Os reservatórios de detenção, popularmente conhecidos como “piscinões”, são estruturas hidráulicas que têm como função retirar e acumular temporariamente um volume de água do sistema de drenagem.

### Altura relativa da água em reservatórios de drenagem

Os dados são basicamente os mesmos do gráfico anterior, só que desta vez foi plotado o percentual de enchimento do reservatório.

Este relatório apresenta uma visão abrangente das soluções desenvolvidas durante o hackathon, visando contribuir para uma gestão mais eficiente e informada das questões hidrológicas na cidade do Rio de Janeiro. Agradecemos o interesse e esperamos que estas ferramentas sejam úteis para todos os envolvidos na gestão das chuvas e dos recursos hídricos da região metropolitana.
""")
