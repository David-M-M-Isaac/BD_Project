import streamlit as st
import plotly.express as px
import datetime
import pandas as pd
import numpy as np

from datetime import datetime, date, time
from collections import defaultdict
from enum import Enum

from scripts.python_scripts.database.database import Database

class Options(Enum):
    COMPANY = {'company': ('Sony', 'Nvidia', 'Microsoft', 'Dell', 'Intel', 'IBM')}
    PREVIEW = {'type': ('YouTube Views', 'Stocks Value', 'Merged')}

# Database
database_obj = Database()
database = database_obj.get_database('Final_Database')

current_collection = 'youtube'

def retrieve_data_plot_line(preview_collection : str, company : str, time_period : tuple):
    x_label = 'Date'

    if len(time_period) == 1:
        time_period = (time_period[0], time_period[0])

    collection_yt = database['youtube']
    collection_company = database['company']

    start_date = datetime.combine(time_period[0], time.min)
    end_date = datetime.combine(time_period[1], time.max)
    query_yt = {"company": company.lower(), "publishedAt": {"$gte": start_date, "$lte": end_date}}
    query_company = {"company_name": company.lower(), "Date": {"$gte": start_date, "$lte": end_date}}

    if preview_collection == 'youtube': # YOUTUBE VIEWS
        documents = collection_yt.find(query_yt)
        x = [date['publishedAt'] for date in documents.__copy__()]
        y1 = [views['view_count'] for views in documents.__copy__()]
        y_label = 'Views'
        df = pd.DataFrame({'x': x, 'y1': y1})
    elif preview_collection == 'company': # STOCKS
        documents = collection_company.find(query_company)
        x = [date['Date'] for date in documents.__copy__()]
        y1 = [adj_close['Adj Close'] for adj_close in documents.__copy__()]
        y_label = 'Adj Close'
        df = pd.DataFrame({'x': x, 'y1': y1})
    else: # MERGED
        documents_company = collection_company.find(query_company)
        documents_youtube = collection_yt.find(query_yt)
        x1 = [date['publishedAt'] for date in documents_youtube.__copy__()]
        x2 = [date['Date'] for date in documents_company.__copy__()]
        y1 = [views['view_count'] for views in documents_youtube.__copy__()]
        y2 = [adj_close['Adj Close'] for adj_close in documents_company.__copy__()]

        x, y1, y2 = merge_data(x1,x2,y1,y2)
        y_label = 'Normalized Values'
        df = pd.DataFrame({'x': x, 'y1': y1, 'y2': y2})

    df = sum_dataframe(df)

    return df, x_label, y_label

def retrieve_data_plot_bar(time_period : tuple):
    if len(time_period) == 1:
        time_period = (time_period[0], time_period[0])

    collection_yt = database['youtube']
    collection_company = database['company']

    start_date = datetime.combine(time_period[0], time.min)
    end_date = datetime.combine(time_period[1], time.max)

    query_yt = {"publishedAt": {"$gte": start_date, "$lte": end_date}}
    query_company = {"Date": {"$gte": start_date, "$lte": end_date}}

    documents_company = collection_company.find(query_company)
    documents_youtube = collection_yt.find(query_yt)

    companies = {'dell': 0,'intel': 0,'microsoft': 0,'nvidia': 0,'ibm': 0,'sony': 0}
    yt = {'dell': 0,'intel': 0,'microsoft': 0,'nvidia': 0,'ibm': 0,'sony': 0}

    for document in documents_company:
        company_name = document.get('company_name', '').lower()  # Get company name and ensure it's lowercase
        if company_name in companies:
            companies[company_name] += document['Adj Close']

    for document in documents_youtube:
        company = document.get('company', '').lower()
        if company in companies:
            yt[company] += document['view_count']

    df = pd.DataFrame({'company': list(yt.keys()),'yt': list(yt.values()), 'stocks': list(companies.values())})

    print('df: ', df.head())

    df['yt'] = df['yt']
    df['stocks'] = df['stocks']

    return df

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

