from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
import os 
from utilities import plot_arc, random_colors, load_object, make_circles
   
dict_xval_loc = load_object("location_data/dict_xval_loc")
dict_yval_loc = load_object("location_data/dict_yval_loc")
 
size_of_bin = 10
bin_ranges = [(size_of_bin * 0.5 + i * size_of_bin, size_of_bin * 1.5 + i * size_of_bin) for i in range(int(360 // size_of_bin) - 1)]
  
for loc in dict_xval_loc:
                                
    #plt.axis("off")

    found = False

    ax = plt.gca()
    ax.set_aspect('equal', adjustable = 'box')
  
    plt.title("Location: " + str(loc)) 
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
 
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
                                             
                                sum_in_b = dict()
                                sum_in_wb = dict()
 
                                for b in wave_bins_for_bin:
                                    for wb in wave_bins_for_bin[b]:
                                        percent = wave_bins_for_bin[b][wb] / len(wave_heights) * 100

                                        if b not in sum_in_b:
                                            sum_in_b[b] = 0

                                        if wb not in sum_in_wb:
                                            sum_in_wb[wb] = 0

                                        sum_in_b[b] += percent
                                        sum_in_wb[wb] += percent
                                
                                step_size_use = max(list(sum_in_b.values())) / 5

                                min_r = step_size_use

                                rsss = np.arange(min_r, min_r + max(list(sum_in_b.values())) + step_size_use, step_size_use)
                                rsss_tags = [str(np.round(rsss_val - min_r, 2)) for rsss_val in rsss]
                                rsss_tags[0] = "0"
 
                                rsss_minus = [- rsss_val for rsss_val in rsss]
                                rsss_minus.reverse()

                                rsss_tags_minus = [rsss_tags_val for rsss_tags_val in rsss_tags]
                                rsss_tags_minus.reverse()

                                rsss_all = [rsss_val for rsss_val in rsss_minus]
                                for rsss_val in rsss:
                                    rsss_all.append(rsss_val)
                                rsss_tags_all = rsss_tags_minus + rsss_tags

                                xoff = long
                                yoff = lat  
                                scf = 1 / 11 / max(list(sum_in_b.values()))

                                found = True

                                make_circles(np.arange(min_r, min_r + max(list(sum_in_b.values())) + step_size_use, step_size_use), np.arange(size_of_bin / 2, 360, size_of_bin), scf, xoff, yoff, 0)
                                
                                rcs = random_colors(len(wave_bins) + 1)  
 
                                for b in dict(sorted(wave_bins_for_bin.items(), key=lambda item: item[0], reverse = True)):
                                    sum_r = min_r
                                    for ci, wb in enumerate(dict(sorted(wave_bins_for_bin[b].items(), key=lambda item: item[0]))): 
                                        sum_r_new = sum_r + wave_bins_for_bin[b][wb] / len(wave_heights) * 100 
                                        if sum_r_new != sum_r:
                                            lnam = "[" + str(np.round(wb[0], 2)) + ", " + str(np.round(wb[1], 2)) + ">"
                                            plot_arc(lnam, sum_r_new, sum_r, b[0], b[1], color_use = rcs[ci], draw_edges = True, scaling_factor = scf, xoffset = xoff, yoffset = yoff, use_label = False)
                                        sum_r = sum_r_new

            file2read.close()

    if not found:
        continue
           
    if not os.path.isdir("wind_rose/" + str(loc)):
        os.makedirs("wind_rose/" + str(loc))

    plt.savefig("wind_rose/" + str(loc) + "/wind_rose_" + str(loc) + "_all_no_map.png", bbox_inches = "tight") 
    plt.close()