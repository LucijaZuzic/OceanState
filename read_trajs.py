import pandas as pd
import matplotlib.pyplot as plt
import os

pd_files = dict()
pd_files_from = dict()
pd_files_to = dict()

plane_classes = ["DH8D"]
marks = ["valid"]

max_num_con = 0
max_con = ""
num_conns = dict()

ix_conns = dict()
#wrong_ids = set()

for plane_class in plane_classes:
    
    if plane_class == "conns":
        continue

    pd_files_from[plane_class] = pd.read_csv("trajs/" + plane_class + "/test_fromICAO_" + plane_class + ".csv", index_col = False, header = None)
    pd_files_to[plane_class] = pd.read_csv("trajs/" + plane_class + "/test_toICAO_" + plane_class + ".csv", index_col = False, header = None)
    
    dict_from = dict()
    dict_to = dict()

    for i in range(len(pd_files_from[plane_class][0])):
        dict_from[int(pd_files_from[plane_class][1][i])] = str(pd_files_from[plane_class][0][i])

    for i in range(len(pd_files_to[plane_class][0])):
        dict_to[int(pd_files_to[plane_class][1][i])] = str(pd_files_to[plane_class][0][i])
     
    pd_files[plane_class] = dict()

    for mark in marks:

        if not os.path.isfile("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv"):
            continue
        
        pd_files[plane_class][mark] = pd.read_csv("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv", index_col = False)
        
        print(plane_class, mark)
        
        for ix in range(len(pd_files[plane_class][mark]["fromICAO"])):
            orig = int(pd_files[plane_class][mark]["fromICAO"][ix])
            desti = int(pd_files[plane_class][mark]["toICAO"][ix])

            if orig not in dict_from or desti not in dict_to:
                #wrong_ids.add((orig, desti))
                continue

            orig = dict_from[orig]
            desti = dict_to[desti]
  
            str_name = str(orig) + "_" + str(desti) 

            if str_name not in num_conns:
                num_conns[str_name] = 0
            num_conns[str_name] += 1
            
            if str_name not in ix_conns:
                ix_conns[str_name] = []
            ix_conns[str_name].append((plane_class, mark, ix))

            if num_conns[str_name] > max_num_con:
                max_num_con = num_conns[str_name]
                max_con = str_name

if "YMML_YSSY" in num_conns:
    max_con = "YMML_YSSY"
    max_num_con = num_conns[max_con]
    
print(max_con, max_num_con)
#print(wrong_ids)

'''
for con in dict(sorted(num_conns.items(), key=lambda item: item[1], reverse = True)):
    print(con, num_conns[con])
    max_con = con
    break
'''

longs = []
lats = []
times = []
icao24_vals = []
segment_starts = [0]

for conn_tuple in ix_conns[max_con]: 
    plane_class, mark, ix = conn_tuple
    longs.append(pd_files[plane_class][mark]["lon"][ix])
    lats.append(pd_files[plane_class][mark]["lat"][ix])
    times.append(pd_files[plane_class][mark]["time"][ix])
    icao24_vals.append(pd_files[plane_class][mark]["icao24"][ix])
    if len(icao24_vals) > 1 and icao24_vals[-1] != icao24_vals[-2]:
        segment_starts.append(len(icao24_vals) - 1)
segment_starts.append(len(icao24_vals))

for seg_ind in range(len(segment_starts) - 1):
    plt.plot([longs[segment_starts[seg_ind]], longs[segment_starts[seg_ind + 1] - 1]], [lats[segment_starts[seg_ind]], lats[segment_starts[seg_ind + 1] - 1]])
plt.show()