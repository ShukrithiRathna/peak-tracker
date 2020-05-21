#importing libraries

from bokeh.models import ColumnDataSource, HoverTool, RangeSlider, CheckboxGroup, Select, CategoricalColorMapper, Range1d
from bokeh.plotting import figure
from bokeh.io import show,curdoc
from bokeh.layouts import column, row
from bokeh.models.widgets import Tabs
from bokeh.models.widgets import RadioButtonGroup

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable
import pandas as pd
import seaborn as sns

def summary_tab(scan_data, merged_time_series, peaks_df):

# plotting summary table
# function to get data for table
    def make_dataset_table(carrier_list):
        table_data=peaks_df.loc[peaks_df['Label'].isin(carrier_list)]
        table_data['Amplitude'] = table_data['Amplitude'].round(2)
        return ColumnDataSource(table_data)

# function to plot table
    def make_plot_table(src_table):
        table_columns = [TableColumn(field='Indices', title='Time(ms)'),TableColumn(field='Amplitude', title='Amplitude'),TableColumn(field='Label', title='Portion of Pipe')]
        peak_table = DataTable(source=src_table, columns=table_columns, width=500)
        return peak_table
    
# function to update table vlues
    def update_table(attr, old, new):
    	parts_to_show = [part_selection.labels[i] for i in part_selection.active]
    
    # get new data for table 
    	new_src_table = make_dataset_table(parts_to_show)
    # update data source with new values
    	src_table.data.update(new_src_table.data)

# define checkbox for table values
    labels = list(peaks_df['Label'].unique())
    part_selection = CheckboxGroup(labels=labels, active = [0, 1])
    part_selection.on_change('active', update_table)

# get initial data for table
    initial_parts = [part_selection.labels[i] for i in part_selection.active]
    src_table = make_dataset_table(initial_parts)	
# plot initial table
    peak_table=make_plot_table(src_table)

# add checkbox and table to layout
    controls_table = row(part_selection)
     

# plotting graph of Peak Amplitudes
# function to get data for plot
    def make_dataset_amp(plot_list):
        if plot_list == 0:
              plot_data=peaks_df.groupby('Label', as_index=False)['Amplitude'].mean()
        if plot_list == 1:
              plot_data=peaks_df.groupby('Label', as_index=False)['Amplitude'].max()
        if plot_list == 2:
              plot_data=peaks_df.groupby('Label', as_index=False)['Amplitude'].min()
        return ColumnDataSource(plot_data)

# function to create plot
    def make_plot_amp(src_2,plot_list):
        Label=['Bend', 'Notch','End']
        plot = figure(x_range=Label, plot_height=200, plot_width = 300, title='Peak Amplitudes')
        plot.vbar(x='Label', top='Amplitude', width=0.2, source=src_2)
        plot.xgrid.grid_line_color = None
        plot.y_range.start = 0
        return plot
    
    def update_plot_amp(attr, old, new):
    	stats_to_plot = stat_selection.active

    # get new data for  plot
    	new_src_plot = make_dataset_amp(stats_to_plot)
    # updata data source
    	src_plot.data.update(new_src_plot.data)

# define radioo button for  stats
    stat_list=['Mean', 'Max', 'Min']
    stat_selection = RadioButtonGroup(labels=stat_list, active = 0)
    stat_selection.on_change('active', update_plot_amp)

# get inital data for pot
    plot_list =  stat_selection.active
    src_plot = make_dataset_amp(plot_list)	# Columns of table
# plot initial data
    amp_plot=make_plot_amp(src_plot,plot_list)

# adding plot of amplitudes to layout
    controls_amp_plot = row(stat_selection)
    

# plotting distribution of peaks

# getting data for plot
    labels=[ 'Notch','Bend','End']
    dist_df=pd.DataFrame(columns=['Label', 'Peak_Count'])
    dist_df['Peak_Count']=peaks_df['Label'].value_counts()
    dist_df['Label']=labels
    dist_df.set_index(['Label'], inplace = True) 
    src_dist=ColumnDataSource(dist_df)

    plot_dist = figure(x_range=labels, plot_height=200, plot_width = 300, title='Peak Distribution', toolbar_location=None, tools="")
    plot_dist.vbar(x='Label', top='Peak_Count', width=0.2, source=src_dist)
    plot_dist.xgrid.grid_line_color = None
    plot_dist.y_range.start = 0

#  creating a box plot to show distribution of Amplitudes
    sns_plot=sns.boxplot( y=merged_time_series["Amplitude"], x=merged_time_series["Label"] );
    fig = sns_plot.get_figure()
    fig.savefig("PeakTracking_App/static/box_plot.png")

# Plotting the saved boxplot image
    box_plot_img = "PeakTracking_App/static/box_plot.png"
    logo_src = ColumnDataSource(dict(url = [box_plot_img]))

    box_plot = figure(plot_width = 400, plot_height = 400, title="Box Plot of Amplitude Distribution")
    box_plot.toolbar.logo = None
    box_plot.toolbar_location = None
    box_plot.x_range=Range1d(start=0, end=1)
    box_plot.y_range=Range1d(start=0, end=1)
    box_plot.xaxis.visible = None
    box_plot.yaxis.visible = None
    box_plot.xgrid.grid_line_color = None
    box_plot.ygrid.grid_line_color = None
    box_plot.image_url(url='url', x=0.05, y = 0.85, h=0.7, w=0.9, source=logo_src)
    box_plot.outline_line_alpha = 0 

# add plots to layout    
    layout = row(column(controls_table, peak_table),column( amp_plot,controls_amp_plot, plot_dist),box_plot)

# Make a tab with the layout 
    tab = Panel(child=layout, title = 'Peak Summary')
    return tab
    # plt.show()
