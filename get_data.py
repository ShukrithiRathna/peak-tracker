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

def get_time_series():
    # convert measured values (Amplitudes) to dataframe
    time_series=pd.DataFrame(columns=['Indices','Amplitude'])
    time_series['Amplitude']=scan_data['avg']
    time_series['Indices']=list(range(len(scan_data['avg'])))
    return time_series


def get_peaks(time_series):
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

    return peaks_df


def get_merged_df(time_series,peaks_df):

    # merge peaks values, labels, and ampltidues into one general purpose dataframe for plotting
    merged_time_series=pd.merge(time_series, peaks_df, on='Indices', how='outer')
    merged_time_series.drop(['Amplitude_y'], axis=1, inplace=True)
    merged_time_series.rename(columns={'Amplitude_x': 'Amplitude'}, inplace=True)

    # Label unknown parts (Amplitudes surrounding peaks get same label as the peaks)
    merged_time_series['Label'].fillna( method ='ffill', limit =250, inplace=True)
    merged_time_series['Label'].fillna( method ='bfill', limit = 250, inplace=True)
    merged_time_series['Label'].fillna( "Pipe", inplace=True)

    return merged_time_series
    # peaks_df.to_csv('peak_data.csv')