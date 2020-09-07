import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

from navbar import Navbar
nav = Navbar()


# Data
from get_data import get_time_series, get_peaks, get_merged_df

# get data
time_series=get_time_series()
peaks_df=get_peaks(time_series)
merged_time_series=get_merged_df(time_series,peaks_df)

plot_peaks = px.line(merged_time_series, x='Indices', y='Amplitude', labels={"Indices": "Time (ms)"}, hover_name="Label" )
plot_peaks.update_layout(
    hoverlabel=dict(
        bgcolor="white", 
        font_size=16, 
        font_family="Rockwell"
    )
)



bend_mask = peaks_df['Label'] == 'Bend'
x_bend=peaks_df[bend_mask]['Indices']
y_bend=peaks_df[bend_mask]['Amplitude']
plot_peaks.add_trace(go.Scatter(x=x_bend, y=y_bend,mode='markers', name='Bend Peaks'))

notch_mask = peaks_df['Label'] == 'Notch'
x_notch=peaks_df[notch_mask]['Indices']
y_notch=peaks_df[notch_mask]['Amplitude']
plot_peaks.add_trace(go.Scatter(x=x_notch, y=y_notch,mode='markers', name='Notch Peaks'))

end_mask = peaks_df['Label'] == 'End'
x_end=peaks_df[end_mask]['Indices']
y_end=peaks_df[end_mask]['Amplitude']
plot_peaks.add_trace(go.Scatter(x=x_end, y=y_end,mode='markers', name='End Peaks'))



card =     [
    dbc.CardBody(
        [   
            # dbc.CardHeader("Peak Tracking in Pipes", className= "text-center"),
            #   dbc.CardImg(s   rc="/static/images/peak.png", top=True),
             html.H5("Peak Tracking in Pipes", className="card-title"),
            html.P("This is a mini-application that displays various stats related to peak tracking of sensor data using Python. The graph on the right displays the ascan sensor data from a pipe. Browse the other tabs on the menu to view other stats." ),
            dbc.Button("View Peaks", color="primary",href="/peaks"),
        ],
        
    style={"width": "22rem", "height":"300px", "justify":"around"}, 
    ), 
    # style={"padding-top":"50px","padding-left":"140px"},
    ]
row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(card)),
        # dbc.Col(html.img(src="/static/images/peak.png"))
   
    ],
    className="mb-4",  style={"padding-top":"50px","padding-left":"500px","padding-right":"500px"},
)

body = dbc.Container(
    [
        # dbc.Row(html.H2("Peak Tracking Application"), className='center-text'),
        dbc.Row([
            dbc.Col([
                html.H5("Peak Tracking in Pipes"),
                html.P("This is a mini-application that displays various stats related to peak tracking of sensor data using Python. The graph on the right displays the ascan sensor data from a pipe. Browse the other tabs on the menu to view other stats." ),
                # dbc.Button("View Peaks", color="secondary",href="/peak"),
            ],
            style= {"padding-top":"130px"},
            md=4,
            ),
            dbc.Col([
                dcc.Graph(
                    id='peak-graph',
                    figure=plot_peaks   
                ),
            ]),
        ])
    ],
    className="mt-4",
)

def Homepage():
    layout = html.Div([
        nav,
        row_1
        
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()

# if __name__ == "__main__":
#     app.run_server(debug=True)