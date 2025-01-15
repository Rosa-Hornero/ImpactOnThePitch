import pandas as pd
import streamlit as st



# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("../streamlit/static/player_injuries_impact.csv",  delimiter=',')

# Función para contar resultados
def count_results(results):
    return {
        "Win": (results == "win").sum(),
        "Draw": (results == "draw").sum(),
        "Loss": (results == "lose").sum(),
    }

# Calculo de media
def media_FIFA(data):
    sum = 0
    nums = 0
    for i in range(0,len(data)):
        try:
            sum = sum + float(data[i])
            nums = nums +1
        except:
            nums = nums
    if nums == 0:
        media = 0
    else:
        media = sum / nums
    return media
