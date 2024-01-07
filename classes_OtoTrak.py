import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np

def load_object(file_name): 
    with open(file_name, 'rb') as file_object:
        data = pickle.load(file_object) 
        file_object.close()
        return data
    
def preprocess_long_lat(long_list, lat_list):
    x_dir = long_list[0] < long_list[1]
    y_dir = lat_list[0] < lat_list[1]
 
    long_list2 = [x - min(long_list) for x in long_list]
    lat_list2 = [y - min(lat_list) for y in lat_list]
    if x_dir == False: 
        long_list2 = [max(long_list2) - x for x in long_list2]
    if y_dir == False:
        lat_list2 = [max(lat_list2) - y for y in lat_list2]

    return long_list2, lat_list2    
 
all_subdirs = os.listdir("../OtoTrak-Data-Test")
ws = 20
 
classes = {"I": 0, "D": 0, "NF": 0, "NM": 0}
num_infls_long = dict()
num_infls_lat = dict()
num_infls_all = dict()
num_infls_mrkr = dict()

anomaly_classes = set()
non_anomaly_classes = set()

order_of_mrkrs = []
 
for subdir_name in all_subdirs:
        
        if not os.path.isdir("../OtoTrak-Data-Test/" + subdir_name) or "Vehicle" not in subdir_name:
            continue 
        print(subdir_name)
        
        all_files = os.listdir("../OtoTrak-Data-Test/" + subdir_name + "/cleaned_csv/") 

        bad_rides_filenames = dict()
        if os.path.isfile("../OtoTrak-Data-Test/" + subdir_name + "/bad_rides_filenames"):
            bad_rides_filenames = load_object("../OtoTrak-Data-Test/" + subdir_name + "/bad_rides_filenames")

        gap_rides_filenames = dict()
        if os.path.isfile("../OtoTrak-Data-Test/" + subdir_name + "/gap_rides_filenames"):
            gap_rides_filenames = load_object("../OtoTrak-Data-Test/" + subdir_name + "/gap_rides_filenames")
 
        for some_file in all_files:   
            if subdir_name + "/cleaned_csv/" + some_file in bad_rides_filenames or subdir_name + "/cleaned_csv/" + some_file in gap_rides_filenames:
                #print("Skipped ride", some_file)
                continue
            #print("Used ride", some_file)
            file_with_ride = pd.read_csv("../OtoTrak-Data-Test/" + subdir_name + "/cleaned_csv/" + some_file)

            longitudes = list(file_with_ride["fields_longitude"])
            latitudes = list(file_with_ride["fields_latitude"])  

            order_of_mrkrs.append([])
            for x in range(0, len(longitudes), ws):
                long = longitudes[x:x + ws]
                lat = latitudes[x:x + ws] 
 
                long_diff = [long[i] - long[0] for i in range(len(long))]
                lat_diff = [lat[i] - lat[0] for i in range(len(long))] 
                points = set([(long[i], lat[i]) for i in range(len(long))])
                
                error_found = len(points) < 3 or len(set(long)) < 2 or len(set(lat)) < 2
                for i in range(1, len(long_diff)):
                    if long_diff[i] == 0 and lat_diff[i] == 0:
                        error_found = True
                        break
                
                if error_found:  
                    continue
                  
                angle_all = []
                radius_all = []
                for i in range(1, len(long_diff)):
                    radius_all.append(np.sqrt(lat_diff[i] ** 2 + long_diff[i] ** 2))
                    if long_diff[i] != 0:
                        angle_all.append(np.arctan(lat_diff[i] / long_diff[i]))
                    else:
                        if lat_diff[i] > 0:
                            angle_all.append(90)
                        elif lat_diff[i] < 0:
                            angle_all.append(270) 

                long_no_move = [radius_all[i] * np.cos(angle_all[i]) for i in range(len(radius_all))]
                lat_no_move = [radius_all[i] * np.sin(angle_all[i]) for i in range(len(radius_all))] 
                long_new = [radius_all[i] * np.cos(angle_all[i] - angle_all[-1]) for i in range(len(radius_all))]
                lat_new = [radius_all[i] * np.sin(angle_all[i] - angle_all[-1]) for i in range(len(radius_all))] 
                long_no_move.insert(0, 0)
                lat_no_move.insert(0, 0)
                long_new.insert(0, 0)
                lat_new.insert(0, 0)

                long_new, lat_new = preprocess_long_lat(long_new, lat_new)
                long_no_move, lat_no_move = preprocess_long_lat(long_no_move, lat_no_move)
  
                long_sgn = [long_new[i + 1] > long_new[i] for i in range(len(long_new) - 1)]
                lat_sgn = [lat_new[i + 1] > lat_new[i] for i in range(len(lat_new) - 1)]

                long_change_sgn = [long_sgn[i + 1] != long_sgn[i] for i in range(len(long_sgn) - 1)]
                lat_change_sgn = [lat_sgn[i + 1] != lat_sgn[i] for i in range(len(lat_sgn) - 1)]
 
                infls_long = []
                infls_lat = []
                infls_long_lat = []
                mrkr = ""
                for i in range(len(long_change_sgn)):
                    if long_change_sgn[i] or lat_change_sgn[i] :
                        infls_long_lat.append(i + 1)
                        #mrkr += "x" + str(int(long_sgn[i]))
                        #mrkr += str(int(long_sgn[i + 1]))
                        #mrkr += "y" + str(int(lat_sgn[i]))
                        #mrkr += str(int(lat_sgn[i + 1]))
                        comp_str_long = str(int(long_sgn[i])) + str(int(long_sgn[i + 1]))
                        comp_str_lat= str(int(lat_sgn[i])) + str(int(lat_sgn[i + 1]))
                        int_comp = int(comp_str_long + comp_str_lat, base = 2)
                        mrkr += str(hex(int_comp))[2:]
                    if long_change_sgn[i]:
                        infls_long.append(i + 1)
                    if lat_change_sgn[i]:
                        infls_lat.append(i + 1) 

                if len(infls_long) == 0:
                    if len(infls_lat) == 0: 
                        plt.plot(long_new, lat_new)
                        plt.show()

                        print(len(lat_sgn))
                        print(len(long_new))
                        if lat_sgn[0]:
                            class_me = "I" 
                        else:
                            class_me = "D"
                    else:
                        class_me = "NM"
                else:
                    class_me = "NF"
                classes[class_me] += 1
 
                #x_mirrored_mrkr = mrkr.replace("x00", "z11").replace("x11", "z00").replace("x01", "z10").replace("x10", "z01").replace("z", "x")
                #y_mirrored_mrkr = mrkr.replace("y00", "k11").replace("y11", "k00").replace("y01", "k10").replace("y10", "k01").replace("k", "y")
                #xy_mirrored_mrkr = mrkr.replace("x00", "z11").replace("x11", "z00").replace("x01", "z10").replace("x10", "z01").replace("z", "x").replace("y00", "k11").replace("y11", "k00").replace("y01", "k10").replace("y10", "k01").replace("k", "y")

                #if x_mirrored_mrkr in num_infls_mrkr:
                    #mrkr = x_mirrored_mrkr

                #if y_mirrored_mrkr in num_infls_mrkr:
                    #mrkr = y_mirrored_mrkr

                #if xy_mirrored_mrkr in num_infls_mrkr:
                    #mrkr = xy_mirrored_mrkr
                 
                if len(infls_lat) not in num_infls_lat:
                    num_infls_lat[len(infls_lat)] = 0
                num_infls_lat[len(infls_lat)] += 1
                if len(infls_long) not in num_infls_long:
                    num_infls_long[len(infls_long)] = 0
                num_infls_long[len(infls_long)] += 1
                if len(infls_long_lat) not in num_infls_all:
                    num_infls_all[len(infls_long_lat)] = 0
                num_infls_all[len(infls_long_lat)] += 1
                if mrkr not in num_infls_mrkr:
                    num_infls_mrkr[mrkr] = 0
                num_infls_mrkr[mrkr] += 1

                order_of_mrkrs[-1].append(mrkr)
                
                is_anom = mrkr[0] != "e"

                if not is_anom:
                    for ch in mrkr:
                        if ch != "d" and ch != "e":
                            is_anom = True
                            break

                if is_anom:
                    anomaly_classes.add(mrkr)
                else:
                    non_anomaly_classes.add(mrkr)

                if is_anom:
                    if not os.path.isdir("mrkr_draw/" + mrkr):
                        os.makedirs("mrkr_draw/" + mrkr)
                    plt.plot(long_new, lat_new, color = "k")
                    plt.axis("off")
                    plt.savefig("mrkr_draw/" + mrkr + "/" + str(ws) + "_" + subdir_name + "_" + some_file + "_" + str(x) + "_" + mrkr + ".png", bbox_inches = "tight")
                    plt.close()

