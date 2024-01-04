import pandas as pd
import matplotlib.pyplot as plt
import os
 
plane_classes = ["A319", "A321"]
marks = ["train", "test", "valid"]
  
wanted_start = ["LDZA"]
wanted_end = ["EGLL"]

begin_str = ""

for ws in wanted_start:
    begin_str += ws + "-"
 
for we in wanted_end:
    begin_str += "-" + we 

begin_str = begin_str.replace("--", "_")

parts = begin_str.split("_")
first_part = parts[0]
second_part = parts[1]

df_all = pd.DataFrame()

for plane_class in plane_classes:
    
    if plane_class == "conns":
        continue

    pd_file_from = pd.read_csv("trajs/" + plane_class + "/test_fromICAO_" + plane_class + ".csv", index_col = False, header = None)
    pd_file_to = pd.read_csv("trajs/" + plane_class + "/test_toICAO_" + plane_class + ".csv", index_col = False, header = None)
     
    dict_from = {str(pd_file_from[0][i]): int(pd_file_from[1][i]) for i in range(len(pd_file_from[0]))}
    dict_to = {str(pd_file_to[0][i]): int(pd_file_to[1][i]) for i in range(len(pd_file_to[0]))}

    dict_from_reverse = {int(pd_file_from[1][i]): str(pd_file_from[0][i]) for i in range(len(pd_file_from[0]))}
    dict_to_reverse = {int(pd_file_to[1][i]): str(pd_file_to[0][i]) for i in range(len(pd_file_to[0]))}

    wanted_start_number = [dict_from[ws] for ws in wanted_start]
    wanted_end_number = [dict_to[we] for we in wanted_end]
       
    df_class = pd.DataFrame()

    for mark in marks:

        if not os.path.isfile("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv"):
            continue

        saved = False
        if os.path.isfile("trajs/" + plane_class + "/conns/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + begin_str + ".csv"):
            saved = True
        
        if not saved:
            pd_file = pd.read_csv("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv", index_col = False)
        else:
            pd_file = pd.read_csv("trajs/" + plane_class + "/conns/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + begin_str + ".csv", index_col = False)

        print(plane_class, mark)
        print(len(pd_file))

        if not saved:
            if len(wanted_start_number) > 0:
                pd_file = pd_file[pd_file["fromICAO"].isin(wanted_start_number)] 

            if len(wanted_end_number) > 0:
                pd_file = pd_file[pd_file["toICAO"].isin(wanted_end_number)]

            pd_file["fromICAO"] = pd_file["fromICAO"].replace(dict_from_reverse)
            pd_file["toICAO"] = pd_file["toICAO"].replace(dict_to_reverse)
            pd_file["plane_class"] = [plane_class for i in range(len(pd_file))]
            pd_file["mark"] = [mark for i in range(len(pd_file))]
        
        if len(pd_file):
            if len(df_all) == 0:
                df_all = pd_file
            else:
                df_all = pd.concat([df_all, pd_file])
                
            if len(df_class) == 0:
                df_class = pd_file
            else:
                df_class = pd.concat([df_class, pd_file])

            print(len(pd_file))
            print(len(df_all))

            if not os.path.isdir("trajs/" + plane_class + "/conns/" + mark + "/" + first_part):
                os.makedirs("trajs/" + plane_class + "/conns/" + mark + "/" + first_part)

            pd_file.to_csv("trajs/" + plane_class + "/conns/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + begin_str + ".csv")

    if not os.path.isdir("trajs/" + plane_class + "/conns/all/" + first_part):
        os.makedirs("trajs/" + plane_class + "/conns/all/" + first_part)

    df_class.to_csv("trajs/" + plane_class + "/conns/all/" + plane_class + "_" + begin_str + ".csv")
    
if not os.path.isdir("trajs/conns/" + first_part):
    os.makedirs("trajs/conns/" + first_part)

df_all.to_csv("trajs/conns/" + first_part + "/" + begin_str + ".csv")
        