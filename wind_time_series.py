from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import os 
from utilities import random_colors, load_object
   
dict_xval_loc = load_object("location_data/dict_xval_loc")
dict_yval_loc = load_object("location_data/dict_yval_loc")

g_const = 9.80665 
p_const = 1.02

start_date = datetime(year = 1993, month = 1, day = 1)

for loc in dict_xval_loc:

    for file in os.listdir("data2"):

        file_split = [int(v) for v in file.replace(".nc", "").split("_")]

        if dict_xval_loc[loc][0] >= file_split[0] and dict_xval_loc[loc][0] <= file_split[1] and dict_yval_loc[loc][0] >= file_split[2] and dict_yval_loc[loc][0] <= file_split[3]:
             
            file2read = netcdf.NetCDFFile('data2/' + file,'r')
 
            if dict_xval_loc[loc][0] >= file2read.variables["longitude"][0] and dict_xval_loc[loc][0] <= file2read.variables["longitude"][-1] and dict_yval_loc[loc][0] >= file2read.variables["latitude"][0] and dict_yval_loc[loc][0] <= file2read.variables["latitude"][-1]:
                
                for j, lat in enumerate(file2read.variables["latitude"]):
                    for k, long in enumerate(file2read.variables["longitude"]):
                        if long >= dict_xval_loc[loc][0] and long <= dict_xval_loc[loc][-1] and lat >= dict_yval_loc[loc][0] and lat <= dict_yval_loc[loc][-1]:
                            
                            wave_heights = file2read.variables["sla"][:, j, k]
  
                            if min(wave_heights) != max(wave_heights) and not np.isnan(min(wave_heights)):
                                 
                                abs_wave_heights = [abs(w) for w in wave_heights]
                                  
                                time_deltas = file2read.variables["time"][0:] - file2read.variables["time"][0]
                                datetimes = [datetime.strftime(start_date + timedelta(days = int(time_delta)), "%d.%m.%Y.") for time_delta in time_deltas]
                                plt.title("Location: " + str(loc) + " long: " + str(long) + " lat: " + str((lat)))
                                plt.plot(time_deltas, wave_heights)
                                steps = list(range(0, len(wave_heights), 7 * 365))
                                steps.append(len(wave_heights))
                                
                                for i in range(len(steps) - 1):
                                    wave_heights_sorted = sorted(abs_wave_heights[steps[i]:steps[i + 1]])
                                    upper_third = wave_heights_sorted[- len(wave_heights_sorted) // 3:] 
                                    mean_upper_third = np.mean(upper_third)
                                    if i == 0:
                                        plt.plot(time_deltas[steps[i]:steps[i + 1]], [mean_upper_third for t in time_deltas[steps[i]:steps[i + 1]]], color = "r", label = "$H_{1/3}$")
                                    else:
                                        plt.plot(time_deltas[steps[i]:steps[i + 1]], [mean_upper_third for t in time_deltas[steps[i]:steps[i + 1]]], color = "r")
                                    plt.plot(time_deltas[steps[i]:steps[i + 1]], [- mean_upper_third for t in time_deltas[steps[i]:steps[i + 1]]], color = "r")
                                 
                                    wave_heights_part = abs_wave_heights[steps[i]:steps[i + 1]] 
                                    energy_part = 0
                                    for val in wave_heights_part:
                                        energy_part += val ** 2
                                    power_part = energy_part / len(wave_heights_part)
                                    hrms = 4 * np.sqrt(power_part / (g_const * p_const))  
 
                                    if i == 0:
                                        plt.plot(time_deltas[steps[i]:steps[i + 1]], [hrms for t in time_deltas[steps[i]:steps[i + 1]]], color = "g", label = "$H_{rms}$")
                                    else:
                                        plt.plot(time_deltas[steps[i]:steps[i + 1]], [hrms for t in time_deltas[steps[i]:steps[i + 1]]], color = "g")
                                    plt.plot(time_deltas[steps[i]:steps[i + 1]], [- hrms for t in time_deltas[steps[i]:steps[i + 1]]], color = "g")
                                 
                                indexes_plot = range(0, len(datetimes), 7 * 365)
                                datetimes_plot = [datetimes[ix] for ix in indexes_plot]
                                plt.xticks(ticks = indexes_plot, labels = datetimes_plot)
                                plt.xlabel("Date")
                                plt.ylabel("Elevation (m)")
                                plt.legend()

                                if not os.path.isdir("wind_rose/" + str(loc)):
                                    os.makedirs("wind_rose/" + str(loc))

                                plt.savefig("wind_rose/" + str(loc) + "/time_series_" + str(loc) + "_long_" + str(long) + "_lat_" + str(lat) + ".png", bbox_inches = "tight") 
                                plt.close() 
                 
            str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
            file2read.close()

            if not os.path.isfile('data2/' + str_name + ".nc"):
                os.rename('data2/' + file, 'data2/' + str_name + ".nc")