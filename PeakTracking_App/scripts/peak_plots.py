# importing libraries
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models.widgets import Tabs

def peak_plot_tab(scan_data, merged_time_series, peaks_df):

# from bokeh.palettes import d3
    plot = figure(plot_width = 1000, plot_height = 650, title = 'Peak Tracking in a-scan Data',x_axis_label = 'Time (Micro seconds))',y_axis_label = 'Amplitude')

# Data Source for plot
    source = (ColumnDataSource(merged_time_series))
    plot.line(x='Indices', y='Amplitude',color='blue', source=source)


# plot bend peaks
    bend_mask = peaks_df['Label'] == 'Bend'
    x_bend=peaks_df[bend_mask]['Indices']
    y_bend=peaks_df[bend_mask]['Amplitude']
    plot.circle(x=x_bend, y=y_bend, size=7,fill_alpha=0.8, color='red', legend='Bend')

# plot notch peaks
    notch_mask = peaks_df['Label'] == 'Notch'
    x_notch=peaks_df[notch_mask]['Indices']
    y_notch=peaks_df[notch_mask]['Amplitude']
    plot.circle(x=x_notch, y=y_notch, size=7,fill_alpha=0.8, color='green', legend='Notch')

# plot end peaks
    end_mask = peaks_df['Label'] == 'End'
    x_end=peaks_df[end_mask]['Indices']
    y_end=peaks_df[end_mask]['Amplitude']
    plot.circle(x=x_end, y=y_end, size=7,fill_alpha=0.8, color='black', legend='End')

# hide legend values on clicking
    plot.legend.click_policy='hide'

# create a hover tool for plot
    h = HoverTool(tooltips = [('Amplitude', '@Amplitude'),('Part','@Label')])
    plot.add_tools(h)

# Make a tab with the plot
    tab = Panel(child = plot, title = 'Peak_plot')

    return(tab)