print(classes)
print(num_infls_lat)
print(num_infls_long)
print(num_infls_all) 
lmt = sorted(list(set(num_infls_mrkr.values())))
cls = dict()
for l in lmt:
    clc = 0
    for cl in num_infls_mrkr:
        if num_infls_mrkr[cl] >= l:
            clc += 1
    cls[l] = clc
print(cls) 
print(lmt)
print(len(num_infls_mrkr))
for cl in num_infls_mrkr:
    if num_infls_mrkr[cl] > 1000:
        print(cl)
        
parent_of_mrkr = dict()
child_of_mrkr = dict()

keys_mrkr = sorted(list(num_infls_mrkr.keys()))
for mrkr in keys_mrkr: 
    parent_of_mrkr[mrkr] = set([mrkr]) 
    child_of_mrkr[mrkr] = set([mrkr]) 
    
for i, mrkr1 in enumerate(keys_mrkr): 
    for j, mrkr2 in enumerate(keys_mrkr[i + 1:]):  
        if mrkr1 == mrkr2[:len(mrkr1)]:
            parent_of_mrkr[mrkr2].add(mrkr1)
            child_of_mrkr[mrkr1].add(mrkr2)
        if mrkr2 == mrkr1[:len(mrkr2)]:
            parent_of_mrkr[mrkr1].add(mrkr2)
            child_of_mrkr[mrkr2].add(mrkr1)

