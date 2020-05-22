from bokeh.models import ColumnDataSource, HoverTool, Panel, RangeSlider
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models.widgets import Tabs

import pandas as  pd

def rolling_mean_tab(scan_data, merged_time_series, peaks_df):

# function to get data for slider    
    def make_dataset_slider(beg, end):
        column_list=list(scan_data.columns)
        column_list.pop()
        cols=column_list[beg:end+1]
        slider_data=pd.DataFrame(columns=['Indices','Rolling_Average', 'Label'])
        slider_data['Indices']=merged_time_series['Indices']
        slider_data['Label']=merged_time_series['Label']
        slider_data['Rolling_Average']=scan_data[cols].mean(axis=1)
        return ColumnDataSource(slider_data)

# function to  plot the data for the slider
    def make_plot_slider(src_slider):
	    # table_columns = [TableColumn(field='Indices', title='Time(micro seconds'),
        plot = figure(plot_width = 1000, plot_height = 700, title = 'Peak Tracking in Ascan Data',x_axis_label = 'Time (ms))',y_axis_label = 'Amplitude')
        plot.line(x='Indices', y='Rolling_Average',color='blue', source=src_slider)
        h = HoverTool(tooltips = [('Amplitude', '@Rolling_Average'),('Part','@Label')])
        plot.add_tools(h)
        return plot
	
# function to update the slider
    def update_slider(attr, old, new):
        beg=range_select.value[0] 
        end=range_select.value[1]

    # get data for slider with new values
        new_src_slider = make_dataset_slider(beg,end)
    # update the data source
        src_slider.data.update(new_src_slider.data)

# define Range Slider
    range_select = RangeSlider(start = 2, end = 119, value = (2, 10), step = 5, title = 'Datafiles for Rolling Mean (Scan #)')
    range_select.on_change('value', update_slider)

# get inital data for slider
    src_slider = make_dataset_slider(beg = range_select.value[0], end = range_select.value[1])	
# plot initial data for slider
    plot_slider=make_plot_slider(src_slider)

# add slider and plot to layout    
    controls = row(range_select)
    layout = column(controls, plot_slider)
    
# Make a tab with the layout 
    tab_slider = Panel(child=layout, title = 'Rolling Mean')
    return tab_slider


