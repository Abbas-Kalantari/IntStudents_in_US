import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime as dt
import plotly.express as px
import time
st.set_page_config(layout="wide", page_title='International Students in US')

st.title('International Students in US')

@st.cache
def load_data():
    data= pd.read_csv('international_students_in_us.csv', index_col=0)
    data= data.replace("-", 0)
    data['year'] = data['year'].astype(int)
    data['student_number'] = data['student_number'].astype(float)
    data= data.sort_values(['country', 'year'])

    return data




st.sidebar.title('Navigate Through Pages')
page= st.sidebar.radio('Explore pages', ['Charts & Visualizations', 'Raw Data'])

data = load_data()

if page=='Charts & Visualizations':

    country_list=  data.groupby('country').count().reset_index()['country'].tolist()

    country_input= st.multiselect('Country Name', country_list)

    # choosing the start date
    start_date = st.number_input("Choose the start date", value=1949,
                                min_value=1949,
                                max_value=2020)  
    # choosing the end date
    end_date = st.number_input("Choose the end date", value=2020,
                                min_value=start_date,
                                max_value=2020)  
    if len(country_input) > 0:
        subset_data = data[data['country'].isin(country_input)]  # getting the stats of the selected country/ies
        # subset_data = subset_data.sort_values(by="date")  # sorting values based on the date
        subset_data = subset_data[((subset_data["year"] )> start_date) & ((subset_data["year"] )< end_date)]  # filtering data based on the selected period

        def draw_plots():
                st.markdown(f'<h2 style="text-align: left;"> Comparing International Students in US Based on Their Country </h2>', unsafe_allow_html=True)
                total_graph = px.line(x=subset_data["year"],
                                    y=subset_data["student_number"],
                                    width=1000,
                                    color=subset_data["country"],
                                    )  # plotly graph
                total_graph.update_layout(title=f'Comparison of the Total Number of International Students',
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='Students Number'),
                                        legend_title=dict(text='<b>Countries</b>')
                                        )
                st.plotly_chart(total_graph)

                index_graph = px.line(x=subset_data["year"],
                                    y=subset_data["student_number"]/subset_data["population"],
                                    width=1000,
                                    color=subset_data["country"],
                                    )  # plotly graph
                index_graph.update_layout(title=f'" Index: Students Number/ Country Popultion"',
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='Students Number/Popultion'),
                                        legend_title=dict(text='<b>Countries</b>')
                                        )
                st.plotly_chart(index_graph)
        
        draw_plots()


if page=='Raw Data':

    st.subheader('Raw data')
    st.write(data)