dict_substr = dict()
num_occur_mrkr_str = dict()
num_infls_mrkr_str = dict()

new_mrkr = []

for mrkr in keys_mrkr:
    dict_substr[mrkr] = dict()

    nm = ""

    for x1 in range(0, 2):
        for x2 in range(0, 2):
            for y1 in range(0, 2):
                for y2 in range(0, 2):

                    if x1 == x2 and y1 == y2:
                        continue

                    str_comp = str(x1) + str(x2) + str(y1) + str(y2)
                    int_comp = int(str_comp, base = 2)
                    str_mark = str(hex(int_comp))[2:]
                        
                    dict_substr[mrkr][str_mark] = mrkr.count(str_mark)

                    if dict_substr[mrkr][str_mark]:
                        nm += str_mark

                    if str_mark not in num_occur_mrkr_str:
                        num_occur_mrkr_str[str_mark] = 0
                    num_occur_mrkr_str[str_mark] += dict_substr[mrkr][str_mark]

                    if dict_substr[mrkr][str_mark] != 0:
                        if str_mark not in num_infls_mrkr_str:
                            num_infls_mrkr_str[str_mark] = 0
                        num_infls_mrkr_str[str_mark] += num_infls_mrkr[mrkr]

    new_mrkr.append(nm)

print(num_occur_mrkr_str)
print(num_infls_mrkr_str)

print(set(new_mrkr))

occur_of_prev_mrkr = dict()
occur_of_prev_prev_mrkr = dict()

for i in range(len(order_of_mrkrs)):

    for j in range(len(order_of_mrkrs[i])):

        mrkr = order_of_mrkrs[i][j]

        if j > 0:

            prev_mrkr = order_of_mrkrs[i][j - 1]
            
            if mrkr not in occur_of_prev_mrkr:
                occur_of_prev_mrkr[mrkr] = dict()

            if prev_mrkr not in occur_of_prev_mrkr[mrkr]:
                occur_of_prev_mrkr[mrkr][prev_mrkr] = 0

            occur_of_prev_mrkr[mrkr][prev_mrkr] += 1

        if j > 1:

            prev_prev_mrkr = order_of_mrkrs[i][j - 2] 
            
            if mrkr not in occur_of_prev_prev_mrkr:
                occur_of_prev_prev_mrkr[mrkr] = dict()

            if prev_mrkr not in occur_of_prev_prev_mrkr[mrkr]:
                occur_of_prev_prev_mrkr[mrkr][prev_mrkr] = dict()

            if prev_prev_mrkr not in occur_of_prev_prev_mrkr[mrkr][prev_mrkr] :
                occur_of_prev_prev_mrkr[mrkr][prev_mrkr][prev_prev_mrkr] = 0

            occur_of_prev_prev_mrkr[mrkr][prev_mrkr][prev_prev_mrkr] += 1
            
