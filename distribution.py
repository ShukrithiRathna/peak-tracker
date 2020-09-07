#importing libraries
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

# Navbar
from navbar import Navbar

# Data
from get_data import get_time_series, get_peaks, get_merged_df

# get data
time_series=get_time_series()
peaks_df=get_peaks(time_series)
merged_time_series=get_merged_df(time_series,peaks_df)




prominence = px.scatter(peaks_df, x="Prominence", y="Amplitude", color="Label", labels={"Label": "Portion of pipe" },title="Prominence of peaks")


hist_graph=px.histogram(peaks_df, x='Label', )


label=peaks_df['Label'].unique()

distro_graph = go.Figure(data=[
    go.Bar(name='Min', x=label, y=peaks_df.groupby('Label', as_index=False)['Amplitude'].min()['Amplitude']),
    go.Bar(name='Max', x=label, y=peaks_df.groupby('Label', as_index=False)['Amplitude'].max()['Amplitude']),
    go.Bar(name='Mean', x=label, y=peaks_df.groupby('Label', as_index=False)['Amplitude'].mean()['Amplitude']),
 ])
# Change the bar mode
distro_graph.update_layout(barmode='group')  

box_plot =px.box( merged_time_series, y="Amplitude", x="Label",  title="Distribution of Amplitudes" )




nav = Navbar()
body=dbc.Container([
    dbc.Row
    ([
        dbc.Col(html.H3(children='Visualizing Sensor Data'), className="mb-4 text-center"),
    ],
        style={'padding-top':'30px'}
    ),

   
    
    dbc.Row
    ([
        dbc.Col
        ([
            dcc.Graph
            (
                id='prominence-graph',
                figure=prominence
            ), 
            
        ]),
        dbc.Col
        ([
            dcc.Graph
            (
            id='box-graph',
            figure=box_plot
            )
        ])
    ]),
    dbc.Row
        ([
            dbc.Col(html.H4(children='Distribution of Peaks'), className="mb-4 text-center")
        ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
            id='hist-graph',
            figure=hist_graph
        )
        ]),
        dbc.Col([
        dcc.Graph(
            id='mean-graph',
            figure=distro_graph
        )

        ])
    ])
  
])    


def App():
    layout = html.Div([
        nav,
        body
    ])
    return layout


if __name__ == '__main__':
    app.run_server(debug=True)