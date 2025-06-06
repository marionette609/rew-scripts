# rew-scripts

This is a repo with simple scripts to automate gathering measurements from Room EQ Wizard (aka REW). I will make additions here if I create more automation code similar to this in the future.

## Distortion Surface

This is a script which gathers measurements necessary to plot a distortion surface and saves them in a local JSON file. Samples of this measurement data format can be found in the sample-data folder of this repository. There are some variables you can change within the script as desired related to which units are used and the resolution of the surface (i.e. how many measurements to run).

If you are unfamiliar, a distortion surface is a visualization of audio distortion devised by Atomicbob, you can find his original thread and inspiration for this script here https://www.superbestaudiofriends.org/index.php?threads/distortion-surface-old-measurement-new-approach.13754/

You should set up REW for this script by calibrating your generator to the correct measured voltage of your signal (I also set the amp's volume to unity gain) and setting up RTA with your desired FFT settings. The script polls the RTA status on an interval and begins the next measurement when RTA has stopped, so ensure that your RTA is not set to run forever (I used 4 averages for included sample data). If you are not running REW with no GUI, you should be able to see measurements happening in real time with the RTA window open. The script is run with a simple `python distortion_surface.py`.

## Plot Distortion Surface

This takes the JSON file generated by the distortion surface script and plots the surface visualization using the plotly library. I've attempted to mimic the scale and units originally used in atomicbob's original post on this visualization method. 

You must edit the file_path variable before running this script. The script is run with a simple `python plot_distortion_surface.py`.
