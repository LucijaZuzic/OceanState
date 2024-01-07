from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
import os 
from utilities import load_object, random_colors
from scipy import stats
   
dict_xval_loc = load_object("location_data/dict_xval_loc")
dict_yval_loc = load_object("location_data/dict_yval_loc")

size_of_bin = 10
bin_ranges = [(size_of_bin * 0.5 + i * size_of_bin, size_of_bin * 1.5 + i * size_of_bin) for i in range(int(360 // size_of_bin) - 1)]

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

                                wave_bins_for_bin = dict()
                                for b in bin_ranges:
                                    wave_bins_for_bin[b] = dict()
                                wave_bins_for_bin[(360 - size_of_bin / 2, size_of_bin / 2)] = dict()

                                abs_wave_heights = [abs(w) for w in wave_heights]
                                wave_bins_starts = np.arange(min(abs_wave_heights), max(abs_wave_heights), (max(abs_wave_heights) - min(abs_wave_heights)) / 6)
                                wave_bins = [(wave_bins_starts[i], wave_bins_starts[i + 1]) for i in range(len(wave_bins_starts) - 1)]
                                
                                for b in bin_ranges:
                                    for wb in wave_bins:
                                        wave_bins_for_bin[b][wb] = 0
                                    wave_bins_for_bin[b][(wave_bins_starts[-1], max(wave_heights)) ] = 0

                                for wb in wave_bins:
                                    wave_bins_for_bin[(360 - size_of_bin / 2, size_of_bin / 2)][wb] = 0
                                wave_bins_for_bin[(360 - size_of_bin / 2, size_of_bin / 2)][(wave_bins_starts[-1], max(abs_wave_heights)) ] = 0

                                larger_than_points = np.arange(min(abs_wave_heights), max(abs_wave_heights), (max(abs_wave_heights) - min(abs_wave_heights)) / 100)
                                probability_of_larger = dict()

                                for b in bin_ranges:
                                    probability_of_larger[b] = dict()
                                    for l in larger_than_points:
                                        probability_of_larger[b][l] = 0

                                probability_of_larger[(360 - size_of_bin / 2, size_of_bin / 2)] = dict()
                                for l in larger_than_points:
                                    probability_of_larger[(360 - size_of_bin / 2, size_of_bin / 2)][l] = 0

                                for i in range(len(ugosa)):
                                    ang = 0
                                    if ugosa[i] != 0:
                                        ang = (np.arctan(vgosa[i] / ugosa[i]) / np.pi * 180 + 360) % 360
                                    elif vgosa[i] > 0:
                                        ang = 90
                                    elif vgosa[i] < 0:
                                        ang = 270
                                    angle_all.append(ang)
                                    
                                    bin_used = (360 - size_of_bin / 2, size_of_bin / 2)
                                    for b in bin_ranges:
                                        if ang >= b[0] and ang < b[1]:
                                            bin_used = b  

                                    wave_bin_used = (wave_bins_starts[-1], max(abs_wave_heights)) 
                                    for wb in wave_bins:
                                        if abs_wave_heights[i] >= wb[0] and abs_wave_heights[i] < wb[1]:
                                            wave_bin_used = wb  

                                    wave_bins_for_bin[bin_used][wave_bin_used] += 1

                                    for l in larger_than_points:
                                        if abs_wave_heights[i] >= l:
                                            probability_of_larger[bin_used][l] += 1
 

                                rcs = random_colors(len(probability_of_larger)) 
                                plt.title("Location: " + str(loc) + " long: " + str(long) + " lat: " + str((lat)))       
                                nf = 0
                                for b in probability_of_larger:
                                    if sum(list(wave_bins_for_bin[b].values())) == 0:
                                        continue
                                    xs = []
                                    ys = []
                                    for l in larger_than_points:
                                        ys.append(l)
                                        xs.append(probability_of_larger[b][l] / sum(list(wave_bins_for_bin[b].values())) * 100)
                                    plt.plot(xs, ys, label = "[" + str(b[0]).replace(".0", "") + ", " + str(b[1]).replace(".0", "") + ">", color = rcs[nf]) 
                                    nf += 1
                                    
                                plt.legend(loc = "lower center", ncol = nf / 4, bbox_to_anchor = (0.45, -0.5), title = "Wave direction (°)")
                                plt.ylabel("Wave Height (m)")
                                plt.xlabel("Probability of Exceedance (%)") 
                                 
                                if not os.path.isdir("wind_rose/" + str(loc)):
                                    os.makedirs("wind_rose/" + str(loc))

                                plt.savefig("wind_rose/" + str(loc) + "/exceedance_weibull_" + str(loc) + "_long_" + str(long) + "_lat_" + str(lat) + ".png", bbox_inches = "tight") 
                                plt.close() 
                 
            str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
            file2read.close()

            if not os.path.isfile('data2/' + str_name + ".nc"):
                os.rename('data2/' + file, 'data2/' + str_name + ".nc")