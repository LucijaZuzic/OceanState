from scipy.io import netcdf
import matplotlib.pyplot as plt
import numpy as np
import os 
from utilities import load_object
from scipy import stats
   
dict_xval_loc = load_object("location_data/dict_xval_loc")
dict_yval_loc = load_object("location_data/dict_yval_loc")

g_const = 9.86
p_const = 1.029

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
 
                                abs_wave_heights = [abs(w) * 100 for w in wave_heights]  
                                        
                                wave_heights_sorted = sorted(abs_wave_heights)
                                upper_third = wave_heights_sorted[- len(wave_heights_sorted) // 3:] 
                                mean_upper_third = np.mean(upper_third) 
  
                                energy_part = 0
                                for val in abs_wave_heights:
                                    energy_part += val ** 2
                                power_part = energy_part / len(abs_wave_heights)
                                hrms = 4 * np.sqrt(power_part / (g_const * p_const)) 

                                plt.title("Location: " + str(loc) + " long: " + str(long) + " lat: " + str((lat)))
                                plt.xlabel("Wave Height (cm)")
                                plt.ylabel("Probability Density")

                                plt.hist(abs_wave_heights, density = True, bins = 100, label = "Recorded Waves") 

                                print(mean_upper_third)
                                scale_parameter = mean_upper_third / np.sqrt(2)
                                rayleigh = [x / (scale_parameter ** 2) * np.e ** (- x ** 2 / (2 * scale_parameter ** 2)) for x in np.arange(0, max(abs_wave_heights) + scale_parameter, (max(abs_wave_heights) + scale_parameter) / 100)]
                                rayleigh_x = [x - scale_parameter for x in np.arange(0, max(abs_wave_heights) + scale_parameter, (max(abs_wave_heights) + scale_parameter) / 100)]
                                plt.plot(rayleigh_x, rayleigh, label = "Estimated Reyleigh $H_{1/3}$")  

                                lambda_parameter = mean_upper_third  
                                m = 2
                                weibull = [m / lambda_parameter * (x / lambda_parameter) ** (m - 1) * np.e ** (- (x / lambda_parameter) ** m) for x in np.arange(0, max(abs_wave_heights) + lambda_parameter, (max(abs_wave_heights) + lambda_parameter) / 100)]
                                weibull_x = [x - lambda_parameter for x in np.arange(0, max(abs_wave_heights) + lambda_parameter, (max(abs_wave_heights) + lambda_parameter) / 100)]
                                plt.plot(weibull_x, weibull, label = "Estimated Weibull $H_{1/3}$") 
                                
                                print(hrms)
                                scale_parameter = hrms / np.sqrt(2)
                                rayleigh = [x / (scale_parameter ** 2) * np.e ** (- x ** 2 / (2 * scale_parameter ** 2)) for x in np.arange(0, max(abs_wave_heights) + scale_parameter, (max(abs_wave_heights) + scale_parameter) / 100)]
                                rayleigh_x = [x - scale_parameter for x in np.arange(0, max(abs_wave_heights) + scale_parameter, (max(abs_wave_heights) + scale_parameter) / 100)]
                                plt.plot(rayleigh_x, rayleigh, label = "Estimated Reyleigh $H_{rms}$") 

                                lambda_parameter = hrms  
                                m = 2
                                weibull = [m / lambda_parameter * (x / lambda_parameter) ** (m - 1) * np.e ** (- (x / lambda_parameter) ** m) for x in np.arange(0, max(abs_wave_heights) + lambda_parameter, (max(abs_wave_heights) + lambda_parameter) / 100)]
                                weibull_x = [x - lambda_parameter for x in np.arange(0, max(abs_wave_heights) + lambda_parameter, (max(abs_wave_heights) + lambda_parameter) / 100)]
                                plt.plot(weibull_x, weibull, label = "Estimated Weibull $H_{rms}$") 
                                
                                rayleigh_args = stats.rayleigh.fit(abs_wave_heights)
                                print(rayleigh_args) 
                                rayleigh_fit = [x / (rayleigh_args[1] ** 2) * np.e ** (- x ** 2 / (2 * rayleigh_args[1] ** 2)) for x in np.arange(0, max(abs_wave_heights) - rayleigh_args[0], (max(abs_wave_heights) - rayleigh_args[0]) / 100)]
                                rayleigh_fit_x = [x + rayleigh_args[0] for x in np.arange(0, max(abs_wave_heights) - rayleigh_args[0], (max(abs_wave_heights) - rayleigh_args[0]) / 100)]
                                plt.plot(rayleigh_fit_x, rayleigh_fit, label = "Fitted Reyleigh") 

                                if not os.path.isdir("wind_rose/" + str(loc)):
                                    os.makedirs("wind_rose/" + str(loc))
                                
                                plt.legend()

                                plt.savefig("wind_rose/" + str(loc) + "/rayleigh_" + str(loc) + "_long_" + str(long) + "_lat_" + str(lat) + ".png", bbox_inches = "tight") 
                                plt.close()
                 
            str_name = str(int(min(file2read.variables["longitude"][0:]))) + "_" + str(int(max(file2read.variables["longitude"][0:]))) + "_" + str(int(min(file2read.variables["latitude"][0:]))) + "_" + str(int(max(file2read.variables["latitude"][0:])))
            file2read.close()

            if not os.path.isfile('data2/' + str_name + ".nc"):
                os.rename('data2/' + file, 'data2/' + str_name + ".nc")