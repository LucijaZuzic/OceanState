from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
import os
from windrose import WindroseAxes
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
                                
                                vgosa = file2read.variables["vgosa"][:, j, k]
                                ugosa = file2read.variables["ugosa"][:, j, k]
                
                                tgosa = [np.sqrt(ugosa[i] ** 2 + vgosa[i] ** 2) for i in range(len(ugosa))]  
                            
                                angle_all = []
 
                                abs_wave_heights = [abs(w) for w in wave_heights] 
                                for i in range(len(ugosa)):
                                    ang = 0
                                    if ugosa[i] != 0:
                                        ang = (np.arctan(vgosa[i] / ugosa[i]) / np.pi * 180 + 360) % 360
                                    elif vgosa[i] > 0:
                                        ang = 90
                                    elif vgosa[i] < 0:
                                        ang = 270
                                    angle_all.append((360 + 90 - ang) % 360)
                                      
                                ax = WindroseAxes.from_ax()
                                ax.bar(angle_all, abs_wave_heights, normed = True, nsector = 36)
                                ax.set_legend() 

                                if not os.path.isdir("wind_rose/" + str(loc)):
                                    os.makedirs("wind_rose/" + str(loc))

                                plt.savefig("wind_rose/" + str(loc) + "/wind_rose_" + str(loc) + "_long_" + str(long) + "_lat_" + str(lat) + ".png", bbox_inches = "tight") 
                                plt.close()
   
            str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
            file2read.close()

            if not os.path.isfile('data2/' + str_name + ".nc"):
                os.rename('data2/' + file, 'data2/' + str_name + ".nc")