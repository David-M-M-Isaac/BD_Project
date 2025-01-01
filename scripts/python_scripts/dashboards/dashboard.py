import streamlit as st
import plotly.express as px
from st_keyup import st_keyup
import datetime
import pandas as pd

from scripts.python_scripts.database.database import Database

# Database
database_obj = Database()
database = database_obj.get_database('Relatorios')

relatorios_teste = database['teste']

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
        options=['YouTube Views', 'Stocks Value', 'Merged']
    )
with col3:
    company = st.selectbox(
        label="Select Company",
        options=['Sony', 'Nvidia', 'Dell', 'Microsoft', 'Intel', 'IBM']
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
    plot_data_line(date_interval=[1, 2, 3, 4, 5], data=[2, 4, 3, 10, 7], company=company)
elif preview_type == 'Stocks Value':
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
