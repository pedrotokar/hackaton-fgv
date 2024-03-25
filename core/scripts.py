import streamlit as st
import pandas_gbq

@st.cache_data
def get_data(query, project_id):
     
    data = pandas_gbq.read_gbq(query, project_id = "hackaton-fgv")
    # data.to_csv("chamados_1746.csv")

    return data