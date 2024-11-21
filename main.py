import numpy as np
import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_plots import top_names_plot, unique_names_summary, name_trend_plot, name_frequencies_plot
import streamlit as st

@st.cache_data
def load_name_data():
    names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
    response = requests.get(names_file)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        dfs = []
        files = [file for file in z.namelist() if file.endswith('.txt')]
        for file in files:
            with z.open(file) as f:
                df = pd.read_csv(f, header=None)
                df.columns = ['name','sex','count']
                df['year'] = int(file[3:7])
                dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
    return data

@st.cache_data
def ohw(df):
    nunique_year = df.groupby(['name', 'sex'])['year'].nunique()
    one_hit_wonders = nunique_year[nunique_year == 1].index
    one_hit_wonder_data = df.set_index(['name', 'sex']).loc[one_hit_wonders].reset_index()
    return one_hit_wonder_data

data = load_name_data()
ohw_data = ohw(data)

st.title('My Cool Name App')

tab1, tab2 = st.tabs(['Names', 'Year'])
with tab1:

    input_name = st.text_input('Enter a name:')

    name_data = data[data['name']==input_name].copy()
    fig = px.line(name_data, x='year',y='count',color='sex')


    st.plotly_chart(fig)

with tab2:

    year_input_tab2 = st.slider("Year", min_value=1880, max_value=2023, value=2000, key="tab2_year_slider")
    fig2 = top_names_plot(data, year=year_input_tab2)

    st.plotly_chart(fig2)

    st.write('Unique Names Table')
    output_table = unique_names_summary(data, 2000)

    st.write(f"Total babies born in {year_input_tab2}: {data[data['year'] == year_input_tab2]['count'].sum()}")


with st.sidebar:
    input_name = st.text_input('Enter a name:', 'Mary')
    year_input_sidebar = st.slider('Year', min_value=1880, max_value=2023, value=2000, key="sidebar_year_slider")
    n_names = st.radio('Number of names per sex', [3,5,10])

with st.container():
    st.write("Statistics for the year:")
    st.bar_chart(data[data['year'] == year_input_tab2].groupby('sex')['count'].sum())
    st.dataframe(data[data['year'] == year_input_tab2].head())