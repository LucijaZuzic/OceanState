import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

num_conns = dict()
start_pos_conns = dict()
end_pos_conns = dict()

for filename in os.listdir("flights"):
    if "flightlist_20220801_20220831" not in filename:
        continue
    pd_file = pd.read_csv("flights/" + filename, index_col = False)

    for ix in range(len(pd_file["origin"])):
        orig = pd_file["origin"][ix]
        desti = pd_file["destination"][ix]

        lat1 = pd_file["latitude_1"][ix]
        long1 = pd_file["longitude_1"][ix]
        alt1 = pd_file["altitude_1"][ix]

        lat2 = pd_file["latitude_2"][ix]
        long2 = pd_file["longitude_2"][ix]
        alt2 = pd_file["altitude_2"][ix]

        str_name = str(orig) + " " + str(desti)

        if orig == desti or str(orig) == "nan" or str(desti) == "nan":
            continue

        if str(lat1) == "nan" or str(lat2) == "nan":
            continue

        if str(long1) == "nan" or str(long2) == "nan":
            continue

        if str(alt1) == "nan" or str(alt2) == "nan":
            continue

        if str_name not in num_conns:
            num_conns[str_name] = 0
        num_conns[str_name] += 1

        if str_name not in start_pos_conns:
            start_pos_conns[str_name] = []
        start_pos_conns[str_name].append((long1, lat1, alt1))
        
        if str_name not in end_pos_conns:
            end_pos_conns[str_name] = []
        end_pos_conns[str_name].append((long2, lat2, alt2))
        
    for con in dict(sorted(num_conns.items(), key=lambda item: item[1], reverse = True)):
        print(con, num_conns[con])
        break

    longs1 = []
    lats1 = []

    longs2 = []
    lats2 = []

    longs3 = []
    lats3 = []

    longs4 = []
    lats4 = []

    for coords in start_pos_conns["RJTT RJFF"]:
        long1, lat1, alt1 = coords
        longs1.append(long1)
        lats1.append(lat1)

    for coords in start_pos_conns["RJFF RJTT"]:
        long3, lat3, alt3 = coords
        longs3.append(long3)
        lats3.append(lat3)

    for coords in end_pos_conns["RJFF RJTT"]:
        long2, lat2, alt2 = coords
        longs2.append(long2)
        lats2.append(lat2)

    for coords in end_pos_conns["RJTT RJFF"]:
        long4, lat4, alt4 = coords
        longs4.append(long4)
        lats4.append(lat4)

    plt.scatter(longs1, lats1) 
    plt.scatter(longs2, lats2)
    plt.show()
    plt.close()
    plt.scatter(longs3, lats3) 
    plt.scatter(longs4, lats4)
    plt.show()
    plt.close()