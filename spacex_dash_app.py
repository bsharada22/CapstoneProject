# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCA4SLC-40', 'value': 'CCA4SLC-40'},
            {'label': 'CCA4SSLC-40', 'value': 'CCA4SSLC-40'},
            {'label': 'KSLC-39A', 'value': 'KSLC-39A'},
            {'label': 'VAFBSLC-4E', 'value': 'VAFBSLC-4E'},
        ],
        value='ALL',  # Default value
        placeholder='Select a Site',  # Placeholder text
        searchable=True
    ),

    html.Br(),  # Line break

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),  # Line break

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
  min_payload = int(spacex_df['Payload Mass (kg)'].min())
max_payload = int(spacex_df['Payload Mass (kg)'].max())

# Updated RangeSlider
dcc.RangeSlider(
    id='payload-slider',
    min=min_payload,
    max=max_payload,
    step=1000,
    value=[min_payload, max_payload],  # Default range
    marks={i: str(i) for i in range(min_payload, max_payload + 1, 1000)}  # Now this will work
),


    html.Br(),  # Line break

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: 
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    # Implement the logic to update the pie chart based on the selected site
    pass  # Replace with your code

# TASK 4: 
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Implement the logic to update the scatter chart based on the selected site and payload range
    pass  # Replace with your code

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
