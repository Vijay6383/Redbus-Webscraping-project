# import necessary modules
import streamlit as st
import sqlite3
import pandas as pd


st.logo("redbus.png")

# connect to our stored database
con = sqlite3.connect("redbusDB.db")

# get all data from the bus_routes table in Dataframe using pandas Sql 
df = pd.read_sql_query('select * from bus_routes;',con)

# dictionary of price ranges for each options 
price_options = {
    'All': (0, 9999),
    'less than 500' : (0, 500),
    '500 to 800': (500, 800),
    'more than 800': (800, 9999)
}

# dictionary of star rating ranges for each options 
rating_options = {
    'All': (0, 6),
    '0 to 2': (0, 2),
    '2 to 4': (2, 4),
    '4 to 5': (4, 6)
}

# dictionary of seat availability ranges for each options 
Seat_Options = {
    'All': (0,999),
    '0 to 10': (0, 10),
    '10 to 20': (10, 20),
    '20 to 40': (20, 40),
    'more than 40': (40, 999)
}

#sessios state for dynamic filtering
if 'Bus_Type' not in st.session_state:
    st.session_state['Bus_Type'] = []

if 'Bus_Route' not in st.session_state:
    st.session_state['Bus_Route'] = ''

if 'df_filtered' not in st.session_state:
    st.session_state['df_filtered'] = pd.DataFrame()
# ---Side Bar---

st.sidebar.image("redbus.png")

st.sidebar.header("Filter Buses here:")

# filter widget for bus type
Bus_Type = st.sidebar.multiselect(
    "Select Bus Type:",
    options=df['bustype'].unique(),
    default=df['bustype'].unique()
)

# filter widget for bus_routes
Bus_Route = st.sidebar.selectbox(
    "Select Bus Route:",
    options=df['route_name'].unique()
)

# filter widget for price range
selected_range = st.sidebar.selectbox(
    "Select Price Range:",
    list(price_options.keys())
)

# filter widget for Star ratings
selected_rating = st.sidebar.selectbox(
    "Select Bus Rating:",
    list(rating_options.keys())
)

# filter widget for seat availability
selected_seatrange = st.sidebar.selectbox(
    "Select the available seat range:",
    list(Seat_Options.keys())
) 

# filters table based on selected Bus_route
if not Bus_Route:
    st.error("Please select atleast one route")
else:
    st.session_state['Bus_Route'] = Bus_Route
    # st.session_state['df_filtered'] = df[df['route_name'].isin(st.session_state['Bus_Route'])]
    st.session_state['df_filtered'] = df[df['route_name']==st.session_state['Bus_Route']]

# filters table based on selected Bus_type
if Bus_Type:
    st.session_state['Bus_Type'] = Bus_Type
    st.session_state['df_filtered'] = st.session_state['df_filtered'][st.session_state['df_filtered']['bustype'].isin(st.session_state['Bus_Type'])]
    

# filters table based on selected price range
if selected_range:
    min_value, max_value = price_options[selected_range]
    st.session_state['df_filtered'] = st.session_state['df_filtered'][(st.session_state['df_filtered']['price']>=min_value) & (st.session_state['df_filtered']['price']<max_value)]
    

# filters table based on selected star rating
if selected_rating:
    min_value, max_value = rating_options[selected_rating]
    st.session_state['df_filtered'] = st.session_state['df_filtered'][(st.session_state['df_filtered']['star_rating']>=min_value) & (st.session_state['df_filtered']['star_rating']<max_value)]
    

# filters table based on selected seat availability
if selected_seatrange:
    min_value, max_value = Seat_Options[selected_seatrange]
    st.session_state['df_filtered'] = st.session_state['df_filtered'][(st.session_state['df_filtered']['seats_available']>=min_value) & (st.session_state['df_filtered']['seats_available']<max_value)]
    


# ---Main Page---
st.header("RedBus Data Table:")

# display Data Table
st.dataframe(st.session_state['df_filtered'],1200)

# visualization of total buses for a particular Price for a specific Route
st.bar_chart(st.session_state['df_filtered']['price'].value_counts(), x_label='Prices', y_label='no_of_buses')