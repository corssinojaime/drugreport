import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import plotly.express as px
import pandas as pd
import numpy as np
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc

deaths = pd.read_csv('deaths-drug-overdoses.csv')

# fig = px.bar(deaths, x = 'Year', y='Deaths - Opioid use disorders - Sex: Both - Age: All Ages (Number)', color='Entity')
df = px.data.gapminder()
years = deaths.Year.unique()
countries = deaths.Entity.unique()

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/dbc.min.css"])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])


drugs_list = ['Opioid','Cocaine','Amphetamine','Other']

deaths_colnames = {
    'Deaths - Opioid use disorders - Sex: Both - Age: All Ages (Number)': drugs_list[0],
    'Deaths - Cocaine use disorders - Sex: Both - Age: All Ages (Number)': drugs_list[1],
    'Deaths - Other drug use disorders - Sex: Both - Age: All Ages (Number)': drugs_list[3],
    'Deaths - Amphetamine use disorders - Sex: Both - Age: All Ages (Number)': drugs_list[2]
}

deaths.rename(columns=deaths_colnames, inplace=True)

xdeaths = deaths.reset_index()
deaths = pd.melt(xdeaths, id_vars=['Entity', 'Code', 'Year'], value_vars=drugs_list)

deaths = deaths.rename(columns={'variable': 'drug',
                                'value': 'total'})


euro_countries = ['Austria','Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
                  'Denmark','Estonia','Finland','France','Germany','Greece','Hungary',
                  'Ireland','Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands',
                  'Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden']

deaths['euro'] = deaths["Entity"].isin(euro_countries) * 1


euro_drugs = deaths[deaths['euro']==1].groupby(['euro', 'Entity','drug'])['total'].sum().reset_index()
euro_drugs['perc'] = 100 * euro_drugs['total'] / euro_drugs.groupby(['euro', 'Entity'])['total'].transform('sum')


header = html.H4(
    "Drugs Report in Europe", className="bg-primary text-white p-2 mb-2 text-leftcenter"
)

table = html.Div(
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True}
                 for i in deaths.columns],
        data=df.to_dict("records"),
        page_size=10,
        editable=True,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        row_selectable="multi",
    ),
    className="dbc-row-selectable",
)


radio_drugs = dbc.RadioItems(
    id='drug_type',
    className='radio',
    options=[dict(label='Opioid', value=0),
             dict(label='Cocaine', value=1),
             dict(label='Amphetamine', value=2)
             #dict(label='Other', value=3),
             #dict(label='All Drugs', value=3)
             ],
    value=0,
    inline=True
)
buttons = html.Div(
    [
        dbc.Button(
            "Primary", color="primary", className="me-1"
        ),
        html.Span(id="example-output", style={"verticalAlign": "middle"}),

    ]
)

dropdown_drugs = html.Div([
    dbc.Label("Select Drug Type"),
    dcc.Dropdown(
        id="drug_type",
        options=[{"label": i, "value": i} for i in deaths_colnames.values()],
        value=None,
        multi=False,
        clearable=False
    )],
    className="mb-4",
)


drop_continent = dcc.Dropdown(
    id='drop_continent',
    clearable=False,
    searchable=False,
    options=[{'label': 'World', 'value': 'world'},
             {'label': 'Europe', 'value': 'europe'},
             {'label': 'Asia', 'value': 'asia'},
             {'label': 'Africa', 'value': 'africa'},
             {'label': 'North america', 'value': 'north america'},
             {'label': 'South america', 'value': 'south america'}],
    value='world',
    style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a',
           'border-color': '#ebb36a'}
)

drop_country = dcc.Dropdown(
        id = 'drop_country',
        options=[{"label": i, "value": i} for i in euro_countries],
        multi=True,
        value=['Portugal'],
        clearable=False,
        #searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )


slider_map = html.Div(
    [
        dbc.Label("Select Year"),
        dcc.RangeSlider(
            min(deaths.Year.unique()),
            max(deaths.Year.unique()),
            5,
            id="slider_years",
            marks={str(i): str(i) for i in range(min(deaths.Year.unique()), max(deaths.Year.unique()), 5)},           
            tooltip={"placement": "bottom", "always_visible": True},
            value=[min(deaths.Year.unique()), max(deaths.Year.unique())],
            className="p-0",
        ),
    ],
    className="mb-4",
)



badge = dbc.Button(
    [
        "Notifications",
        dbc.Badge("4", color="warning",
                  text_color="primary", className="ms-1"),
    ],
    color="primary",
)


fig_drugs = px.sunburst(euro_drugs, path = ['Entity','drug'], values = 'perc', 
                    color = 'drug', color_discrete_sequence = px.colors.sequential.Peach_r).update_traces(hovertemplate = '%{label}<br>' + 'Global Grugs: %{value}%', textinfo = "label + percent entry") 

fig_drugs = fig_drugs.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),
                        'paper_bgcolor': '#F9F9F8',
                        'font_color':'#363535'})



