#importing libraries

import pandas as pd
import numpy as np
import os

#detect peaks
from scipy.signal import find_peaks, peak_prominences

#function to label each peak as end, notch or bend
def fill_labels(labels,ind,value):
    labels[ind]=value   
    return labels

# Read data into dataframes
scan_data = pd.DataFrame()
for file in os.listdir('Data/')[1:-1]:
    filepath='Data/'+str(file)
    temp = open(filepath,'+r')
    temp = temp.read().splitlines()
    temp = [int(item) for item in temp]
    scan_data[file.split('.')[0]] = temp

#get average of all trials  of measurement (Amplitudes)
scan_data['avg'] = scan_data.mean(axis=1)

# convert measured values (Amplitudes) to dataframe
time_series=pd.DataFrame(columns=['Indices','Amplitude'])
time_series['Amplitude']=scan_data['avg']
time_series['Indices']=list(range(len(scan_data['avg'])))

# obtain peak values
peak_indices = find_peaks(time_series['Amplitude'],height=[5,200], distance=300)[0] #get indices of peaks
prominence=peak_prominences(time_series['Amplitude'], peak_indices, wlen=None)[0] # get prominences of peaks

#combine peaks with measured values into dataframe
peaks_df = pd.DataFrame(columns=['Indices', 'Amplitude','Prominence', 'Label'])
peaks_df['Indices']=peak_indices
peaks_df['Amplitude'] = peaks_df.apply(lambda row: time_series['Amplitude'][row.Indices], axis = 1) 
peaks_df['Prominence']=prominence

#get labels for each value based on domain knowledge
labels = ['']*len(time_series['Amplitude'])
q1 = np.quantile(time_series['Amplitude'][peak_indices],0.25)
q3 = np.quantile(time_series['Amplitude'][peak_indices],0.75)
for item in peak_indices:
    if time_series['Amplitude'][item] <= q1 :
        labels = fill_labels(labels,item,'Bend')
    elif ((time_series['Amplitude'][peak_indices][item] >= q1) & (time_series['Amplitude'][item] <= q3)):
        labels = fill_labels(labels,item,'Notch')
    else:
        labels = fill_labels(labels,item,'End')

# add label to peaks dataframe
peaks_df['Label'] = peaks_df.apply(lambda row: labels[row.Indices], axis = 1) 

# merge peaks values, labels, and ampltidues into one general purpose dataframe for plotting
merged_time_series=pd.merge(time_series, peaks_df, on='Indices', how='outer')
merged_time_series.drop(['Amplitude_y'], axis=1, inplace=True)
merged_time_series.rename(columns={'Amplitude_x': 'Amplitude'}, inplace=True)

# Label unknown parts (Amplitudes surrounding peaks get same label as the peaks)
merged_time_series['Label'].fillna( method ='ffill', limit =250, inplace=True)
merged_time_series['Label'].fillna( method ='bfill', limit = 250, inplace=True)
merged_time_series['Label'].fillna( "Pipe", inplace=True)

peaks_df.to_csv('peak_data.csv')

import plotly.express as px
import plotly.graph_objects as go
# import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.title = 'Peak Tracking'

df = merged_time_series
fig = px.line(df, x='Indices', y='Amplitude', title='Peaks', labels={
                     "Indices": "Time (ms)"
                 }, hover_name="Label" )
fig.update_layout(
    hoverlabel=dict(
        bgcolor="white", 
        font_size=16, 
        font_family="Rockwell"
    )
)
# fig.add_trace(go.Scatter( peaks_df,  x='Indices', y='Amplitude', color = 'Label', mode='markers', labels={"Label": "Portion of pipe"}))                 


bend_mask = peaks_df['Label'] == 'Bend'
x_bend=peaks_df[bend_mask]['Indices']
y_bend=peaks_df[bend_mask]['Amplitude']
fig.add_trace(go.Scatter(x=x_bend, y=y_bend,mode='markers', name='Bend Peaks'))

notch_mask = peaks_df['Label'] == 'Notch'
x_notch=peaks_df[notch_mask]['Indices']
y_notch=peaks_df[notch_mask]['Amplitude']
fig.add_trace(go.Scatter(x=x_notch, y=y_notch,mode='markers', name='Notch Peaks'))

end_mask = peaks_df['Label'] == 'End'
x_end=peaks_df[end_mask]['Indices']
y_end=peaks_df[end_mask]['Amplitude']
fig.add_trace(go.Scatter(x=x_end, y=y_end,mode='markers', name='End Peaks'))

fig2 = px.scatter(peaks_df, x="Prominence", y="Amplitude", color="Label",
                 labels={
                     "Label": "Portion of pipe"
                 },
                title="Prominence of peaks")
# plot_data=peaks_df.groupby('Label', as_index=False)['Amplitude'].mean()
# print(plot_data)


# print(peaks_df.groupby('Label', as_index=False)['Amplitude'].mean()['Amplitude'])
fig5=px.histogram(peaks_df, x='Label', )

label=peaks_df['Label'].unique()

fig3 = go.Figure(data=[
    go.Bar(name='Min', x=label, y=peaks_df.groupby('Label', as_index=False)['Amplitude'].min()['Amplitude']),
    go.Bar(name='Max', x=label, y=peaks_df.groupby('Label', as_index=False)['Amplitude'].max()['Amplitude']),
    go.Bar(name='Mean', x=label, y=peaks_df.groupby('Label', as_index=False)['Amplitude'].mean()['Amplitude']),
 ])
# Change the bar mode
fig3.update_layout(barmode='group')  

peaks_df['Label'].value_counts()

fig4 =px.box( y=merged_time_series["Amplitude"], x=merged_time_series["Label"], title="Distribution of Amplitudes" )

app.layout = html.Div(children=[
    dbc.Container
    ([
        dbc.Row
        ([
            dbc.Col(html.H1("Peak Tracking of Sensor Data"), className="mb-2 text-center", style = {'paddingTop':'20px'})
        ]),
        dbc.Row
        ([
            dbc.Col(html.H6(children='Visualising sensor data from pipes'), className="mb-4 text-center")
        ]),

    ]),

    dcc.Graph(
        id='peak-graph',
        figure=fig
    ),
    
    dbc.Row
    ([
        dbc.Col
        ([
            dcc.Graph
            (
                id='prominence-graph',
                figure=fig2
            ), 
            
        ]),
        dbc.Col
        ([
            dcc.Graph
            (
            id='box-graph',
            figure=fig4
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
            figure=fig5
        )
        ]),
        dbc.Col([
        dcc.Graph(
            id='mean-graph',
            figure=fig3
        )

        ])


    ])

    

])    

if __name__ == '__main__':
    app.run_server(debug=True)