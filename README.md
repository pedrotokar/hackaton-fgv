# Hackathon

Esse repositório faz parte de nossa submissão para o Hackathon organizado FGValley, EMAp e Prefeitura do Rio de Janeiro em 2024. 

O objetivo era construir uma plataforma que concentrasse todos os dados das chuvas da área metropolitana do Rio de Janeiro de maneira lúdica e interativa.
A solução apresentada consiste em uma plataforma web com gráficos interativos sobre alguns dos pontos mais críticos para o entendimento da situação hidrológica da cidade, 
com textos explicativos para cada um desses.

## Rodando o projeto

Para obter uma cópia do site apresentado rodando em sua máquina local, é necessário instalar as bibliotecas que usamos. Para isso, é necessário rodar:

```bash
$ pip install -r requirements.txt
```

Após isso, tudo já deve estar configurado. Para rodar, use o comando

```bash
$ streamlit run Home.py
```

## Autenticação

Para que todas as visualizações sejam mostradas sem problemas, é necessário que você tenha disponível uma conta gmail com acesso às tabelas privilegiadas.
Quando uma query for feita, uma janela de autenticação será aberta. Você deverá selecionar sua conta gmail  com o acesso necessário. Após isso, não será mais
necessário autenticar, já que as informações ficarão armazenadas em seu computador.
