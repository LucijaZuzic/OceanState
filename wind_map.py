import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
import os 
from utilities import load_object
import windrose
    
dict_xval_loc = load_object("location_data/dict_xval_loc")
dict_yval_loc = load_object("location_data/dict_yval_loc")
  
for loc in dict_xval_loc:

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

                if len(found_x) == 0:
                    continue

                proj = ccrs.PlateCarree()
                fig = plt.figure(figsize = (12, 6))
                # Draw main ax on top of which we will add windroses
                main_ax = fig.add_subplot(1, 1, 1, projection = proj)
                main_ax.set_extent([min(found_x) - 0.125, max(found_x) + 0.125, min(found_y) - 0.125, max(found_y) + 0.125], crs = proj)
                main_ax.gridlines(draw_labels = True)
                main_ax.coastlines()

                request = cimgt.OSM()
                main_ax.add_image(request, 12)

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
                                      
                                '''
                                # Inset axe it with a fixed size
                                wrax_fixed = inset_axes(main_ax,
                                        width=1,                             # size in inches
                                        height=1,                            # size in inches
                                        loc='center',                        # center bbox at given position
                                        bbox_to_anchor=(cham_lon, cham_lat), # position of the axe
                                        bbox_transform=main_ax.transData,    # use data coordinate (not axe coordinate)
                                        axes_class=windrose.WindroseAxes,    # specify the class of the axe
                                        )
                                '''

                                # Inset axe with size relative to main axe
                                height_deg = 0.1
                                wrax_relative = inset_axes(main_ax,
                                        width = "100%",                        # size in % of bbox
                                        height = "100%",                       # size in % of bbox
                                        #loc='center',  # don't know why, but this doesn't work.
                                        # specify the center lon and lat of the plot, and size in degree
                                        bbox_to_anchor = (long - height_deg / 2, lat - height_deg / 2, height_deg, height_deg),
                                        bbox_transform = main_ax.transData,
                                        axes_class = windrose.WindroseAxes,
                                        )

                                wrax_relative.bar(angle_all, abs_wave_heights, normed = True, nsector = 36) 
                                for ax in [wrax_relative]:
                                    ax.tick_params(labelleft = False, labelbottom = False)
 
            if not os.path.isdir("wind_rose/" + str(loc)):
                os.makedirs("wind_rose/" + str(loc))

            plt.savefig("wind_rose/" + str(loc) + "/wind_rose_" + str(loc) + "_all.png", bbox_inches = "tight") 
            plt.close()
  
            str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
            file2read.close()

            if not os.path.isfile('data2/' + str_name + ".nc"):
                os.rename('data2/' + file, 'data2/' + str_name + ".nc")