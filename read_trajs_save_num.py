import pandas as pd
import matplotlib.pyplot as plt
import os
 
plane_classes = os.listdir("trajs")
marks = ["train", "test", "valid"]
 
use_all = False
wanted_cons = []

for plane_class in plane_classes:
    
    if plane_class == "conns":
        continue

    pd_file_from = pd.read_csv("trajs/" + plane_class + "/test_fromICAO_" + plane_class + ".csv", index_col = False, header = None)
    pd_file_to = pd.read_csv("trajs/" + plane_class + "/test_toICAO_" + plane_class + ".csv", index_col = False, header = None)
    
    dict_from = dict()
    dict_to = dict()

    for i in range(len(pd_file_from[0])):
        dict_from[int(pd_file_from[1][i])] = str(pd_file_from[0][i])

    for i in range(len(pd_file_to[0])):
        dict_to[int(pd_file_to[1][i])] = str(pd_file_to[0][i])
       
    for mark in marks:

        if not os.path.isfile("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv"):
            continue

        if os.path.isfile("trajs/" + plane_class + "/conns/" + plane_class + "_" + mark + "_num_conns.csv"):

            pd_num_conns = pd.read_csv("trajs/" + plane_class + "/conns/" + plane_class + "_" + mark + "_num_conns.csv", index_col = False)
            
            found_conns = set()

            for ix in range(len(pd_num_conns["fromICAO"])):

                orig = pd_num_conns["fromICAO"][ix]
                desti = pd_num_conns["toICAO"][ix]

                str_name = str(orig) + "_" + str(desti)

                found_conns.add(str_name)
            
            all_found = True

            if use_all:
                wanted_cons = list(found_conns)

            for conn in wanted_cons:
                
                if conn not in found_conns:
                    continue

                first_part = conn.split("_")[0]

                if not os.path.isfile("trajs/" + plane_class + "/conns/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + conn + ".csv"):
                    all_found = False
                    break
            
            if all_found:
                continue
        
        pd_file = pd.read_csv("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv", index_col = False)
        
        print(plane_class, mark)

        num_conns = dict()
        ix_conns = dict()
        
        for ix in range(len(pd_file["fromICAO"])):

            orig = int(pd_file["fromICAO"][ix])
            desti = int(pd_file["toICAO"][ix])

            if orig not in dict_from or desti not in dict_to:
                continue

            orig = dict_from[orig]
            desti = dict_to[desti]
  
            str_name = str(orig) + "_" + str(desti)
            
            if str_name not in ix_conns:
                ix_conns[str_name] = []
            ix_conns[str_name].append(ix)
            
            if str_name not in num_conns:
                num_conns[str_name] = 0
            num_conns[str_name] += 1

        for conn in wanted_cons:

            if conn not in ix_conns:
                continue

            first_part = conn.split("_")[0]

            if os.path.isfile("trajs/" + plane_class + "/conns/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + conn + ".csv"):
                continue

            if not os.path.isdir("trajs/" + plane_class + "/conns/" + mark + "/" + first_part):
                os.makedirs("trajs/" + plane_class + "/conns/" + mark + "/" + first_part)

            df_new = pd_file.loc[ix_conns[conn]] 
            df_new.to_csv("trajs/" + plane_class + "/conns/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + conn + ".csv", index = False)

            new_pd = pd.read_csv("trajs/" + plane_class + "/conns/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + conn + ".csv", index_col = False)
 
        if os.path.isfile("trajs/" + plane_class + "/conns/" + plane_class + "_" + mark + "_num_conns.csv"):
            continue

        if not os.path.isdir("trajs/" + plane_class + "/conns"):
            os.makedirs("trajs/" + plane_class + "/conns")
        
        str_pr = "fromICAO,toICAO,num\n"
        for conn in num_conns: 
            parts = conn.split("_")
            str_pr += parts[0] + "," + parts[1] + "," + str(num_conns[conn]) + "\n"
        str_pr = str_pr[:-1] 

        file_save = open("trajs/" + plane_class + "/conns/" + plane_class + "_" + mark + "_num_conns.csv", "w")
        file_save.write(str(str_pr))
        file_save.close()