percent_of_prev_mrkr = dict()
for mrkr in occur_of_prev_mrkr:
    percent_of_prev_mrkr[mrkr] = dict()
    for prev_mrkr in occur_of_prev_mrkr[mrkr]:
        percent_of_prev_mrkr[mrkr][prev_mrkr] = occur_of_prev_mrkr[mrkr][prev_mrkr] / sum(list(occur_of_prev_mrkr[mrkr].values())) * 100
 
for cl in num_infls_mrkr:
    if num_infls_mrkr[cl] > 1000:
        if cl in percent_of_prev_mrkr:
            print(cl)
            for x in percent_of_prev_mrkr[cl]:
                if percent_of_prev_mrkr[cl][x] >= 1:
                    print(cl, x, percent_of_prev_mrkr[cl][x])

percent_of_prev_prev_mrkr = dict()
for mrkr in occur_of_prev_prev_mrkr:
    percent_of_prev_prev_mrkr[mrkr] = dict()
    for prev_mrkr in occur_of_prev_prev_mrkr[mrkr]:
        percent_of_prev_prev_mrkr[mrkr][prev_mrkr] = dict()
        for prev_prev_mrkr in occur_of_prev_prev_mrkr[mrkr][prev_mrkr]:
            percent_of_prev_prev_mrkr[mrkr][prev_mrkr][prev_prev_mrkr] = occur_of_prev_prev_mrkr[mrkr][prev_mrkr][prev_prev_mrkr] / sum(list(occur_of_prev_prev_mrkr[mrkr][prev_mrkr].values())) * 100

'''
for cl in num_infls_mrkr:
    if num_infls_mrkr[cl] > 1000:
        if cl in percent_of_prev_prev_mrkr:
            for x in percent_of_prev_prev_mrkr[cl]:
                for y in percent_of_prev_prev_mrkr[cl][x]:
                    if percent_of_prev_prev_mrkr[cl][x][y] >= 10:
                        print(cl, x, y, percent_of_prev_prev_mrkr[cl][x][y])
'''

print(len(anomaly_classes), len(non_anomaly_classes))
natotal = 0
atotal = 0
max_size_of_anomaly_class = 0
min_size_of_non_anomaly_class = 1000000
max_size_of_non_anomaly_class = 0
min_size_of_anomaly_class = 1000000
max_anomaly_class = ""
min_anomaly_class = ""
max_non_anomaly_class = ""
min_non_anomaly_class = ""
for cl in num_infls_mrkr:
    if cl in anomaly_classes:
        atotal += num_infls_mrkr[cl]
        if num_infls_mrkr[cl] > max_size_of_anomaly_class:
            max_size_of_anomaly_class = num_infls_mrkr[cl]
            max_anomaly_class = cl
        if num_infls_mrkr[cl] < min_size_of_anomaly_class:
            min_size_of_anomaly_class = num_infls_mrkr[cl]
            min_anomaly_class = cl
    if cl in non_anomaly_classes:
        natotal += num_infls_mrkr[cl]
        if num_infls_mrkr[cl] > max_size_of_non_anomaly_class:
            max_size_of_non_anomaly_class = num_infls_mrkr[cl]
            max_non_anomaly_class = cl
        if num_infls_mrkr[cl] < min_size_of_non_anomaly_class:
            min_size_of_non_anomaly_class = num_infls_mrkr[cl]
            min_non_anomaly_class = cl

print(atotal, natotal)

print(min_anomaly_class, min_size_of_anomaly_class)
print(max_anomaly_class, max_size_of_anomaly_class)

print(min_non_anomaly_class, min_size_of_non_anomaly_class)
print(max_non_anomaly_class, max_size_of_non_anomaly_class)
