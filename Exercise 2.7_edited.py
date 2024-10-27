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

# Load the CitiBike data once at the beginning
file_path = '/Users/renubalaji/Documents/GitHubProjects/Bike_rental_2018/merged_data_new.csv'
df = pd.read_csv(file_path)

# Sidebar for analysis selection
st.sidebar.title('Analysis Sections')
page = st.sidebar.selectbox('Choose an analysis section:', 
                             ['CitiBike Analysis', 
                              'Interactive map Analysis',
                              'Most Frequent Start Stations',
                              'Age Distribution of Users',
                              'Conclusions and Recommendations'])

# CITIBIKES DASHBOARD
if page == 'CitiBike Analysis':
    st.markdown('### Welcome to the CitiBike Strategy Dashboard')
    
    myImage = Image.open("Commuter Bicycle Park.jpg")
    st.image(myImage) 
    
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
    total_rides = df_aggregated['bike_rides_daily'].sum()
    st.metric(label='Total Bike Rides', value=numerize.numerize(total_rides))  # This is your original code

    # Check the columns for debugging
    st.write("DataFrame columns:", df.columns)

    # Convert tripduration to numeric
    df['tripduration'] = pd.to_numeric(df['tripduration'], errors='coerce')

    # Drop NaN values in tripduration
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
    
    # Add observations
    st.markdown("### Observations")
    st.markdown("""
    - **Canal St & Adams St** is the most popular station in terms of trip duration, indicating a high volume of bike usage or longer trip times associated with this location.
    - **Clinton St & Washington Blvd** and **Clinton St & Madison St** also rank highly, suggesting that these areas are significant for bike traffic, potentially due to popular destinations or major transit hubs nearby.
    - The top 5 stations contribute to a substantial portion of the total trip duration, highlighting areas of high demand.
    - Observing high-demand stations can help in decision-making for maintenance and expansion, as these locations might benefit from additional resources or more bikes available for rent.
    """)


# DIVVY BIKES DASHBOARD
elif page == 'Divvy Bike Analysis':
    st.markdown('### Welcome to the Divvy Bike Strategy Dashboard')
    
# Interactive Map Analysis
elif page == 'Interactive map Analysis':
    st.header('Interactive Map: Aggregated Bike Trips')
    path_to_html = "Divvy_Bike_Trips_Aggregated.html"
    with open(path_to_html, 'r') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=1000)

# MOST FREQUENT START STATIONS TAB
elif page == 'Most Frequent Start Stations':
    st.header('Most Frequent Start Stations')
    
    # Calculate most frequent start stations
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
    
    # Observations
    st.header("Observations")
    st.markdown("""
    - **Canal St & Adams St** is the most frequently used start station, followed closely by **Clinton St & Washington Blvd** and **Clinton St & Madison St**. These stations likely serve as key hubs in areas with high commuter or tourist traffic.
    - **Top 5 Stations**: The top five stations dominate in ride counts, each with over 4,000 rides. This indicates these locations might benefit from more bike availability to meet demand.
    - **Centralized Demand**: The concentration of high-frequency stations suggests that demand is centralized in specific areas, likely around business districts or popular neighborhoods.
    - **Consistent Patterns**: There is a steady decrease in frequency after the top 5 stations, indicating that while some stations are highly popular, a larger number see moderate but steady usage.
    - **Implications for Expansion**: Expanding or placing additional bikes at high-frequency stations could improve service efficiency and user satisfaction, particularly in peak hours when bikes might be scarce.
    """)


# Age Distribution tab
elif page == 'Age Distribution of Users':
    st.header('Age Distribution of Users')
    
    sns.set_style('darkgrid')
    fig_age = plt.figure(figsize=(9, 5))
    sns.histplot(df['birthyear'], bins=15, kde=True)
    plt.title("Distribution of Users' Ages")
    plt.xlabel("Birth year")
    plt.ylabel("Frequency")
    st.pyplot(fig_age)
    
    # Observations for Age Distribution of Users
    st.header("Observations")
    st.markdown("""
    - **Peak Age Range**: Most users were born between 1970 and 2000, indicating a strong preference for bike rentals among users aged approximately 20 to 50.
    - **Younger Demographic**: There is a peak around 1980-1990, suggesting that bike rentals are particularly popular among users in their 30s and 40s.
    - **Older Users**: There are fewer users born before 1950, indicating that the service may be less popular among older demographics.
    - **Potential Target for Marketing**: Given the popularity among users under 50, marketing efforts could be targeted toward younger professionals and city commuters.
    - **Opportunity for Accessibility Improvements**: Given the lower usage among older age groups, adding accessible options might encourage a more diverse age range of users.
    """)

# Conclusions
else:
    
    st.header("Conclusions")
    st.markdown("""
    1. **Top Bike Stations**:
    - High bike usage is concentrated around specific stations such as "Canal St & Adams St" and "Clinton St & Washington Blvd". These are likely high-traffic areas that serve as popular entry/exit points for commuters or tourists.
    - Total trip durations are highest for these stations as well, indicating a substantial demand for bikes in these areas.

    2. **User Age Distribution**:
    - The majority of users fall within the age range of 20-50, with a peak around ages 30-40, suggesting that the service is highly popular among young adults and middle-aged commuters.
    - Users over the age of 50 are less frequent, which could indicate that the service is not as appealing to older age groups.

    3. **Trip Duration Patterns**:
    - Some stations experience longer trip durations on average, potentially indicating either longer commute routes or areas with greater traffic congestion.

    4. **Frequent Start Stations**:
    - Stations such as "Canal St & Adams St" and "Clinton St & Washington Blvd" also appear as frequent start stations, aligning with their high usage for total trip duration and suggesting that they are key hubs in the network.
    """)

# Recommendations based on data insights
    st.header("Recommendations")
    st.markdown("""
    1. **Increase Bike Availability at High-Demand Stations**:
    - To meet demand, add more bikes at "Canal St & Adams St", "Clinton St & Washington Blvd", and other frequently used stations during peak hours.
    - Implement real-time bike tracking at these stations to ensure bikes are available when needed.

    2. **Targeted Marketing for Younger Age Groups**:
    - With most users aged between 20 and 50, focus marketing efforts on young professionals and city commuters.
    - Consider introducing discounts or membership benefits for users in this age range to encourage frequent use.

    3. **Accessibility Enhancements for Older Users**:
    - Given the lower usage among older age groups, introduce op""")
