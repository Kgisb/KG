#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
from ipywidgets import widgets, interact

# Load Google Sheet data (publicly accessible)
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
data = pd.read_csv(sheet_url)

# Ensure the Date column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Function for filtering and visualization
def filter_data(ac_name="All", start_date=None, end_date=None):
    filtered_data = data.copy()

    # Filter by AC Name if not "All"
    if ac_name != "All":
        filtered_data = filtered_data[filtered_data['AC Name'] == ac_name]

    # Filter by date range if specified
    if start_date and end_date:
        filtered_data = filtered_data[
            (filtered_data['Date'] >= pd.to_datetime(start_date)) &
            (filtered_data['Date'] <= pd.to_datetime(end_date))
        ]
    
    # Aggregated metrics
    summary = filtered_data.groupby('AC Name').agg({
        'Cash-in': 'sum',
        'Enrl': 'sum',
        'SGR Conversion': 'sum',
        'Fresh Leads': 'sum',
        'SGR Leads': 'sum',
        'Overall Leads': 'sum'
    }).reset_index()

    # Interactive chart
    fig = px.bar(summary, x='AC Name', y=['Cash-in', 'Enrl', 'SGR Conversion'], barmode='group',
                 title="Performance Metrics by AC")
    fig.show()

    return filtered_data

# Create interactive widgets
ac_name_widget = widgets.Dropdown(
    options=["All"] + data['AC Name'].unique().tolist(),
    value="All",
    description="AC Name:"
)

start_date_widget = widgets.DatePicker(
    description="Start Date:",
    disabled=False
)

end_date_widget = widgets.DatePicker(
    description="End Date:",
    disabled=False
)

# Interactive dashboard
def interactive_dashboard(ac_name, start_date, end_date):
    filtered_data = filter_data(ac_name, start_date, end_date)
    display(filtered_data)

interact(
    interactive_dashboard,
    ac_name=ac_name_widget,
    start_date=start_date_widget,
    end_date=end_date_widget
)


# In[ ]:




