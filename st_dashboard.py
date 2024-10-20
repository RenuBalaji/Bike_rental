import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 
st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')

st.title("Divvy Bikes Strategy Dashboard")

st.markdown("The dashboard will help with the expansion problems Divvy currently faces")

df = pd.read_csv('merged_data_new.csv', index_col = 0)
top_20 = pd.read_csv('top20.csv', index_col = 0)

# ########################### DEFINE THE CHARTS ############################


## Bar chart 

# Group by 'from_station_name' and sum the 'tripduration' for each station
df_groupby_bar = df.groupby('from_station_name', as_index=False).agg({'tripduration': 'sum'})

# Check the data type of tripduration
print(df_groupby_bar['tripduration'].dtype)

# Convert tripduration to numeric if it's not already
df_groupby_bar['tripduration'] = pd.to_numeric(df_groupby_bar['tripduration'], errors='coerce')

# Drop rows with NaN values in tripduration
df_groupby_bar = df_groupby_bar.dropna(subset=['tripduration'])

# Get the top 20 stations with the highest trip durations
top_20 = df_groupby_bar.nlargest(20, 'tripduration')

# Display the result
print(top_20)

df['tripduration'] = pd.to_numeric(df['tripduration'], errors='coerce')

# Assuming 'df' is your DataFrame and it has been cleaned as discussed earlier

# Group by 'from_station_name' and sum the 'tripduration' for each station
df_groupby_bar = df.groupby('from_station_name', as_index=False).agg({'tripduration': 'sum'})

# Get the top 20 stations with the highest trip durations
top_20 = df_groupby_bar.nlargest(20, 'tripduration')

# Display the result
print(top_20)

# Convert tripduration to numeric
df['tripduration'] = pd.to_numeric(df['tripduration'], errors='coerce')

# Drop NaN values
df = df.dropna(subset=['tripduration'])

# Group by 'from_station_name' and sum the tripduration
df_groupby_bar = df.groupby('from_station_name', as_index=False).agg({'tripduration': 'sum'})

# Get the top 20 stations with the highest trip durations
top_20 = df_groupby_bar.nlargest(20, 'tripduration')

# Check the columns
print(top_20.columns)

# Plot a bar chart
fig = go.Figure(go.Bar(x=top_20['from_station_name'], y=top_20['tripduration']))

# Add title and labels
fig.update_layout(
    title="Top 20 Stations by Total Trip Duration",
    xaxis_title="Station Name",
    yaxis_title="Total Trip Duration (seconds)",
    xaxis_tickangle=-45  # Optional: Rotate x-axis labels for better visibility
)
st.plotly_chart(fig, use_container_width = True)


import plotly.graph_objects as go

# Check the columns in top_20 to confirm what they are
print(top_20.columns)

# Plot a bar chart using the correct column name
fig = go.Figure(go.Bar(
    x=top_20['from_station_name'],
    y=top_20['tripduration'],  # Change 'value' to 'tripduration'
    marker=dict(color=top_20['tripduration'], colorscale='Blues')  # Optional: color by tripduration
))

# Add titles and labels
fig.update_layout(
    title='Top 20 Stations by Total Trip Duration',
    xaxis_title='Station Name',
    yaxis_title='Total Trip Duration (seconds)',  # or whatever unit you're using
    xaxis_tickangle=-45  # Optional: tilt x-axis labels for better visibility
)

st.plotly_chart(fig, use_container_width = True)

fig.update_layout(
     title = 'Top 20 most popular bike stations in Chicago',
     xaxis_title = 'Start stations',
     yaxis_title ='Sum of trips',
     width = 900, height = 600)

st.plotly_chart(fig, use_container_width = True)


# Path to your HTML file
html_file_path = 'Divvy_Bike_Trips_Aggregated.html'  # Adjust the path if necessary

# Read the HTML file
with open(html_file_path, 'r') as f:
    html_content = f.read()

# Display the HTML content in Streamlit
st.components.v1.html(html_content, height=600)  # Adjust height as needed