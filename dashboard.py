import streamlit as st
import plotly.express as px
import datetime
import pandas as pd

from enum import Enum
from scripts.python_scripts.database.database import Database

class Options(Enum):
    COMPANY = {'company': ('Sony', 'Nvidia', 'Microsoft', 'Dell', 'Intel', 'IBM')}
    PREVIEW = {'type': ('YouTube Views', 'Stocks Value', 'Merged')}

# Database
database_obj = Database()
database = database_obj.get_database('Final_Database')

current_collection = 'youtube'

def retrieve_data(preview_collection : str, company : str):
    collection = database[preview_collection]
    x, y, x_label, y_label = [], [], 'Date', ''

    if preview_collection == 'youtube':
        documents = collection.find({"company": company.lower()})
        x = [date for date in documents['publishedAt']]
        y = [views for views in documents['views_count']]
        y_label = 'Views'
    elif preview_collection == 'company':
        documents = collection.find({"company_name": company.lower()})
        x = [date for date in documents['Date']]
        y = [adj_close for adj_close in documents['Adj Close']]
        y_label = 'Adj Close'
    x_label = 'Date'

    return x, y, x_label, y_label

# Nome do nosso Streamlit
st.title("DashBoard Data")

col1, col2, col3 = st.columns(3)

today = datetime.datetime.now()
next_year = today.year + 1

jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)
min_value = datetime.date(1999, 1, 1)  # Set the minimum date to January 1, 1999
max_value = datetime.date(next_year, 12, 31)

with col1:
    d = st.date_input(
        label="Select (Start - End) Date",
        value=(jan_1, datetime.date(next_year, 1, 7)),
        min_value=min_value,
        max_value=dec_31,
        format="MM.DD.YYYY",
    )
with col2:
    preview_type = st.selectbox(
        label="Select Data to Preview",
        options=list(Options.PREVIEW.value['type'])
    )
with col3:
    company = st.selectbox(
        label="Select Company",
        options=list(Options.COMPANY.value['company'])
    )

# Gráfico de barras das probabilidades
def plot_data_line(date_interval, data, company):

    data_ = pd.DataFrame({
        'date_interval': date_interval,
        'data': data,
        'company': company,
    })

    fig = px.line(
        data_,
        x="date_interval",
        y="data",
        orientation="h",
        title=f"{preview_type} - {company}",
    )

    st.plotly_chart(fig)

def plot_data_bar():
    data_ = pd.DataFrame({
        'data_views': [20,30,40,50,60,70],
        'data_stocks': [10,50,40,15,20,35],
        'companies': ['Sony', 'Nvidia', 'Dell', 'Microsoft', 'Intel', 'IBM'],
    })

    # Reshape the DataFrame into long format
    data_long = data_.melt(id_vars='companies',
                           value_vars=['data_views', 'data_stocks'],
                           var_name='metric',
                           value_name='count')

    fig = px.bar(
        data_long,
        x="count",
        y="companies",
        color="metric",
        orientation="h",
        title=f"{preview_type} - Companies",
        labels={'count': 'Values', 'companies': 'Company', 'metric': 'Metric'}
    )

    st.plotly_chart(fig)

if preview_type == 'YouTube Views':
    current_collection = 'youtube'
    plot_data_line(date_interval=[1, 2, 3, 4, 5], data=[2, 4, 3, 10, 7], company=company)
elif preview_type == 'Stocks Value':
    current_collection = 'company'
    plot_data_line([1, 2, 3, 4, 5], [5, 3, 2, 10, 15], company)

lower_col1, lower_col2 = st.columns(2)
with lower_col1:
    plot_data_bar()
with lower_col2:
    lower_right_col1, lower_right_col2 = st.columns(2)
    height = 170
    with lower_right_col1:
        lower_container = st.container(height=height)
        lower_container.write("Average Views")
        lower_container.metric('x1.191', value='20K', delta='19.1%', delta_color='normal')

    with lower_right_col2:
        upper_container = st.container(height=height)
        upper_container.write("Average Stocks")
        upper_container.metric('x0.97', value='370K', delta=f'{-3}%', delta_color='normal')

print(retrieve_data(preview_collection=current_collection, company='Nvidia'))