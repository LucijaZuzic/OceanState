import opensky_api
from datetime import datetime, timedelta
dt = datetime(day = 12, month = 1, year = 2016)
dt_end = datetime(day = 30, month = 12, year = 2023)
epoch_time = datetime(1970, 1, 1)

while dt < dt_end:
    start_sec = int((dt - epoch_time).total_seconds())
    end_sec = start_sec + 3600 * 24 * 7
    opensky = opensky_api.OpenSkyApi("lzuzic", "uGJp64kA")
    data_res = opensky.get_departures_by_airport("LDZA", start_sec, end_sec)
    print(data_res)
    for e in data_res:  
        dict_e = eval(str(e)) 
        print(dict_e["estArrivalAirport"])
        print(dict_e)
        #data_track = opensky.get_track_by_aircraft(dict_e["icao24"], start_sec)
        #print(data_track)
    dt = dt + timedelta(days = 7)
    print(dt)
    break