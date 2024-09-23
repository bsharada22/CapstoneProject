import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a Dash application
app = dash.Dash(__name__)

# Define min and max values for the RangeSlider
min_value = 0
max_value = 10000  # Adjust based on your dataset

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown for site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        ],
        value='ALL',  # Default value
        placeholder='Select a Site',
        searchable=True
    ),
     # Pie chart for successful launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    # RangeSlider for Payload Mass
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=max_value,
        step=500,
        marks={i: str(i) for i in range(0, max_value + 1, 1000)},
        value=[0, max_value]
    ),

    
   
    # Scatter plot for payload vs. launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    launch_counts = spacex_df.groupby('Launch Site')['class'].value_counts().unstack(fill_value=0)
    launch_counts = launch_counts.reset_index()  # Prepare for plotting
    launch_counts = launch_counts[['Launch Site', 1]]  # Get successful launches only
    
    fig_all = px.pie(launch_counts, names='Launch Site', values=1, 
                     title='Successful Launches from Each Site')
    
    if selected_site != 'ALL':
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        
        success_count = site_data['class'].value_counts().get(1, 0)
        failure_count = site_data['class'].value_counts().get(0, 0)

        pie_data = pd.DataFrame({
            'Status': ['Success', 'Failure'],
            'Count': [success_count, failure_count]
        })

        fig_site = px.pie(pie_data, names='Status', values='Count',
                          title=f'Success vs. Failure for {selected_site}',
                          labels={'Status': 'Launch Status'},
                          hole=0.3)  # This makes it a donut chart (optional)
        
        return fig_site
    else:
        return fig_all

# Callback for the scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, payload_range):
    min_payload, max_payload = payload_range

    # Filter DataFrame based on selected site and payload range
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                                 (spacex_df['Payload Mass (kg)'] <= max_payload)]
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                 (spacex_df['Payload Mass (kg)'] >= min_payload) & 
                                 (spacex_df['Payload Mass (kg)'] <= max_payload)]
    
    # Create the scatter plot
    fig_scatter = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs. Launch Success',
        labels={'class': 'Launch Outcome (0 = Failure, 1 = Success)'}
    )

    return fig_scatter

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
