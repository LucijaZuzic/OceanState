from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import os
from windrose import WindroseAxes, WindAxes

def random_colors(num_colors):
    colors_set = []
    for x in range(num_colors):
        string_color = "#"
        while string_color == "#" or string_color in colors_set:
            string_color = "#"
            set_letters = "0123456789ABCDEF"
            for y in range(6):
                string_color += set_letters[np.random.randint(0, 16)]
        colors_set.append(string_color)
    return colors_set

def plot_arc(radius, start_radius, start, end, color_use = "blue", next_color = "white"):
    if radius == 0:
        return
    if start > end:
        start = start - 360
    
    x_coords_arc = [radius * np.cos(angle / 180 * np.pi) for angle in range(start, end + 1)]
    y_coords_arc = [radius * np.sin(angle / 180 * np.pi) for angle in range(start, end + 1)]
    plt.plot(x_coords_arc, y_coords_arc, c = "k")
    x_coords_arcb = [start_radius * np.cos(angle / 180 * np.pi) for angle in range(start, end + 1)]
    y_coords_arcb = [start_radius * np.sin(angle / 180 * np.pi) for angle in range(start, end + 1)]
    plt.plot(x_coords_arcb, y_coords_arcb, c = "k")
    x_coords_s = [ra * np.cos(start / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.0001, 0.0001)]
    y_coords_s = [ra * np.sin(start / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.0001, 0.0001)]
    plt.plot(x_coords_s, y_coords_s, c = "k")
    x_coords_e = [ra * np.cos(end / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.0001, 0.0001)]
    y_coords_e = [ra * np.sin(end / 180 * np.pi) for ra in np.arange(start_radius, radius + 0.0001, 0.0001)]
    plt.plot(x_coords_e, y_coords_e, c = "k") 
    
    if end >= 0 and end < 90:
        q = 1
    if end >= 90 and end < 180:
        q = 2
    if end >= 180 and end < 270:
        q = 3
    if end >= 270 and end < 360:
        q = 4
 
    plt.fill_between(x_coords_e, y_coords_e, color = color_use) 
    plt.fill_between(x_coords_s, y_coords_s, color = color_use)
    plt.fill_between(x_coords_arc, y_coords_arc, color = color_use) 
    plt.fill_between(x_coords_arcb, y_coords_arcb, color = color_use) 
 
    '''
    if q == 1:
        val = min(min(min(y_coords_arc), min(y_coords_arcb)), min(min(y_coords_e), min(y_coords_s)))

    if q == 2:
        val = max(max(max(x_coords_arc), max(x_coords_arcb)), max(max(x_coords_e), max(x_coords_s)))

    if q == 3:
        val = max(max(max(y_coords_arc), max(y_coords_arcb)), max(max(y_coords_e), max(y_coords_s)))

    if q == 4:
        val = min(min(min(x_coords_arc), min(x_coords_arcb)), min(min(x_coords_e), min(x_coords_s))) 

    line_down_e = [val for y in y_coords_e]
    line_down_a = [val for y in y_coords_arc]  
    line_down_s = [val for y in y_coords_s]  
    line_down_b = [val for y in y_coords_arcb]  
   
    if q == 1 or q == 3:
        plt.fill_between(x_coords_e, y_coords_e, line_down_e, color = color_use)
        plt.fill_between(x_coords_arc, y_coords_arc, line_down_a, color = color_use) 
        plt.fill_between(x_coords_s, y_coords_s, line_down_s, color = "white") 
        plt.fill_between(x_coords_arcb, y_coords_arcb, line_down_b, color = next_color) 
    else: 
        plt.fill_betweenx(y_coords_e, x_coords_e, line_down_e, color = color_use)
        plt.fill_betweenx(y_coords_arc, x_coords_arc, line_down_a, color = color_use) 
        plt.fill_betweenx(y_coords_s, x_coords_s, line_down_s, color = "white") 
        plt.fill_betweenx(y_coords_arcb, x_coords_arcb, line_down_b, color = next_color) 
    '''
        
plot_arc(4, 2, 30, 45, "blue")
plot_arc(4, 2, 85, 95, "blue")
plot_arc(4, 2, 120, 150, "blue")
plot_arc(4, 2, 175, 185, "blue")
plot_arc(4, 2, 200, 230, "blue")
plot_arc(4, 2, 265, 275, "blue")
plot_arc(4, 2, 300, 320, "blue")
plot_arc(4, 2, 355, 5, "blue")
plt.show()

