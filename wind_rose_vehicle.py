import os
import pandas as pd 
import matplotlib.pyplot as plt 
from utilities import load_object 
from windrose import WindroseAxes 
from scipy.io import netcdf
import  numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

location_vehicles = dict()
vehicle_location = dict()
  
dict_xval_loc = load_object("location_data/dict_xval_loc")
dict_yval_loc = load_object("location_data/dict_yval_loc")
  
all_subdirs = os.listdir("../OtoTrak-Data-Test")

location_vehicles = load_object("location_data/location_veh")

for loc in location_vehicles:

    for file in os.listdir("data2"):

        file_split = [int(v) for v in file.replace(".nc", "").split("_")]

        if dict_xval_loc[loc][0] >= file_split[0] and dict_xval_loc[loc][0] <= file_split[1] and dict_yval_loc[loc][0] >= file_split[2] and dict_yval_loc[loc][0] <= file_split[3]:
             
            file2read = netcdf.NetCDFFile('data2/' + file,'r')
 
            if dict_xval_loc[loc][0] >= file2read.variables["longitude"][0] and dict_xval_loc[loc][0] <= file2read.variables["longitude"][-1] and dict_yval_loc[loc][0] >= file2read.variables["latitude"][0] and dict_yval_loc[loc][0] <= file2read.variables["latitude"][-1]:
                
                found_x = []
                found_y = []

                for j, lat in enumerate(file2read.variables["latitude"]):
                    for k, long in enumerate(file2read.variables["longitude"]):
                        if long >= dict_xval_loc[loc][0] and long <= dict_xval_loc[loc][-1] and lat >= dict_yval_loc[loc][0] and lat <= dict_yval_loc[loc][-1]:
                            
                            wave_heights = file2read.variables["sla"][:, j, k]
  
                            if min(wave_heights) != max(wave_heights) and not np.isnan(min(wave_heights)):
                                found_x.append(long)
                                found_y.append(lat)

            file2read.close()

    if len(found_x) == 0:
        continue

    all_heading_for_point = dict()
    all_speed_for_point = dict()

    for ix in range(len(found_x)):
        all_heading_for_point[(found_x[ix], found_y[ix])] = []
        all_speed_for_point[(found_x[ix], found_y[ix])] = []
     
    for subdir_name in location_vehicles[loc]:
            
        if not os.path.isdir("../OtoTrak-Data-Test/" + subdir_name) or "Vehicle" not in subdir_name:
            continue 
        print(subdir_name)
        
        all_files = os.listdir("../OtoTrak-Data-Test/" + subdir_name + "/cleaned_csv/") 

        bad_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object(subdir_name + "/bad_rides_filenames")

        gap_rides_filenames = dict()
        if os.path.isfile(subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object(subdir_name + "/gap_rides_filenames")
 
        for some_file in all_files:   
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            #print("Used ride", some_file)
            file_with_ride = pd.read_csv("../OtoTrak-Data-Test/" + subdir_name + "/cleaned_csv/" + some_file)

            headings = list(file_with_ride["fields_direction"]) 
            speeds = list(file_with_ride["fields_speed"])  

            longi = list(file_with_ride["fields_longitude"]) 
            lati = list(file_with_ride["fields_latitude"])  
              
            for pix in range(len(longi)):

                mini_dist = 100000
                mini_point = (found_x[0], found_y[0])

                for ix in range(len(found_x)):
                    one_dist = np.sqrt((found_x[ix] - longi[pix]) ** 2 + (found_y[ix] - lati[pix]) ** 2)
                    if one_dist < mini_dist:
                        mini_dist = one_dist
                        mini_point = (found_x[ix], found_y[ix])

                all_heading_for_point[mini_point].append(headings[pix])
                all_speed_for_point[mini_point].append(speeds[pix])
   
    maxx = - 10000
    minx = 10000
    maxy = - 10000
    miny = 10000
 
    for ix in range(len(found_x)):
        
        if len(all_heading_for_point[(found_x[ix], found_y[ix])]) == 0:
            continue

        maxx = max(maxx, found_x[ix])
        minx = min(minx, found_x[ix]) 
        maxy = max(maxy, found_y[ix])
        miny = min(miny, found_y[ix]) 

    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize = (12, 6))
    # Draw main ax on top of which we will add windroses
    main_ax = fig.add_subplot(1, 1, 1, projection = proj)
    main_ax.set_extent([minx - 0.125, maxx + 0.125, miny - 0.125, maxy + 0.125], crs = proj)
    main_ax.gridlines(draw_labels = True)
    main_ax.coastlines()

    request = cimgt.OSM()
    main_ax.add_image(request, 12)

    for ix in range(len(found_x)):
        
        if len(all_heading_for_point[(found_x[ix], found_y[ix])]) == 0:
            continue

        # Inset axe with size relative to main axe
        height_deg = 0.1
        wrax_relative = inset_axes(main_ax,
                width = "100%",                        # size in % of bbox
                height = "100%",                       # size in % of bbox
                #loc='center',  # don't know why, but this doesn't work.
                # specify the center lon and lat of the plot, and size in degree
                bbox_to_anchor = (found_x[ix] - height_deg / 2, found_y[ix] - height_deg / 2, height_deg, height_deg),
                bbox_transform = main_ax.transData,
                axes_class = WindroseAxes,
                )

        wrax_relative.bar(all_heading_for_point[(found_x[ix], found_y[ix])], all_speed_for_point[(found_x[ix], found_y[ix])], normed = True, nsector = 36) 
        for ax in [wrax_relative]:
            ax.tick_params(labelleft = False, labelbottom = False)
  
    if not os.path.isdir("wind_rose/" + str(loc)):
        os.makedirs("wind_rose/" + str(loc))

    plt.savefig("wind_rose/" + str(loc) + "/wind_rose_" + str(loc) + "_vehicle.png", bbox_inches = "tight") 
    plt.close() 