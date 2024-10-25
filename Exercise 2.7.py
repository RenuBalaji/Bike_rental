import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime as dt
from PIL import Image
from numerize import numerize
import matplotlib.pyplot as plt
import seaborn as sns 

# Set up Streamlit
st.set_page_config(page_title='Bike Rental Strategy Dashboard', layout='wide')
st.title('Bike Rental Strategy Dashboard')

# Sidebar for analysis selection
st.sidebar.title('Analysis Sections')
page = st.sidebar.selectbox('Choose an analysis section:', 
                             ['CitiBike Analysis', 
                              'Interactive map Analysis',
                              'Most Frequent Start Stations',
                              'Age Distribution of Users',
                              'Conclusions'])

# CITIBIKES DASHBOARD
if page == 'CitiBike Analysis':
    st.markdown('### Welcome to the CitiBike Strategy Dashboard')
    
    # Load the CitiBike data
    file_path = '/Users/renubalaji/Documents/GitHubProjects/Bike_rental_2018/merged_data_new.csv'
    df = pd.read_csv(file_path)
    
    # INTRO PAGE
    st.markdown('Welcome to the **CitiBike Strategy Dashboard**. This platform provides insights into challenges faced by New York City’s CitiBike program.')

    # WEATHER IMPACT PAGE
    st.header('Weather Impact on Bike Usage')
    
    # Calculate daily bike rides
    df['bike_rides_daily'] = df.groupby('date')['trip_id'].transform('count')
    
    # Aggregate the data by date
    df_aggregated = df.groupby('date').agg({
        'bike_rides_daily': 'mean',  
        'avgTemp': 'mean'
    }).reset_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_aggregated['date'], 
                               y=df_aggregated['bike_rides_daily'], 
                               name='Daily Bike Rides', 
                               line=dict(color='blue')))
    fig2.add_trace(go.Scatter(x=df_aggregated['date'], 
                               y=df_aggregated['avgTemp'], 
                               name='Daily Temperature', 
                               line=dict(color='red')))
    fig2.update_layout(title='Temperature vs Daily Bike Rides (NYC, 2022)', 
                       xaxis_title='Date', 
                       yaxis_title='Daily Bike Rides', 
                       yaxis2=dict(title='Average Temperature (°F)', overlaying='y', side='right'))
    st.plotly_chart(fig2, use_container_width=True)

    # TOP BIKE STATIONS PAGE
    st.header('Top Bike Stations')
    

    # Calculate total rides
    total_rides = df_aggregated ['bike_rides_daily'].sum()
    st.metric(label='Total Bike Rides', value=numerize.numerize(total_rides))  # Closing parenthesis added here
    
    # Print columns for debugging
    st.write("DataFrame columns:", df.columns.tolist())

    # Convert tripduration to numeric
    df['tripduration'] = pd.to_numeric(df['tripduration'], errors='coerce')

    # Drop NaN values
    df = df.dropna(subset=['tripduration'])

    # Group by 'from_station_name' and sum the tripduration
    df_groupby_bar = df.groupby('from_station_name', as_index=False).agg({'tripduration': 'sum'})

    # Get the top 20 stations with the highest trip durations
    top_20 = df_groupby_bar.nlargest(20, 'tripduration')

    # Check the columns
    st.write("Top 20 stations by total trip duration:", top_20)

    # Plot a bar chart
    fig = go.Figure(go.Bar(x=top_20['from_station_name'], y=top_20['tripduration']))

    # Add title and labels
    fig.update_layout(
        title="Top 20 Stations by Total Trip Duration",
        xaxis_title="Station Name",
        yaxis_title="Total Trip Duration (seconds)",
        xaxis_tickangle=-45  # Rotate x-axis labels for better visibility
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Add other analyses here...
    # For example, your previous sections like 'Weather Impact', 'Top Bike Stations', etc.

# DIVVY BIKES DASHBOARD
elif page == 'Divvy Bike Analysis':
    st.markdown('### Welcome to the Divvy Bike Strategy Dashboard')

# Plot a bar chart using the correct column name
    fig = go.Figure(go.Bar(
        x=top_20['from_station_name'],
        y=top_20['tripduration'],  # Use 'tripduration'
        marker=dict(color=top_20['tripduration'], colorscale='Blues')  # Color by tripduration
    ))

    # Add titles and labels
    fig.update_layout(
        title='Top 20 Stations by Total Trip Duration',
        xaxis_title='Station Name',
        yaxis_title='Total Trip Duration (seconds)',  # Specify units
        xaxis_tickangle=-45  # Tilt x-axis labels for better visibility
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # INTERACTIVE MAP PAGE
    st.header('Interactive Map: Aggregated Bike Trips')
    path_to_html = "CitiBike Trips Aggregated.html"
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=1000)

    # CLASSIC VS ELECTRIC BIKES PAGE
    st.header('Classic vs Electric Bikes')
    
    # Check if rideable_type column exists
    if 'rideable_type' not in df.columns:
        st.error("Rideable type column not found in the dataset.")
        st.stop()
        
    classic_bikes = df[df['rideable_type'] == 'classic_bike']
    electric_bikes = df[df['rideable_type'] == 'electric_bike']
    
    hist_classic = go.Histogram(x=classic_bikes['avgTemp'], name='Classic Bike', marker=dict(color='blue'))
    hist_electric = go.Histogram(x=electric_bikes['avgTemp'], name='Electric Bike', marker=dict(color='lightblue'))
    
    fig3 = go.Figure(data=[hist_classic, hist_electric])
    fig3.update_layout(title='Bike Rentals by Temperature (Classic vs Electric)', 
                       xaxis_title='Average Temperature (°F)', 
                       yaxis_title='Rental Frequency', 
                       barmode='overlay')
    st.plotly_chart(fig3)

    # RECOMMENDATIONS PAGE
    st.header('Conclusions and Recommendations')
    bikes = Image.open('CitiBike.jpg')
    st.image(bikes)
    st.markdown('### Recommendations:')
    st.markdown('- **Optimize for Seasonal Demand**: Increase bike availability during warmer months (May-October).')
    st.markdown('- **Focus on Popular Locations**: Add more bikes and parking spaces at high-demand stations.')
    st.markdown('- **Expand Electric Bike Fleet**: Increase the availability of electric bikes to meet consistent demand.')

# Interactive DASHBOARD
elif page == 'Interactive map Analysis':
    st.markdown('### Welcome to the Divvy Bike Strategy Dashboard')
    

   # Load and display the interactive map from the HTML file
    st.header('Interactive Map: Aggregated Divvy Bike Trips')
    path_to_html = "Divvy_Bike_Trips_Aggregated.html"  # Path to your HTML file
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=1000)
    