for file in os.listdir("data2"):
    file2read = netcdf.NetCDFFile('data2/' + file,'r')

    start_date = datetime(year = 1993, month = 1, day = 1)
    num_obs = 0
    
    for j, lat in enumerate(file2read.variables["latitude"]):
        for k, long in enumerate(file2read.variables["longitude"]):
            wave_heights = file2read.variables["sla"][:, j, k]
            if min(wave_heights) != max(wave_heights) and not np.isnan(min(wave_heights)):

                num_obs += 1

                vgosa = file2read.variables["vgosa"][:, j, k]
                ugosa = file2read.variables["ugosa"][:, j, k]
 
                tgosa = [np.sqrt(ugosa[i] ** 2 + vgosa[i] ** 2) for i in range(len(ugosa))] 
                bin_ranges = [(5 + i * 10, 15 + i * 10) for i in range(35)]
             
                angle_all = []

                wave_bins_for_bin = dict()
                for b in bin_ranges:
                    wave_bins_for_bin[b] = dict()
                wave_bins_for_bin[(355, 5)] = dict()

                abs_wave_heights = [abs(w) for w in wave_heights]
                wave_bins_starts = np.arange(min(abs_wave_heights), max(abs_wave_heights), (max(abs_wave_heights) - min(abs_wave_heights)) / 6)
                wave_bins = [(wave_bins_starts[i], wave_bins_starts[i + 1]) for i in range(len(wave_bins_starts) - 1)]
                
                for b in bin_ranges:
                    for wb in wave_bins:
                        wave_bins_for_bin[b][wb] = 0
                    wave_bins_for_bin[b][(wave_bins_starts[-1], max(wave_heights)) ] = 0

                for wb in wave_bins:
                    wave_bins_for_bin[(355, 5)][wb] = 0
                wave_bins_for_bin[(355, 5)][(wave_bins_starts[-1], max(abs_wave_heights)) ] = 0

                larger_than_points = np.arange(min(abs_wave_heights), max(abs_wave_heights), (max(abs_wave_heights) - min(abs_wave_heights)) / 100)
                probability_of_larger = dict()

                for b in bin_ranges:
                    probability_of_larger[b] = dict()
                    for l in larger_than_points:
                        probability_of_larger[b][l] = 0

                probability_of_larger[(355, 5)] = dict()
                for l in larger_than_points:
                    probability_of_larger[(355, 5)][l] = 0

                for i in range(len(ugosa)):
                    ang = 0
                    if ugosa[i] != 0:
                        ang = (np.arctan(vgosa[i] / ugosa[i]) / np.pi * 180 + 360) % 360
                    elif vgosa[i] > 0:
                        ang = 90
                    elif vgosa[i] < 0:
                        ang = 270
                    angle_all.append(ang)
                    
                    bin_used = (355, 5)
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
                            
                ax = WindroseAxes.from_ax()
                ax.bar(angle_all, abs_wave_heights, nsector = 36)
                ax.set_legend()
                plt.show()
                plt.close()

                ax2 = WindAxes.from_ax() 
                bins = np.arange(0, max(abs_wave_heights) + 0.01, 0.01)
                bins = bins[1:]
                ax2, params = ax2.pdf(abs_wave_heights, bins = bins)
                print(params)

                rcs = random_colors(len(wave_bins) + 1) 
                for b in dict(sorted(wave_bins_for_bin.items(), key=lambda item: item[0], reverse = True)):
                    sum_r = 0
                    for ci, wb in enumerate(dict(sorted(wave_bins_for_bin[b].items(), key=lambda item: item[0], reverse = True))): 
                        print(b, wb, wave_bins_for_bin[b][wb] / len(wave_heights) * 100)
                        sum_r_new = sum_r + wave_bins_for_bin[b][wb] / len(wave_heights) * 100 
                        print(ci, len(rcs)) 
                        if ci != 0:
                            nc = rcs[ci - 1]
                        else:
                            nc = "white"
                        plot_arc(sum_r_new, sum_r, b[0], b[1], rcs[ci], nc)
                        sum_r = sum_r_new
                plt.show()
                plt.close()

                print(wave_bins)

                for b in probability_of_larger:
                    if sum(list(wave_bins_for_bin[b].values())) == 0:
                        continue
                    xs = []
                    ys = []
                    for l in larger_than_points:
                        ys.append(l)
                        xs.append(probability_of_larger[b][l] / sum(list(wave_bins_for_bin[b].values())) * 100)
                    plt.plot(xs, ys, label = str(b))
                plt.legend()
                plt.ylabel("Elevation (m)")
                plt.xlabel("Probability of exceedance (%)")
                plt.show()
                
                time_deltas = file2read.variables["time"][0:] - file2read.variables["time"][0]
                datetimes = [datetime.strftime(start_date + timedelta(days = int(time_delta)), "%d.%m.%Y.") for time_delta in time_deltas]
                plt.title("long: " + str(long) + " lat: " + str((lat)))
                plt.plot(time_deltas, wave_heights)
                steps = list(range(0, len(wave_heights), 7 * 365))
                steps.append(len(wave_heights))
                for i in range(len(steps) - 1):
                    wave_heights_sorted = sorted(wave_heights[steps[i]:steps[i + 1]])
                    upper_third = wave_heights_sorted[- len(wave_heights_sorted) // 3:] 
                    mean_upper_third = np.mean(upper_third)
                    plt.plot(time_deltas[steps[i]:steps[i + 1]], [mean_upper_third for t in time_deltas[steps[i]:steps[i + 1]]])
                    plt.plot(time_deltas[steps[i]:steps[i + 1]], [- mean_upper_third for t in time_deltas[steps[i]:steps[i + 1]]])
                indexes_plot = range(0, len(datetimes), 7 * 365)
                datetimes_plot = [datetimes[ix] for ix in indexes_plot]
                plt.xticks(ticks = indexes_plot, labels = datetimes_plot)
                plt.xlabel("Date")
                plt.ylabel("Elevation (m)")
                plt.show()
                plt.close()
                
                scale_parameter = mean_upper_third * 8 / 9.86 / 1.029
                rayleigh = [len(time_deltas) * x / scale_parameter * np.e ** (- x ** 2 / (2 * scale_parameter) ** 2) for x in np.arange(0, max(wave_heights), max(wave_heights) / 100)]
                plt.hist(wave_heights, bins = 10)
                #plt.show()
                plt.close()
                plt.plot(np.arange(0, max(wave_heights), max(wave_heights) / 100), rayleigh)
                #plt.show()
                

                plt.close()
                
    str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
    print(str_name, num_obs)
    print(file2read.variables["time"][-1] - file2read.variables["time"][0])
    file2read.close()

    if not os.path.isfile('data2/' + str_name + ".nc"):
        os.rename('data2/' + file, 'data2/' + str_name + ".nc")