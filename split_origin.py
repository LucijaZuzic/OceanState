import pandas as pd
import os
import numpy as np

plane_classes = os.listdir("trajs")
marks = ["valid", "test", "train"] 

chunksize = 100000
 
for plane_class in plane_classes:

    if plane_class == "conns":
        continue
 
    pd_file_from = pd.read_csv("trajs/" + plane_class + "/test_fromICAO_" + plane_class + ".csv", index_col = False, header = None)
    pd_file_to = pd.read_csv("trajs/" + plane_class + "/test_toICAO_" + plane_class + ".csv", index_col = False, header = None)

    dict_from = {str(pd_file_from[0][i]): int(pd_file_from[1][i]) for i in range(len(pd_file_from[0]))}
    dict_to = {str(pd_file_to[0][i]): int(pd_file_to[1][i]) for i in range(len(pd_file_to[0]))}
  
    dict_from_reverse = {int(pd_file_from[1][i]): str(pd_file_from[0][i]) for i in range(len(pd_file_from[0]))}
    dict_to_reverse = {int(pd_file_to[1][i]): str(pd_file_to[0][i]) for i in range(len(pd_file_to[0]))} 

    for mark in marks:
        
        print(plane_class, mark)

        df_size = pd.DataFrame({"fromICAO": [], "toICAO": [], "plane_class": [], "mark": [], "num": []})    

        if not os.path.isfile("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv"):
            continue
  
        for chunk in pd.read_csv("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv", index_col = False, chunksize = chunksize):              
            
            pd_file = chunk
   
            pd_file["fromICAO"] = pd_file["fromICAO"].replace(dict_from_reverse)
            pd_file["toICAO"] = pd_file["toICAO"].replace(dict_to_reverse)
            pd_file["plane_class"] = [plane_class for i in range(len(pd_file))]
            pd_file["mark"] = [mark for i in range(len(pd_file))]

            pd_file["from-to"] = pd_file['fromICAO'].astype(str) + "_" + pd_file['toICAO'].astype(str)
            pd_file_groups = pd_file.groupby("from-to")
 
            for name, data in pd_file_groups: 

                begin_str = list(data["from-to"])[0]

                if "0" in begin_str:
                    continue

                first_part = list(data["fromICAO"])[0]
                second_part = list(data["toICAO"])[0]
  
                pd_file_old = pd.DataFrame()
                if not os.path.isdir("trajs/" + plane_class + "/" + mark + "/" + first_part):
                    os.makedirs("trajs/" + plane_class + "/" + mark + "/" + first_part)
                else:
                    if os.path.isfile("trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + begin_str + ".csv"):
                        pd_file_old = pd.read_csv("trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + begin_str + ".csv", index_col = False)

                pd_file = pd.concat([pd_file_old, data.drop(columns = ["from-to"])]).drop_duplicates().reset_index(drop = True)
                pd_file.to_csv("trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + begin_str + ".csv", index = False)
                print("trajs/" + plane_class + "/" + mark + "/" + first_part + "/" + plane_class + "_" + mark + "_" + begin_str + ".csv")
 
                if len(df_size[(df_size["fromICAO"] == first_part) & (df_size["toICAO"] == second_part) & (df_size["plane_class"] == plane_class) & (df_size["mark"] == mark)]):
                    df_size["num"] = np.where((df_size["fromICAO"] == first_part) & (df_size["toICAO"] == second_part) & (df_size["plane_class"] == plane_class) & (df_size["mark"] == mark), len(pd_file), df_size["num"])
                else:    
                    some_data = {"fromICAO": [], "toICAO": [], "plane_class": [], "mark": [], "num": []}
                    some_data["fromICAO"].append(first_part)
                    some_data["toICAO"].append(second_part)
                    some_data["plane_class"].append(plane_class)
                    some_data["mark"].append(mark)
                    some_data["num"].append(len(pd_file))
                    df_size = pd.concat([df_size, pd.DataFrame(some_data)]).drop_duplicates().reset_index(drop = True)

        df_size = df_size.sort_values(by = ["fromICAO", "toICAO", "plane_class", "mark", "num"])
        df_size["num"] = df_size["num"].astype("int")
        df_size.to_csv("trajs/" + plane_class + "/" + mark + "/" + plane_class + "_" + mark + "_num_connections.csv", index = False)