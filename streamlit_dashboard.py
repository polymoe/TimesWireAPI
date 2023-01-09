import plotly.express as px
import streamlit as st
import pandas as pd
import requests
import json
from pywaffle import Waffle
import matplotlib.pyplot as plt
import math
import numpy as np
import base64
import streamlit.components.v1 as components
import subprocess
import sys
import docker

def add_bg_from_local(image_file):
  with open(image_file, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
  st.markdown(
  f"""
  <style>
  .stApp {{
      background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
      background-size: cover
  }}
  </style>
  """,
  unsafe_allow_html=True
  )

def run_subprocess():

  p = subprocess.run([f"{sys.executable}", "pipeline.py"])
  st.write(p)
    
add_bg_from_local('ny.jpg')

# Title
st.title("BigApplePI : reproduction du dashboard Kibana grâce à la FastAPI")

st.sidebar.title("Soutenance formation DE")
st.sidebar.subheader("choisissez votre top !")
st.sidebar.write("Les visualisations s'ajusteront automatiquement selon la taille du classement que vous souhaitez en retour")
top = st.sidebar.slider("top ..", 1, 20, 10)

st.sidebar.subheader("A. Fradin, T. Kiener, M. Toumi")
st.sidebar.write("9 janvier 2023")

if st.button('Update data'):
  run_subprocess()

requestUrl = "http://127.0.0.1:8000/viz"
requestHeaders = {
    "accept": "application/json",
    "Authorization" : "Basic YWxpY2U6d29uZGVybGFuZA==",
    "Content-Type" : "application/json"
}

### viz : top geo ###
query_body_geo = {
  "top": top,
  "viz": "geo"
}
response_geo = requests.post(requestUrl, headers=requestHeaders, data = json.dumps(query_body_geo))

df_geo = pd.DataFrame.from_dict(response_geo.json())

fig_geo = px.treemap(df_geo, path=["key"], values='doc_count')
fig_geo.update_traces(root_color="rgba(89, 179, 191, 0.5)")
fig_geo.update_layout(margin = dict(t=50, l=25, r=25, b=25), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

### viz : top material ###
query_body_material = {
  "top": top,
  "viz": "material_type"
}
response_material = requests.post(requestUrl, headers=requestHeaders, data = json.dumps(query_body_material))

df_material = pd.DataFrame.from_dict(response_material.json())

fig_material = plt.figure(
    FigureClass=Waffle, 
    rows=15, 
    values=list(df_material.doc_count),
    labels=list(df_material.key),
    figsize=(13, 6),
    legend={'bbox_to_anchor': (0.5, 0.5)},
    facecolor=None   
)

## viz : people vs geo ###
query_body_pvg = {
  "top": top,
  "viz": "people_vs_geo"
}
response_pvg = requests.post(requestUrl, headers=requestHeaders, data = json.dumps(query_body_pvg))

df_pvg = pd.DataFrame(columns=['key', 'doc_count', 'people'])

for element in range(len(response_pvg.json())):
  parse=response_pvg.json()[element]['1']['buckets']
  df = pd.DataFrame.from_dict(parse)
  df["people"] = response_pvg.json()[element]['key']
  df_pvg = pd.concat([df_pvg,df], axis = 0)

print(df_pvg)

fig_pvg = px.sunburst(df_pvg, path=['people', 'key'], values='doc_count', color='people')
fig_pvg.update_layout(paper_bgcolor="rgba(89, 179, 191, 0.5)", plot_bgcolor="rgba(89, 179, 191, 0.5)")

tab1, tab2, tab3 = st.tabs(["Treemap (top of geo)", "Waffle (top of materials)", "Sunburst pie chard (people vs geo)"])
with tab1:
    # for  Streamlit theme, use theme = "streamlit"
    # None is the default (plotly default). So you can also omit the theme argument.
    st.plotly_chart(fig_geo, theme=None, use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.pyplot(fig_material)
with tab3:
    # for  Streamlit theme, use theme = "streamlit"
    # None is the default (plotly default). So you can also omit the theme argument.
    st.plotly_chart(fig_pvg, theme=None, use_container_width=True)
# with tab4:
#     components.iframe("http://108.128.121.13:5601/s/soutenance/app/dashboards#/view/da98e0c0-8b75-11ed-9aea-4904f7ce7c8e?_g=(filters%3A!())", 1000,1000)
  