##############################################
################### LAYOUT ###################
##############################################


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    # html.Div([
    # html.Div([


         html.Div([                   
                html.Label("Drug Report in Europe Countries", className='header_label'),
                ], className='header', style={'width': '97%', 'padding-bottom': '10px'}),

    html.Div([



        html.Div([
            
            html.Div([

                html.Div([                   
                    html.Label(id='title_map', style={'font-size': 'medium'}),

                ], style={'width': '70%'}),
                
                html.Div([
                    drop_continent,
                    html.Br(),
                   
                ], style={'width': '45%', 'font-size': '13px'}),
            ], className='row'),
             html.Br(),
             html.Br(),

            dcc.Graph(id='map', style={'position': 'relative', 'top': '-50px'}),

            html.Div([
                slider_map,                
            ], style={'margin-right': '15%', 'position': 'relative', 'top': '-30px'}),

        ], className='box', style={'width': '50%', 'padding-bottom': '0px'}),

        html.Div([
            html.Label("2. Title here", style={'font-size': 'medium'}),
            html.Br(),
            radio_drugs,
            html.Div([
                    html.Label(id='choose_country', style= {'margin': '10px'}),
                    drop_country,
                    ], style={'width': '100%'}),
            #html.Br(),            
            html.Br(),
            dcc.Graph(id='plt_lines')
        ], className='box', style={'width': '50%'}),
    ], className='row'),

    html.Div([
        html.Div([
            html.Label("3. Title here", style={'font-size': 'medium'}),
            html.Br(),
            html.Label('Click on it to know more!',
                       style={'font-size': '9px'}),
            html.Br(),
            html.Br(),
            dcc.Graph(figure=fig_drugs)
        ], className='box', style={'width': '53%'}),
        html.Div([
            html.Label("4. Title here", style={'font-size': 'medium'}),
            html.Br(),
            html.Label('Click on it to know more!',
                       style={'font-size': '9px'}),
            html.Br(),
            html.Br(),
             dcc.Graph(id = 'first_graph')
        ], className='box', style={'width': '50%'}),
    ], className='row'),

    html.Div([
        html.Div([
            html.P(['Group name', html.Br(), 'Names'],
                   style={'font-size': '12px'}),
        ], style={'width': '60%'}),
        html.Div([
            html.P(['Sources ', html.Br(), html.A('Our World in Data', href='https://ourworldindata.org/', target='_blank'), ', ', html.A(
                'Food and Agriculture Organization of the United Nations', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'font-size': '12px'})
        ], style={'width': '37%'}),
    ], className='footer', style={'display': 'flex'}),
    # ], className='main'),
    # ]),
])


@app.callback(
    [
        Output('title_map', 'children'),
        #Output('choose_country','children'),
        Output('map', 'figure')
    ],
    [
        #Input('drop_map', 'value'),
        Input('slider_years', 'value'), 
        Input('drop_continent', 'value'),
        Input('drug_type', 'value')
    ],
    #[State("drop_map","options")]
)

def update_map(year, continent, drug):

    drug_label = ''
    if drug == 0:
        drug_label = 'Opioid'
    if drug == 1:
        drug_label = 'Cocaine'
    if drug == 2:
        drug_label = 'Amphetamine'

    
    death_sub = deaths[(deaths['drug'] == drug_label) & (deaths['Year'].isin(year))]

    print("Begin", continent," droga ", drug, "label: ", drug_label, "shape....", death_sub.shape)

    title ='Number of deaths caused by {} drug '.format(death_sub['drug'].unique()[0])  #font_color = '#363535',
    data_slider = []
    data_each_yr = dict(type='choropleth',
                        locations = death_sub['Entity'],
                        locationmode='country names',
                        autocolorscale = False,
                        z=np.log(death_sub['total'].astype(float)),
                        zmin=0, 
                        zmax = np.log(deaths[deaths['drug']== drug_label]['total'].max()),
                        colorscale = ["#ffe2bd", "#006837"],   
                        marker_line_color= 'rgba(0,0,0,0)',
                        colorbar= {'title':'Tonnes (log)'},#Tonnes in logscale
                        colorbar_lenmode='fraction',
                        colorbar_len=0.8,
                        colorbar_x=1,
                        colorbar_xanchor='left',
                        colorbar_y=0.5,
                        name='')
    data_slider.append(data_each_yr)
 
    layout = dict(geo=dict(scope=continent,
                            projection={'type': 'natural earth'},
                            bgcolor= 'rgba(0,0,0,0)'),
                    margin=dict(l=0,
                                r=0,
                                b=0,
                                t=30,
                                pad=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)')
 
    fig_choropleth = go.Figure(data=data_slider, layout=layout)
    fig_choropleth.update_geos(showcoastlines=False, showsubunits=False,showframe=False)

    return [title, fig_choropleth]


@ app.callback(
    [
        #Output('first_graph', 'figure'),       
        Output('plt_lines', 'figure')
    ],
    [
        Input('drop_country', 'value'),
        Input('drug_type', 'value')
        #Input('choose_country', 'value')
    ]
)
def update_chart(country, drug):    

    drug_label = ''
    if drug == 0:
        drug_label = [drugs_list[0]]
    if drug == 1:
        drug_label = [drugs_list[1]]
    if drug == 2:
        drug_label = [drugs_list[2]]
    #if drug == 3:
    #    drug_label = drugs_list

    deaths_sub = deaths[(deaths["Entity"].isin(country)) & (deaths['drug'].isin(drug_label))]    

    fig2 = px.line(deaths_sub,
                  x="Year",
                  y='total',
                  color='Entity')

    fig2 = fig2.update_layout({'margin': dict(t=0, l=0, r=0, b=0),
                               'paper_bgcolor': '#F9F9F8',
                               'font_color': '#363535'})
    
    
    return [go.Figure(fig2)]




if __name__ == "__main__":
    app.run_server(debug=True)
