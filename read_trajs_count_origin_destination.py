import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
 
def add_to_df(nc, from_a, to_a, some_df):

    if len(some_df[(some_df["fromICAO"] == from_a) & (some_df["toICAO"] == to_a)]):
        some_df["num"] = np.where((some_df["fromICAO"] == from_a) & (some_df["toICAO"] == to_a), some_df["num"] + nc, some_df["num"])
    else:    
        some_data = {"fromICAO": [], "toICAO": [], "num": []} 
        some_data["fromICAO"].append(from_a)
        some_data["toICAO"].append(to_a)
        some_data["num"].append(nc)
        some_df = pd.concat([some_df, pd.DataFrame(some_data)])

    return some_df

plane_classes = sorted(os.listdir("trajs"), reverse = True)
marks = ["valid", "test", "train"]

df_all = pd.DataFrame({"fromICAO": [], "toICAO": [], "num": []})
df_val = pd.DataFrame({"fromICAO": [], "toICAO": [], "num": []})
df_train = pd.DataFrame({"fromICAO": [], "toICAO": [], "num": []})
df_test = pd.DataFrame({"fromICAO": [], "toICAO": [], "num": []})

chunksize = 1000

for plane_class in plane_classes:

    if plane_class == "conns":
        continue

    pd_file_from = pd.read_csv("trajs/" + plane_class + "/test_fromICAO_" + plane_class + ".csv", index_col = False, header = None)
    pd_file_to = pd.read_csv("trajs/" + plane_class + "/test_toICAO_" + plane_class + ".csv", index_col = False, header = None)
     
    dict_from = {str(pd_file_from[0][i]): int(pd_file_from[1][i]) for i in range(len(pd_file_from[0]))}
    dict_to = {str(pd_file_to[0][i]): int(pd_file_to[1][i]) for i in range(len(pd_file_to[0]))}
 
    df_class = pd.DataFrame({"fromICAO": [], "toICAO": [], "num": []})

    for mark in marks:

        if not os.path.isfile("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv"):
            continue

        counted = False
        if os.path.isfile("trajs/" + plane_class + "/" + plane_class + "_" + mark + "_num_conns.csv"):
            counted = True
  
        counter_dataframe = pd.DataFrame({"fromICAO": [], "toICAO": [], "num": []})

        print(plane_class, mark)

        if counted:

            pd_file_num = pd.read_csv("trajs/" + plane_class + "/" + plane_class + "_" + mark + "_num_conns.csv", index_col = False)
            pd_file_num = pd_file_num.sort_values(by = ["fromICAO", "toICAO"])
            print("Counted", sum(list(pd_file_num["num"])))
 
            for df in dict_from:

                counter_df_part1 = pd_file_num[pd_file_num["fromICAO"] == df] 

                for dt in dict_to: 
                        
                    counter_df = counter_df_part1[counter_df_part1["toICAO"] == dt]
                    if len(counter_df):
                        num_counter = list(counter_df["num"])[0]
                    else:
                        num_counter = 0
                    
                    if num_counter != 0:
                        df_all = add_to_df(num_counter, df, dt, df_all)

                        if mark == "valid":
                            df_val = add_to_df(num_counter, df, dt, df_val)
                        
                        if mark == "train":
                            df_train = add_to_df(num_counter, df, dt, df_train)
                        
                        if mark == "test":
                            df_test = add_to_df(num_counter, df, dt, df_test)
                        
                        counter_dataframe = add_to_df(num_counter, df, dt, counter_dataframe)
                        df_class = add_to_df(num_counter, df, dt, df_class)

        else:

            len_chunks = 0

            for pd_file in pd.read_csv("trajs/" + plane_class + "/" + plane_class + "_" + mark + ".csv", index_col = False, chunksize = chunksize):        
                
                len_chunks += len(pd_file)

                for df in dict_from:
 
                    counter_df_part1 = pd_file[pd_file["fromICAO"] == dict_from[df]]

                    for dt in dict_to: 
                            
                        counter_df = counter_df_part1[counter_df_part1["toICAO"] == dict_to[dt]]
                        num_counter = len(counter_df)
                            
                        if num_counter != 0:
                            df_all = add_to_df(num_counter, df, dt, df_all)
                            
                            if mark == "valid":
                                df_val = add_to_df(num_counter, df, dt, df_val)
                            
                            if mark == "train":
                                df_train = add_to_df(num_counter, df, dt, df_train)
                            
                            if mark == "test":
                                df_test = add_to_df(num_counter, df, dt, df_test)

                            counter_dataframe = add_to_df(num_counter, df, dt, counter_dataframe)
                            df_class = add_to_df(num_counter, df, dt, df_class)

            print("Not counted", len_chunks)
 
        counter_dataframe["num"] = counter_dataframe["num"].astype("int")
        counter_dataframe = counter_dataframe.sort_values(by = ["fromICAO", "toICAO"])
        print(len(counter_dataframe))
        counter_dataframe.to_csv("trajs/" + plane_class + "/" + plane_class + "_" + mark + "_num_conns.csv", index = False)
 
    df_class["num"] = df_class["num"].astype("int")
    df_class = df_class.sort_values(by = ["fromICAO", "toICAO"])
    print(len(df_class))
    df_class.to_csv("trajs/" + plane_class + "/" + plane_class + "_num_conns.csv", index = False)

df_all["num"] = df_all["num"].astype("int")
df_all = df_all.sort_values(by = ["fromICAO", "toICAO"])
print(len(df_all))
df_all.to_csv("trajs/num_conns.csv", index = False)

df_val["num"] = df_val["num"].astype("int")
df_val = df_val.sort_values(by = ["fromICAO", "toICAO"])
print(len(df_val))
df_val.to_csv("trajs/num_conns_val.csv", index = False)

df_train["num"] = df_train["num"].astype("int")
df_train = df_train.sort_values(by = ["fromICAO", "toICAO"])
print(len(df_train))
df_train.to_csv("trajs/num_conns_train.csv", index = False)

df_test["num"] = df_test["num"].astype("int")
df_test = df_test.sort_values(by = ["fromICAO", "toICAO"])
print(len(df_test))
df_test.to_csv("trajs/num_conns_test.csv", index = False)