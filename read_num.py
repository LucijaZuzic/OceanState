import os
import pandas as pd

plane_classes = os.listdir("trajs")
marks = ["valid", "test", "train"] 

df_all = pd.DataFrame()

for plane_class in plane_classes: 

    for mark in marks:

        if not os.path.isfile("trajs/" + plane_class + "/" + mark + "/" + plane_class + "_" + mark + "_num_connections.csv"):
            continue
        print(plane_class, mark)
        pd_df = pd.read_csv("trajs/" + plane_class + "/" + mark + "/" + plane_class + "_" + mark + "_num_connections.csv", index_col = False)
        df_all = pd.concat([df_all, pd_df])

all_destinations = set(df_all["toICAO"])
all_sources = set(df_all["fromICAO"])

print(len(all_sources))
print(len(all_destinations))

dict_src_dest = dict()
dict_dest = dict()
dict_src = dict()

maxi_src = 0
maxi_src_val = "LDZA"
maxi_src_dest = 0
maxi_src_dest_val = "LDZA_EGLL"

for src in all_sources:

    dict_src_dest[src] = dict()

    df_new_src = df_all[df_all["fromICAO"] == src]
    dict_src[src] = sum(df_new_src["num"])

    if dict_src[src] > maxi_src:
        maxi_src = dict_src[src]
        maxi_src_val = src 
        print("from", maxi_src, maxi_src_val)

    for dest in all_destinations:

        if src == dest:
            continue

        df_new_src_dest = df_new_src[df_new_src["toICAO"] == dest]
        dict_src_dest[src][dest] = sum(df_new_src_dest["num"])

        if dict_src_dest[src][dest] > maxi_src_dest:
            maxi_src_dest = dict_src_dest[src][dest]
            maxi_src_dest_val = src + "_" + dest
            print("from-to", maxi_src_dest, maxi_src_dest_val)
  
print("from", maxi_src, maxi_src_val)
print("from-to", maxi_src_dest, maxi_src_dest_val)

maxi_dest = 0
maxi_dest_val = "LDZA"

for dest in all_destinations:

    df_new_dest = df_all[df_all["toICAO"] == dest]
    dict_dest[dest] = sum(df_new_dest["num"])

    if dict_dest[dest] > maxi_dest:
        maxi_dest = dict_dest[dest]
        maxi_dest_val = dest 
        print("to", maxi_dest, maxi_dest_val)

print("to", maxi_dest, maxi_dest_val)