import streamlit as st

def default_style():
    hide_streamlit_style = """
                            <style>
                            div[data-testid="stToolbar"] {
                            visibility: hidden;
                            height: 0%;
                            position: fixed;
                            }
                            div[data-testid="stDecoration"] {
                            visibility: hidden;
                            height: 0%;
                            position: fixed;
                            }
                            div[data-testid="stStatusWidget"] {
                            visibility: hidden;
                            height: 0%;
                            position: fixed;
                            }
                            #MainMenu {
                            visibility: hidden;
                            height: 0%;
                            }
                            header {
                            visibility: hidden;
                            height: 0%;
                            }
                            footer {
                            visibility: hidden;
                            height: 0%;
                            }
                            </style>
                            """


    st.set_page_config(page_icon=":droplet:", layout="centered", initial_sidebar_state="auto")

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)   
    st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)