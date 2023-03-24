import dash
from dash import Dash, dash_table, Input, Output, callback
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url


import pandas as pd
import plotly.graph_objs as go

# data processing
df = pd.read_csv('deaths-drug-overdoses.csv')


# Requiremnets for dash components
country_options = [
    {'label': 'Country Portugal', 'value': 'Portugal'},
    {'label': 'Country Spain', 'value': 'Spain'},
    {'label': 'Country France', 'value': 'France'}
]
"""
Equivalent way to iteratively build country_options from the dataset's countries:

country_options = [
    dict(label='Country ' + country, value=country)
    for country in df['country_name'].unique()]
 
 Try it out!
"""

drug_options = [
    {'label': 'Opiods', 'value': 'Deaths - Opioid use disorders - Sex: Both - Age: All Ages (Number)'},
    {'label': 'Other Drugs', 'value': 'Deaths - Other drug use disorders - Sex: Both - Age: All Ages (Number)'},
    {'label': 'Amphetamine', 'value': 'Deaths - Amphetamine use disorders - Sex: Both - Age: All Ages (Number)'},
    {'label': 'Cocaine', 'value': 'Deaths - Cocaine use disorders - Sex: Both - Age: All Ages (Number)'}
]


# APP

app = dash.Dash(__name__)

app.layout = html.Div([


    html.H2('Drug Report'),

    dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    ),

    html.Br(),

    dcc.RadioItems(
        id='drug_radio',
        options=drug_options,
        value='Deaths - Opioid use disorders - Sex: Both - Age: All Ages (Number)'
    ),

    dcc.Graph(id='graph_example'),

    html.Br(),

    dcc.RangeSlider(
        id='year_slider',
        min=1990,
        max=2019,
        value=[1990, 2019],
        marks={'1990': 'Year 1990',
               '1995': 'Year 1995',
               '2000': 'Year 2000',
               '2005': 'Year 2005',
               '2010': 'Year 2010',
               '2015': 'Year 2015',
               '2019': 'Year 2019'},
        step=1
    )
])


@app.callback(
    Output('graph_example', 'figure'),
    [Input('country_drop', 'value'),
     Input('drug_radio', 'value'),
     Input('year_slider', 'value')]
)
def update_graph(countries, drug, year):
    filtered_by_year_df = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['Entity'] == country]

        temp_data = dict(
            type='scatter',
            y=filtered_by_year_and_country_df[drug],
            x=filtered_by_year_and_country_df['Year'],
            name=country
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Year'),
                          yaxis=dict(title=drug)
                          )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)

    return fig


if __name__ == '__main__':

    app.run_server(debug=True)
