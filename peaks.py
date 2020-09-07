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

plot_peaks = px.line(merged_time_series, x='Indices', y='Amplitude' ,labels={"Indices": "Time (ms)"}, hover_name="Label" )
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


body= dbc.Container ([
        # dbc.Row
        # ([
        #     dbc.Col(html.H1("Peak Tracking of Sensor Data"), className="mb-2 text-center", style = {'paddingTop':'20px'})
        # ]),
    dbc.Row
    ([
        dbc.Col(html.H3(children='Time Series of Peaks'), className="mb-4 text-center" , style = {'paddingTop':'30px'})
    ]),

])

peaks_graph = dcc.Graph(
            id='peak-graph',
            figure=plot_peaks   
        )
    




def Peak():
    layout = html.Div([
        nav,
        body,
        peaks_graph
        
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Peak()

# if __name__ == "__main__":
#     app.run_server(debug=True)