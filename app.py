import dash
from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url


deaths = pd.read_csv('deaths-drug-overdoses.csv')

fig = px.bar(deaths, x = 'Year', y='Deaths - Opioid use disorders - Sex: Both - Age: All Ages (Number)', color='Entity')  
df = px.data.gapminder()
years = deaths.Year.unique()
countries = deaths.Entity.unique()

# stylesheet with the .dbc class
#dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/dbc.min.css"])


header = html.H4(
    "Drugs Report in Europe", className="bg-primary text-white p-2 mb-2 text-leftcenter"
)

table = html.Div(
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True} for i in deaths.columns],
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


dropdown = html.Div(
    [
        dbc.Label("Select indicator (y-axis)"),
        dcc.Dropdown(
            ["gdpPercap", "lifeExp", "pop"],
            "pop",
            id="indicator",
            clearable=False,
        ),
    ],
    className="mb-4",
)

checklist = html.Div(
    [
        dbc.Label("Select Continents"),
        dbc.Checklist(
            id="continents",
            options=["Check", "List", "example"],
            value=countries,
            inline=True,
        ),
    ],
    className="mb-4",
)

slider = html.Div(
    [
        dbc.Label("Select Years"),
        dcc.RangeSlider(
            years[0],
            years[-1],
            5,
            id="years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[2], years[-2]],
            className="p-0",
        ),
    ],
    className="mb-4",
)
theme_colors = [
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "light",
    "dark",
    "link",
]
colors = html.Div(
    [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
)
colors = html.Div(["Theme Colors:", colors], className="mt-2")


slider_years = html.Div(
    [
        dbc.Label("Select Birth Year"),
        dcc.RangeSlider(
            min(deaths.Year.unique()),
            max(deaths.Year.unique()),
            5,
            id="birth_years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[min(deaths.Year.unique()), max(deaths.Year.unique())],
            className="p-0",
        ),
    ],
    className="mb-4",
)

dropdown_prem = html.Div([
    dbc.Label("Select Premim Type"),
    dcc.Dropdown(options=['something here', 'ideia'],
                        value='ALL',
                        clearable=False)])

dropdown_educ = html.Div([
    dbc.Label("Select Education Degree"),
    dcc.Dropdown(options= ['something here', 'ideia'],
                        value='All degrees',
                        clearable=False,
                        id='educs')])


checklist_childs = html.Div(
    [
        dbc.Label("With Childrens"),
        dbc.Checklist(
            id="childrens",
            options=['something here', 'ideia'],
            value="test",
            inline=True,
        ),
    ],
    className="mb-4",
)


controls = dbc.Card(
    [dropdown, checklist, slider, dropdown_prem, slider_years, dropdown_educ, checklist_childs],
    body=True,
)


##############################################
################### LAYOUT ###################
##############################################


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([    
    html.Div([
     html.H1(children='DRUG REPORT', style={'width': '100%', 'align':'center', 'opacity':'80%'}),
        controls
        ], className='side_bar'),
   
    html.Div([
        html.Div([
               
            html.Div([
                html.Div([

                    html.Div([   
                        html.Label(id='title_bar'),           
                        dcc.Graph(id='bar_fig'), 
                        html.Div([              
                            html.P(id='comment')
                        ], className='box_comment'),
                    ], className='box', style={'padding-bottom':'15px'}),
                ], style={'width': '40%'}),


                html.Div([
               
                    html.Div([
                        html.Div([
                            html.Label('Drug Types', style={'font-size': 'medium'}),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                html.Div([
                                    html.H4('Land use', style={'font-weight':'normal'}),
                                    html.H3(id='land_use')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('Animal Feed', style={'font-weight':'normal'}),
                                    html.H3(id='animal_feed')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('Farm'),
                                    html.H3(id='farm')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('Processing'),
                                    html.H3(id='processing')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('Transport'),
                                    html.H3(id='transport')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('Packaging', style={'font-weight':'normal'}),
                                    html.H3(id='packging')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('Retail', style={'font-weight':'normal'}),
                                    html.H3(id='retail')
                                ],className='box_emissions'),
                            ], style={'display': 'flex'}),

                        ], className='box', style={'heigth':'10%'}),

                        html.Div([ 
                            html.Div([
                                
                                html.Div([
                                    html.Br(),
                                    html.Label("2. GRAPGH some details", id='title_map', style={'font-size':'medium'}), 
                                    html.Br(),
                                    html.Label('These quantities refer to the raw material used to produce the product selected above', style={'font-size':'9px'}),
                                ], style={'width': '70%'}),
                                html.Div([

                                ], style={'width': '5%'}),
                                html.Div([
                                   # fig, 
                                    html.Br(),
                                    html.Br(), 
                                ], style={'width': '25%'}),
                            ], className='row'),
                            
                            dcc.Graph(id='map', style={'position':'relative', 'top':'-50px'}), 

                            html.Div([
                                #fig
                            ], style={'margin-left': '15%', 'position':'relative', 'top':'-38px'}),
                            
                        ], className='box', style={'padding-bottom': '0px'}), 
                    ]),
                ], style={'width': '60%'}),           
            ], className='row'),

            html.Div([
                html.Div([
                    html.Label("3. Global greenhouse gas emissions from food production, in percentage", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Click on it to know more!', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(figure=fig)
                ], className='box', style={'width': '53%'}), 
                html.Div([
                    html.Label("4. Freshwater withdrawals per kg of product, in Liters", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Click on it to know more!', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(figure=fig)
                ], className='box', style={'width': '50%'}), 
            ], className='row'),

            html.Div([
                html.Div([
                    html.Label("3. Global greenhouse gas emissions from food production, in percentage", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Click on it to know more!', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(figure=fig)
                ], className='box', style={'width': '53%'}), 
                html.Div([
                    html.Label("4. Freshwater withdrawals per kg of product, in Liters", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Click on it to know more!', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(figure=fig)
                ], className='box', style={'width': '50%'}), 
            ], className='row'),

            html.Div([
                html.Div([
                    html.P(['Group name', html.Br(),'Names'], style={'font-size':'12px'}),
                ], style={'width':'60%'}), 
                html.Div([
                    html.P(['Sources ', html.Br(), html.A('Our World in Data', href='https://ourworldindata.org/', target='_blank'), ', ', html.A('Food and Agriculture Organization of the United Nations', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
        ], className='main'),
    ]),
])


@app.callback(       
    Output("line-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("table", "data"),       
    Input("indicator", "value"),
    Input("continents", "value"),
    Input("years", "value"),    
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
def update_line_chart(indicator, continent, yrs, theme, educ):
    if continent == [] or indicator is None:
        return {}, {}, []

    dff = df[df.year.between(yrs[0], yrs[1])]
    dff = dff[dff.continent.isin(continent)]
    data = dff.to_dict("records")

    fig = px.line(
        dff,
        x="year",
        y=indicator,
        color="continent",
        line_group="country",
        template=template_from_url(theme),
    )

    fig_scatter = px.scatter(
        df.query(f"year=={yrs[1]} & continent=={continent}"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
        template=template_from_url(theme),
        title="Gapminder %s: %s theme" % (yrs[1], template_from_url(theme)),
    )

    return fig, fig_scatter, data


if __name__ == "__main__":

    app.run_server(debug=True)