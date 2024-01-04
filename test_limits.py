import pandas as pd 
import matplotlib.pyplot as plt
import os
import numpy as np

ang_limits = dict()
ang_limits["LDZA"] = [0, 13, 75, 115, 140, 165, 180, 215, 280, 318, 360]
ang_limits["EGLL"] = [0, 60, 150, 180, 210, 255, 340, 360]
ang_limits["EDDF"] = [0, 14, 40, 95, 115, 137, 165, 180, 230, 265, 285, 310, 347, 360]
ang_limits["EDDT"] = [0, 25, 35, 50, 70, 100, 141, 161, 200, 255, 295, 325, 360]
ang_limits["EDDM"] = [0, 8, 44, 72, 115, 161, 215, 265, 280, 300, 337, 360]
ang_limits["YSSY"] = [0, 44, 90, 123, 143, 159, 169, 200, 240, 320, 330, 340, 350, 360]
ang_limits["YMML"] = [0, 40, 60, 100, 151, 169, 200, 320, 345, 360]
ang_limits["KLAX"] = [0, 17, 75, 127, 162, 200, 270, 325, 342, 360]
ang_limits["KJFK"] = [0, 22, 55, 120, 150, 158, 167, 205, 216, 287, 320, 339, 360]

plane_classes = os.listdir("trajs")
marks = ["valid", "test", "train"] 
starts = list(ang_limits.keys())

ends = {start: [] for start in starts} 

longs = {start: {mark: [] for mark in marks} for start in starts}
lats = {start: {mark: [] for mark in marks} for start in starts}
desti = {start: {mark: [] for mark in marks} for start in starts}

for plane_class in plane_classes: 

    for mark in marks:

        for first_part in starts:
            
            if not os.path.isdir("trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                continue

            for filename_short in os.listdir("trajs/" + plane_class + "/" + mark + "/" + first_part + "/"):
                
                second_part = filename_short.replace(".csv", "").split("_")[-1]

                if len(ends[first_part]) > 0 and second_part not in ends[first_part]:
                    continue
 
                filename = "trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + filename_short

                if not os.path.isfile(filename):
                    continue

                pd_file = pd.read_csv(filename, index_col = False)

                pd_file['group'] = pd_file['timestep'].eq(0).cumsum()
                df = pd_file.groupby('group')

                dfs = []
                for name, data in df:
                    dfs.append(data)
                    longs[first_part][mark].append(list(data["lon"]))
                    lats[first_part][mark].append(list(data["lat"]))
                    desti[first_part][mark].append(list(data["toICAO"]))

xoffset = dict()
yoffset = dict()
ang = dict()
label_ang = dict() 
dict_label_ang = dict()
dict_label_desti = dict()
dir_for_airport = dict()

for first_part in starts:

    xoffset[first_part] = dict()
    yoffset[first_part] = dict()
    ang[first_part] = dict()
    label_ang[first_part] = dict() 
    dict_label_ang[first_part] = dict()
    dict_label_desti[first_part] = dict()
    dir_for_airport[first_part] = dict()

    for mark in marks:

        xoffset[first_part][mark] = [[] for i in range(len(longs[first_part][mark]))]
        yoffset[first_part][mark] = [[] for i in range(len(longs[first_part][mark]))]

        for i in range(len(xoffset[first_part][mark])):
            xoffset[first_part][mark][i] = [long - longs[first_part][mark][i][0] for long in longs[first_part][mark][i]]
            yoffset[first_part][mark][i] = [lat - lats[first_part][mark][i][0] for lat in lats[first_part][mark][i]]
 
        X = [] 
        Y = []
        ang[first_part][mark] = []
        label_ang[first_part][mark] = []

        for i in range(len(xoffset[first_part][mark])):
            X.append([xoffset[first_part][mark][i][-1], yoffset[first_part][mark][i][-1]]) 
            Y.append(desti[first_part][mark][i][0])
            ang_one = (360 + np.arctan2(yoffset[first_part][mark][i][-1], xoffset[first_part][mark][i][-1]) / np.pi * 180) % 360
            ang[first_part][mark].append(ang_one)
            for i in range(len(ang_limits[first_part]) - 1):
                if ang_one >= ang_limits[first_part][i] and ang_one < ang_limits[first_part][i + 1]:
                    label_ang[first_part][mark].append(i)
                    break 
   
    plt.title(first_part)
    plt.hist([ang[first_part]["train"], ang[first_part]["test"], ang[first_part]["valid"]], bins = 100, stacked = True)

    for val in ang_limits[first_part]:
        plt.axvline(val)

    plt.show()
    plt.close()

    plt.title(first_part)
    plt.hist([ang[first_part]["train"], ang[first_part]["test"], ang[first_part]["valid"]], bins = ang_limits[first_part], stacked = True)
    plt.show()
    plt.close() 