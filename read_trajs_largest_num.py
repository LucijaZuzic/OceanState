import pandas as pd
import matplotlib.pyplot as plt
import os
 
plane_classes = os.listdir("trajs")
marks = ["train", "test", "valid"]
 
num_conns = dict()
num_from = dict()
num_to = dict()

for plane_class in plane_classes:

    if plane_class == "conns":
        continue
    
    for mark in marks:

        if not os.path.isfile("trajs/" + plane_class + "/conns/" + plane_class + "_" + mark + "_num_conns.csv"):
            continue
  
        pd_file = pd.read_csv("trajs/" + plane_class + "/conns/" + plane_class + "_" + mark + "_num_conns.csv", index_col = False)
          
        for ix in range(len(pd_file["fromICAO"])):

            orig = pd_file["fromICAO"][ix]
            desti = pd_file["toICAO"][ix]
  
            str_name = str(orig) + "_" + str(desti)
            
            if str_name not in num_conns:
                num_conns[str_name] = 0
            num_conns[str_name] += pd_file["num"][ix]

            if orig not in num_from:
                num_from[orig] = 0
            num_from[orig] += pd_file["num"][ix]

            if desti not in num_to:
                num_to[desti] = 0
            num_to[desti] += pd_file["num"][ix]
 
for con in dict(sorted(num_conns.items(), key=lambda item: item[1], reverse = True)):
    print(con, num_conns[con])
    max_con = con
    break
 
for orig in dict(sorted(num_from.items(), key=lambda item: item[1], reverse = True)):
    print(orig, num_from[orig])
    break
 
for desti in dict(sorted(num_to.items(), key=lambda item: item[1], reverse = True)):
    print(desti, num_to[desti])
    break

print("LDZA_EGLL", num_conns["LDZA_EGLL"])
print("EGLL_LDZA", num_conns["EGLL_LDZA"])
print("LDZA", num_from["LDZA"], num_to["LDZA"])
print("EGLL", num_from["EGLL"], num_to["EGLL"])