# MOST FREQUENT START STATIONS TAB
elif page == 'Most Frequent Start Stations':
    st.header('Most Frequent Start Stations')
    
    # Load the CitiBike data again or reuse df if it's available
    file_path = '/Users/renubalaji/Documents/GitHubProjects/Bike_rental_2018/merged_data_new.csv'
    df = pd.read_csv(file_path)
    
    
    # Convert tripduration to numeric and drop NaN values
    df['tripduration'] = pd.to_numeric(df['tripduration'], errors='coerce')
    df = df.dropna(subset=['tripduration'])
    
    # Group by 'from_station_name' and count occurrences
    top20 = df['from_station_name'].value_counts().reset_index()
    top20.columns = ['from_station_name', 'value']
    
    # Create a bar plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top20.head(20), x='value', y='from_station_name', palette='Blues')  # Limit to top 20
    plt.title("Most Frequent Start Stations")
    plt.xlabel("Number of Rides")
    plt.ylabel("Station Name")
    
    # Show the plot in Streamlit
    st.pyplot(plt)
    
# Age Distribution tab
elif page == 'Age Distribution of Users':
    st.header('Age Distribution of Users')
    
    # Load the CitiBike data again or reuse df if it's available
    file_path = '/Users/renubalaji/Documents/GitHubProjects/Bike_rental_2018/merged_data_new.csv'
    df = pd.read_csv(file_path)
    
    sns.set_style('darkgrid')
    fig_age = plt.figure(figsize=(9, 5))
    sns.histplot(df['birthyear'], bins=15, kde=True)
    plt.title("Distribution of Users' Ages")
    plt.xlabel("Birth year")
    plt.ylabel("Frequency")
    st.pyplot(fig_age)
    
# Conclusions
else:
    st.header('Conclusions')
    
    st.markdown('- Our analysis indicates that there is no particular seasonality which impacts the rides in particular')
    st.markdown('- The Canal St & Adams St has the highest trip duration amongst all')
    st.markdown('- The Canal St & Adams St is also the most frequent start station')