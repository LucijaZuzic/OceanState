import os
import pandas as pd
import pickle
import numpy as np

def load_object(file_name): 
    with open(file_name, 'rb') as file_object:
        data = pickle.load(file_object) 
        file_object.close()
        return data

location_vehicles = dict()
vehicle_location = dict()

min_long_loc = dict()
max_long_loc = dict()
min_lat_loc = dict()
max_lat_loc = dict()
    
all_subdirs = os.listdir("../OtoTrak-Data-Test")

for subdir_name in all_subdirs:
        
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

        min_long_veh = 1000
        max_long_veh = -1000
        min_lat_veh = 1000
        max_lat_veh = -1000

        for some_file in all_files:   
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            #print("Used ride", some_file)
            file_with_ride = pd.read_csv("../OtoTrak-Data-Test/" + subdir_name + "/cleaned_csv/" + some_file)

            longitudes = list(file_with_ride["fields_longitude"])

            min_long_veh = min(min_long_veh, min(longitudes))
            max_long_veh = max(max_long_veh, max(longitudes))

            latitudes = list(file_with_ride["fields_latitude"])  

            min_lat_veh = min(min_lat_veh, min(latitudes))
            max_lat_veh = max(max_lat_veh, max(latitudes))

            location_veh = file_with_ride["location_id"][0]
            
        if location_veh not in location_vehicles:
            location_vehicles[location_veh] = []

        if location_veh not in min_long_loc:
            min_long_loc[location_veh] = min_long_veh

        if location_veh not in max_long_loc:
            max_long_loc[location_veh] = max_long_veh

        if location_veh not in min_lat_loc:
            min_lat_loc[location_veh] = min_lat_veh

        if location_veh not in max_lat_loc:
            max_lat_loc[location_veh] = max_lat_veh

        location_vehicles[location_veh].append(subdir_name)
        vehicle_location[subdir_name] = location_veh
        min_long_loc[location_veh] = min(min_long_veh, min_long_loc[location_veh])
        max_long_loc[location_veh] = max(max_long_veh, max_long_loc[location_veh])
        min_lat_loc[location_veh] = min(min_lat_veh, min_lat_loc[location_veh])
        max_lat_loc[location_veh] = max(max_lat_veh, max_lat_loc[location_veh])

print(location_vehicles)
print(vehicle_location)
print(min_long_loc)
print(max_long_loc)
print(min_lat_loc)
print(max_lat_loc)
for loc in location_vehicles:
    print(loc, min_long_loc[loc], max_long_loc[loc], min_lat_loc[loc], max_lat_loc[loc])
    print(loc, np.floor(min_long_loc[loc]), np.floor(max_long_loc[loc]), np.floor(min_lat_loc[loc]), np.floor(max_lat_loc[loc]))
    print(loc, np.ceil(min_long_loc[loc]), np.ceil(max_long_loc[loc]), np.ceil(min_lat_loc[loc]), np.ceil(max_lat_loc[loc])) 