#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'yearly'},
    {'label': 'Recession Period Statistics', 'value': 'recession'}
]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard", style={'textAlign': 'left', 'color': '#503D36', 'font-size': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='select-statistics',
            options=dropdown_options,
            value='yearly',
            placeholder='Select Statistics...'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value=1980,
            placeholder='Select Year...'
        )
    ]),
    html.Div(id='output-container', className='output-container', style={'margin-top': '20px'})
])

# Define the callback function to update the output container based on the selected statistics
@app.callback(
    Output('output-container', 'children'),
    [Input('select-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'recession':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period"))

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle')['Automobile_Sales'].mean().reset_index()
        chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle', y='Automobile_Sales', title="Average Vehicles Sold by Vehicle Type during Recession"))

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle')['Total_Expenditure'].sum().reset_index()
        chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Total_Expenditure', names='Vehicle', title='Total Expenditure Share by Vehicle Type during Recession'))

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        # (Assuming 'Unemployment_Rate' is a column in your dataset)
        chart4 = dcc.Graph(figure=px.bar(recession_data, x='Vehicle', y='Automobile_Sales', color='Unemployment_Rate', title='Effect of Unemployment Rate on Vehicle Type and Sales during Recession'))

        return [html.Div(className='chart-item', children=[chart1, chart2], style={'margin-bottom': '30px'}),
                html.Div(className='chart-item', children=[chart3, chart4], style={'margin-bottom': '30px'})]
    
    elif selected_statistics == 'yearly':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yearly_sales = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(yearly_sales, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales'))

        # Plot 2: Total Monthly Automobile sales using line chart
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        chart2 = dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avg_vehicles = yearly_data.groupby('Vehicle')['Automobile_Sales'].mean().reset_index()
        chart3 = dcc.Graph(figure=px.bar(avg_vehicles, x='Vehicle', y='Automobile_Sales', title=f'Average Vehicles Sold by Vehicle Type in {input_year}'))

        # Plot 4: Pie chart for total advertisement expenditure for each vehicle
        exp_share = yearly_data.groupby('Vehicle')['Total_Expenditure'].sum().reset_index()
        chart4 = dcc.Graph(figure=px.pie(exp_share, values='Total_Expenditure', names='Vehicle', title=f'Total Advertisement Expenditure for Each Vehicle in {input_year}'))

        return [html.Div(className='chart-item', children=[chart1, chart2], style={'margin-bottom': '30px'}),
                html.Div(className='chart-item', children=[chart3, chart4], style={'margin-bottom': '30px'})]
    
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
