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
 
        plt.title(first_part + " " + mark)  
        plt.hist(ang[first_part][mark], bins = 100) 

        for val in ang_limits[first_part]:
            plt.axvline(val) 

        plt.show()
        plt.close()

        plt.title(first_part + " " + mark)
        plt.hist(ang[first_part][mark], bins = ang_limits[first_part])
        plt.show()
        plt.close()

        dict_label_ang[first_part][mark] = dict()

        for i, labela in enumerate(label_ang[first_part][mark]):

            if labela not in dict_label_ang[first_part][mark]:
                dict_label_ang[first_part][mark][labela] = []
            dict_label_ang[first_part][mark][labela].append(X[i])

        dict_label_desti[first_part][mark] = dict()

        for i, labela in enumerate(label_ang[first_part][mark]):
            
            if labela not in dict_label_desti[first_part][mark]:
                dict_label_desti[first_part][mark][labela] = []
            dict_label_desti[first_part][mark][labela].append(Y[i])

        dir_for_airport[first_part][mark] = dict()
   
        for labela in range(len(ang_limits[first_part]) - 1):

            if labela not in dict_label_desti[first_part][mark]:
                continue

            new_dict_label = dict()

              
            for val in set(dict_label_desti[first_part][mark][labela]):
                new_dict_label[val] = dict_label_desti[first_part][mark][labela].count(val)

                if val not in dir_for_airport[first_part][mark]:
                    dir_for_airport[first_part][mark][val] = dict()

                dir_for_airport[first_part][mark][val]["[" + str(ang_limits[first_part][labela]) + ", " + str(ang_limits[first_part][labela + 1]) + ">"] = new_dict_label[val]
                 
            dict_label_desti[first_part][mark][labela] = new_dict_label
              
        plt.title(first_part + " " + mark)

        for labela in range(len(ang_limits[first_part]) - 1):

            if labela not in dict_label_ang[first_part][mark]:
                continue

            xs = [p[0] for p in dict_label_ang[first_part][mark][labela]]
            ys = [p[1] for p in dict_label_ang[first_part][mark][labela]] 

            plt.scatter(xs, ys, label = "[" + str(ang_limits[first_part][labela]) + ", " + str(ang_limits[first_part][labela + 1]) + ">")
        
        plt.legend()
        plt.show()
        plt.close() 
        
        for labela in range(len(ang_limits[first_part]) - 1):
            
            if labela not in dict_label_desti[first_part][mark]:
                continue

            plt.title(first_part + " " + mark + " [" + str(ang_limits[first_part][labela]) + ", " + str(ang_limits[first_part][labela + 1]) + ">")
            plt.pie(list(dict_label_desti[first_part][mark][labela].values()), labels = list(dict_label_desti[first_part][mark][labela].keys()), autopct = "%1.1f%%")
            plt.show()
            plt.close()

        for airport in sorted(list(set(Y))):
              
            plt.title(first_part + " " + mark + " " + airport)
            plt.pie(list(dir_for_airport[first_part][mark][airport].values()), labels = list(dir_for_airport[first_part][mark][airport].keys()), autopct = "%1.1f%%")
            plt.show()
            plt.close()

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

    plt.title(first_part)

    for labela in range(len(ang_limits[first_part]) - 1): 

        xs_all_mark = []
        ys_all_mark = []

        for mark in marks:
            if labela not in dict_label_ang[first_part][mark]:
                continue

            xs_all_mark += [p[0] for p in dict_label_ang[first_part][mark][labela]]
            ys_all_mark += [p[1] for p in dict_label_ang[first_part][mark][labela]] 

        plt.scatter(xs_all_mark, ys_all_mark, label = " [" + str(ang_limits[first_part][labela]) + ", " + str(ang_limits[first_part][labela + 1]) + ">")
    
    plt.legend()
    plt.show()
    plt.close()
    
    new_dict_dest = dict()

    for labela in range(len(ang_limits[first_part]) - 1):

        new_dict_dest[labela] = dict() 

        for mark in marks:
        
            if labela not in dict_label_desti[first_part][mark]:
                continue

            for airport in dict_label_desti[first_part][mark][labela]:

                if airport not in new_dict_dest[labela]:
                    new_dict_dest[labela][airport] = 0

                new_dict_dest[labela][airport] += dict_label_desti[first_part][mark][labela][airport]
        
    for labela in range(len(ang_limits[first_part]) - 1):

        plt.title(first_part + " [" + str(ang_limits[first_part][labela]) + ", " + str(ang_limits[first_part][labela + 1]) + ">")
        plt.pie(list(new_dict_dest[labela].values()), labels = list(new_dict_dest[labela].keys()), autopct = "%1.1f%%")
        plt.show()
        plt.close()
        
    new_dict_airport = dict()

    for mark in marks:

        for airport in dir_for_airport[first_part][mark]:

            new_dict_airport[airport] = dict() 
 
            for labela in dir_for_airport[first_part][mark][airport]:
 
                if labela not in new_dict_airport[airport]:
                    new_dict_airport[airport][labela] = 0

                new_dict_airport[airport][labela] += dir_for_airport[first_part][mark][airport][labela]
        
    for airport in sorted(list(new_dict_airport.keys())):

        plt.title(first_part + " " + airport)
        plt.pie(list(new_dict_airport[airport].values()), labels = list(new_dict_airport[airport].keys()), autopct = "%1.1f%%")
        plt.show()
        plt.close()