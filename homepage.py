import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

from navbar import Navbar
nav = Navbar()


card = [
    dbc.CardBody(
        [   
            html.H5("Peak Tracking in Pipes", className="card-title"),
            html.P("This is a mini-application that displays various stats related to peak tracking of sensor data using Python. The graphs display the stats of ascan sensor data of pipes." ),
            dbc.Button("View Peaks", color="primary",href="/peaks"),
        ],
        
    style={"width": "22rem", "height":"300px", "justify":"around"}, 
    ), 
]

row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(card)),
        # dbc.Col(html.img(src="/static/images/peak.png"))
   
    ],
    className="mb-4",  style={"padding-top":"50px","padding-left":"500px","padding-right":"500px"},
)

def Homepage():
    layout = html.Div([
        nav,
        row_1
        
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()

