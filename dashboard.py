import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

conn = sqlite3.connect('sentiments.db')
df = pd.read_sql("SELECT * FROM reviews", conn)

st.title("Product Sentiment Dashboard")
product = st.selectbox("Select Product", df['product'].unique())

col_df = df[df['product'] == product]
fig = px.bar(col_df, x='label', y='score', color='label', title=f"{product} Sentiment")
st.plotly_chart(fig)

st.dataframe(col_df.tail(10))  # Recent reviews
