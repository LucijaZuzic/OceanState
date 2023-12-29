from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import os
for file in os.listdir("data"):
    file2read = netcdf.NetCDFFile('data/' + file,'r')

    '''
    print(file2read.variables.keys())
    print(np.shape(file2read.variables["VAVH_INST"]))
    print(np.shape(file2read.variables["time"]))
    print(np.shape(file2read.variables["latitude"]))
    print(np.shape(file2read.variables["longitude"]))
    print(file2read.variables["VAVH_INST"][0,:,:])
    print(file2read.variables["time"][0:]) 
    print(file2read.variables["latitude"][0:])
    print(file2read.variables["longitude"][0:])
    '''
    start_date = datetime(year = 2020, month = 1, day = 1)
    num_obs = 0
    for j, lat in enumerate(file2read.variables["latitude"]):
        for k, long in enumerate(file2read.variables["longitude"]):
            wave_heights = file2read.variables["VAVH_INST"][:, j, k]
            if min(wave_heights) != max(wave_heights):
                time_deltas = file2read.variables["time"][0:] - file2read.variables["time"][0]
                datetimes = [datetime.strftime(start_date + timedelta(days = int(time_delta)), "%d.%m.%Y.") for time_delta in time_deltas]
                plt.title("long: " + str(int(long)) + " lat: " + str((lat)))
                plt.plot(time_deltas, wave_heights / 1000)
                indexes_plot = range(0, len(datetimes), 363)
                datetimes_plot = [datetimes[ix] for ix in indexes_plot]
                plt.xticks(ticks = indexes_plot, labels = datetimes_plot)
                plt.xlabel("Date")
                plt.ylabel("Wave height (m)")
                plt.show()
                plt.close()
                wave_heights_sorted = sorted(wave_heights)
                scale_parameter = 1000
                rayleigh = [x / scale_parameter * np.e ** (- x ** 2 / (2 * scale_parameter) ** 2) for x in range(max(wave_heights))]
                plt.hist(wave_heights, bins = 100)
                plt.show()
                plt.close()
                plt.plot(rayleigh)
                plt.show()
                plt.close()

                num_obs += 1
                
    str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
    print(str_name, num_obs)
    print(file2read.variables["time"][-1] - file2read.variables["time"][0])
    file2read.close()

    #os.rename('data/' + file, 'data/' + str_name + ".nc")
   