def merge_data(x1, x2, y1, y2):
    # Use a set to merge and sort the unique dates from x1 and x2
    x3 = sorted(set(x1) | set(x2))

    # Create dictionaries for quick lookup of y1 and y2 values by date
    date_to_y1 = defaultdict(int, zip(x1, y1))
    date_to_y2 = defaultdict(int, zip(x2, y2))

    # Build y3 and y4 using the merged date array x3
    y3 = [date_to_y1[date] for date in x3]
    y4 = [date_to_y2[date] for date in x3]

    return x3, y3, y4

def sum_dataframe(df):
    if df.shape[1] == 3:
        # Step 1: Replace zeros with NaN to interpolate
        df['y1'] = df['y1'].replace(0, np.nan).interpolate()
        df['y2'] = df['y2'].replace(0, np.nan).interpolate()

        # Step 2: Smooth the data using a rolling average
        df['y1_smooth'] = df['y1'].rolling(window=7, min_periods=1).mean()
        df['y2_smooth'] = df['y2'].rolling(window=7, min_periods=1).mean()

        # Step 3: Normalize the data
        df['y1'] = normalize(df['y1_smooth'])
        df['y2'] = normalize(df['y2_smooth'])
        df = df.groupby('x', as_index=False).sum()
    else:
        df = df.groupby('x')['y1'].sum().reset_index()

    return df.sort_values(by='x')


# Nome do nosso Streamlit
st.title("DashBoard Data")

col1, col2, col3 = st.columns(3)

today = datetime.now()

# Define January 1 and December 31 of the next year
jan_1 = date(2020, 1, 1)
dec_31_this_year = date(today.year, 12, 31)

# Define the minimum and maximum date range
min_value = date(1998, 1, 1)  # Minimum date is January 1, 1999

with col1:
    d = st.date_input(
        label="Select (Start - End) Date",
        value=(jan_1, dec_31_this_year),
        min_value=min_value,
        max_value=dec_31_this_year,
        format="YYYY.MM.DD",
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
def plot_data_line(dataframe, x_label, y_label, company, preview_type):
    if preview_type == 'Merged':

        dataframe = dataframe.rename(columns={"y1": "YouTube Views", "y2": "Stocks Value"})

        fig = px.line(
            dataframe,
            x="x",
            y=['YouTube Views', 'Stocks Value'],
            labels={
                "x": x_label,
                "value": y_label,
                "variable": "Metrics"
            },
            title=f"{preview_type} - {company}",
        )
    else:
        fig = px.line(
            dataframe,
            x="x",
            y="y1",
            labels={
                "x": x_label,
                "y1": y_label,
            },
            title=f"{preview_type} - {company}",
        )

    st.plotly_chart(fig)

def plot_data_bar(df):
    # Create a copy of the original DataFrame
    data_ = df.copy()

    # Reshape the DataFrame into long format
    data_long = data_.melt(id_vars=['company'],  # 'company' as the identifier
                           value_vars=['yt', 'stocks'],  # Metrics to melt
                           var_name='metric',  # Name for the 'metric' column
                           value_name='count')  # Name for the values

    metric_labels = {'yt': 'YouTube Views', 'stocks': 'Stock Values'}
    data_long['metric'] = data_long['metric'].map(metric_labels)

    # Plot the bar chart
    fig = px.bar(
        data_long,
        x="count",
        y="company",  # Plot the companies on the y-axis
        color="metric",  # Differentiate by metric (yt or stocks)
        orientation="h",  # Horizontal bar chart
        title="YouTube Views - Companies Stock Value",
        labels={'count': 'Values', 'companies': 'Company', 'metric': 'Metric'}
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig)

if preview_type == 'YouTube Views':
    current_collection = 'youtube'

elif preview_type == 'Stocks Value':
    current_collection = 'company'

else:
    current_collection = ''

df, x_label, y_label = retrieve_data_plot_line(preview_collection=current_collection, company=company, time_period=d)

plot_data_line(dataframe=df, x_label=x_label, y_label=y_label, company=company, preview_type=preview_type)

lower_col1, lower_col2 = st.columns(2)
with lower_col1:
    plot_data_bar(retrieve_data_plot_bar(time_period=d))
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