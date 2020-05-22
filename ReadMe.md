## Peak Tracking Application

* This is a small application (dashboard) created in bokeh to display various stats related to peak tracking of sensor data
* The application runs on a bokeh server. 
  
### Usage

* The application uses the following python packages. Kindly ensure that all necessary packages are installed before running the server.
  * bokeh
  * numpy
  * pandas
  * seaborn
 *  Requirements can be installed by running 'pip install -r requirements.txt' in your virtual environment. 
* To run the application, use the following command from the folder in which this repository has been  placed
  * bokeh serve --show peak-tracker
* The application will open in your system's default browser.
  
### Features

* The dashboard contains three tabs:
  1. Peak Plot:
       * Contains Line plot of average of all trials of sensor along with Scatter Plot of Peaks detected
       * Hovering over the plot returns the Amplitude and the Part of the pipe (bend, end, notch, pipe) at that point.
       * The legend denoting the colour codes of the peaks corresponding to the part of the pipe can be clicked on to toggle visibilty of the corresponding peaks.
  2. Rolling Mean:
      * A slider widget lets the user interact with the plot.
      * Line plot of rolling mean of all trials of data is plotted based on user input. 
      * Sliding the two toggles on the slider sets the window for the rolling mean.
      * Hovering over the plot returns the Amplitude and the part of the pipe (bend, end, notch, pipe) at that point.
  3. Peak Summary:
     1. Table:
        * The table along with the checkbox widget displays a summary of the peaks - Amplitude, Indices and part of the pipe.
        * The checkbox allows the user to choose which for portions of the pipe the data is displayed.

     2. Peak Amplitudes:

          * This plot shows the mean, max and min peak amplitudes of each part of the pipe.
          * The radio button allows the user to toggle between mean, min and max values.
     3. Peak Distribution:

        * This plot shows the distribution of peaks between the different parts of the pipe.
     4. Boxplot of Amplitudes:

        *  This plot shows the distribution of amplitude values in different parts of the pipe.
