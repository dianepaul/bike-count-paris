import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# Title for the app
st.title("Data Visualization Streamlit App")

# Sidebar: File Upload, Date Column Selection, and Plot Type Selection
st.sidebar.header("Data Settings")

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Plot Type Selection
plot_type = st.sidebar.selectbox("Select a plot type", ["Line Plot", "Bar Chart", "Scatter Plot"])

# Date Filter
date_filter = st.sidebar.checkbox("Enable Date Filter")

# Main Content
if uploaded_file is not None:
    # Load the data
    data = pd.read_csv(uploaded_file)

    # Get the column names from the uploaded dataset
    column_names = data.columns.tolist()

    # Dropdown for Date Column Selection
    date_column = st.sidebar.selectbox("Select the Date Column", column_names)

    # Dropdowns for X and Y Columns
    x_column = st.selectbox("Select the X-axis column", column_names)
    y_column = st.selectbox("Select the Y-axis column", column_names)

    #Convert the selected date column to datetime if needed
    if date_column:
        data[date_column] = pd.to_datetime(data[date_column])

    # Set start_date and end_date to the minimum and maximum dates in the date column
    if date_column and not data.empty:
        min_date = data[date_column].min()
        max_date = data[date_column].max()
        start_date = st.sidebar.date_input("Start Date", min_date)
        end_date = st.sidebar.date_input("End Date", max_date)
    
    # Convert start_date and end_date to datetime objects
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.min.time())

    # Apply date filter if enabled
    if date_filter:
        data = data[(data[date_column] >= start_date) & (data[date_column] <= end_date)]

    # Display the raw data
    st.subheader("Raw Data")
    st.write(data)

    # Data Visualization
    st.subheader("Data Visualization")

    if plot_type == "Line Plot":
        # Specify X and Y columns explicitly
        st.line_chart(data.set_index(x_column)[y_column])
    elif plot_type == "Bar Chart":
        # Create a custom bar chart using Matplotlib
        plt.figure(figsize=(12, 6))
        plt.bar(data[x_column], data[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f"Bar Chart: {x_column} vs. {y_column}")
        st.pyplot(plt)
    elif plot_type == "Scatter Plot":
        if st.button("Create Scatter Plot"):
            scatter_plot = sns.scatterplot(data=data, x=x_column, y=y_column)
            st.pyplot(plt)
