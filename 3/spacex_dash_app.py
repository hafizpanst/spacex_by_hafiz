# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


def create_options(spacex_df):
    result = spacex_df["Launch Site"].unique()
    list_r = []
    for r in result:
        list_r += [{
            "label" : r,
            "value" : r,
        }]
    return list_r


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {"label" : "All Sites",
            "value" : "ALL",}
        ] + create_options(spacex_df),
        value="ALL",
        placeholder="Select a Launch Site Here",
        searchable=True,
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id="success-pie-chart", component_property="figure"), Input(component_id="site-dropdown", component_property="value"))
def create_pie_chart(input):
    print("creating pie chart of {}".format(input))
    if input=="ALL":
        a = spacex_df.copy()
        output = px.pie(a, values="class", names="Launch Site")
    else:
        a = spacex_df[spacex_df["Launch Site"]==input]
        output = px.pie(a, values="Flight Number", names="class")
    return output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), [Input(component_id='site-dropdown', component_property='value'),Input(component_id="payload-slider", component_property="value")])
def success_payload_scatter(site_dropdown, payload_slider):
    print(site_dropdown, payload_slider, type(site_dropdown), type(payload_slider))
    if site_dropdown == "ALL":
        a = spacex_df[(spacex_df["Payload Mass (kg)"]>=float(payload_slider[0]))&(spacex_df["Payload Mass (kg)"]<=float(payload_slider[1]))]
        
    else:
        a = spacex_df[(spacex_df["Payload Mass (kg)"]>=float(payload_slider[0]))&(spacex_df["Payload Mass (kg)"]<=float(payload_slider[1]))]
        a = a[a["Launch Site"]==site_dropdown]
    
    output = px.scatter(a, "Payload Mass (kg)", "class", color="Booster Version Category")
    return output


# Run the app
if __name__ == '__main__':
    app.run_server()