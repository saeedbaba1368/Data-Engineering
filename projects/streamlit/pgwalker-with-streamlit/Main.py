import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pygwalker as pyg

# page layout
st.set_page_config(page_title="Analytics", page_icon="🌎", layout="wide")

# title
st.title("⏱ PYGWALKER")

# load dataset
df = pd.read_excel("foodsales.xlsx", sheet_name="FoodSales")

# pyg_html = pyg.to_html(df)
pyg_html = pyg.walk(df, return_html=True, dark="dark")
components.html(pyg_html, height=1000, scrolling=True)
