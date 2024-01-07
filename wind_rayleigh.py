from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime 
import os
from windrose import WindAxes
from utilities import load_object
   
dict_xval_loc = load_object("location_data/dict_xval_loc")
dict_yval_loc = load_object("location_data/dict_yval_loc")

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
                                 
                                abs_wave_heights = [abs(w) * 100 for w in wave_heights] 

                                ax2 = WindAxes.from_ax() 
                                bins = np.arange(0, max(abs_wave_heights) + 1, 1)
                                bins = bins[1:]
                                ax2, params = ax2.pdf(abs_wave_heights, bins = bins) 
                                
                                if not os.path.isdir("wind_rose/" + str(loc)):
                                    os.makedirs("wind_rose/" + str(loc))

                                plt.savefig("wind_rose/" + str(loc) + "/rayleigh_" + str(loc) + "_long_" + str(long) + "_lat_" + str(lat) + ".png", bbox_inches = "tight") 
                                plt.close()

                                print(params) 
                                 
            str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
            file2read.close()

            if not os.path.isfile('data2/' + str_name + ".nc"):
                os.rename('data2/' + file, 'data2/' + str_name + ".nc")