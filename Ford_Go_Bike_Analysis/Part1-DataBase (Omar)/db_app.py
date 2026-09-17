import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

DATABASE_URL = (
    'postgresql://postgres:01114473131@localhost:5432/ford_gobike'
)
engine = create_engine(DATABASE_URL)

st.set_page_config(page_title='Ford GoBike DB Viewer', layout='wide')
st.title('🚲 Ford GoBike - PostgreSQL Database Viewer')

table_name = st.sidebar.selectbox(
    'Select Table from DataBase:',
    ['fact_trips', 'dim_time', 'dim_station', 'dim_user'],
)

num_rows = st.sidebar.slider('Number of rows:', 5, 100, 10)
 
try:
  query = f'SELECT * FROM {table_name} LIMIT {num_rows};'
  df = pd.read_sql(query, engine)

  st.subheader(f'Present Data of table: `{table_name}`')
  st.dataframe(df, use_container_width=True)

  total_count = pd.read_sql(
      f'SELECT COUNT(*) FROM {table_name};', engine
  ).iloc[0, 0]
  st.info(f'Total number of rows sorted in this table: **{total_count:,}**')

except Exception as e:
  st.error(f'An error occurred while connecting to the database: {e}')
