import datetime
import json
# import pandas as pd
import requests
from datetime import timedelta,datetime
import re
import csv

def room_generate():
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term="

    # getting the term for url
    date = datetime.now()
    season = "2"
    if (date.month <= 12 and date.month >= 7):
        season = "8"
    term = "1" + str(date.year)[2:] + season


    # aggregating all valid page numbers to one object that has all json for current term classes
    index = 1
    request = requests.get(url + term + "&page=" + str(index))
    json_data = request.json()
    #room_df = []
    with open('class_res.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        fields = ["Days", "Start_time", "End_time", "Start_date", "End_date", "Building", "Room"]
        writer.writerow(fields)
        while True:
            if not json_data:
                # print(index)
                break
        # making data frame of classes
            for c in json_data:
                if len(c['meetings'])>0:
                    room = re.split('(\d+)', str(c['meetings'][0]['facility_descr']))
                    start_time = c['meetings'][0]['start_time'][0:5]
                    end_time = c['meetings'][0]['end_time'][0:5]
                    start_date = c['meetings'][0]['start_dt']
                    end_date = c['meetings'][0]['end_dt']
                    if len(end_time)>1:
                        end = int(end_time[3:])
                        diff = 0
                        if end != 30 or end != 00:
                            if end < 30:
                                diff = 30 - end
                            else:
                                diff = 60 - end
                        time_object = datetime.strptime(end_time[0:5], '%H.%M')
                        minutes_add = timedelta(minutes=diff)
                        end_time = (time_object + minutes_add).time()
                    if len(room) > 1:
                        room_name = room[0]
                        room_num = room[1]
                        arr = []
                        if "Mo" in c['meetings'][0]['days']:
                            writer.writerow(["Monday", start_time, end_time,
                                            start_date, end_date, room_name.strip(),
                                            int(room_num)
                                            ])
                        if "Tu" in c['meetings'][0]['days']:
                            writer.writerow(["Tuesday", start_time, end_time,
                                            start_date, end_date, room_name.strip(),
                                            int(room_num)
                                            ])
                        if "We" in c['meetings'][0]['days']:
                            writer.writerow(["Wednesday", start_time, end_time,
                                            start_date, end_date, room_name.strip(),
                                            int(room_num)
                                            ])
                        if "Th" in c['meetings'][0]['days']:
                            writer.writerow(["Thursday", start_time, end_time,
                                            start_date, end_date, room_name.strip(),
                                            int(room_num)
                                            ])
                        if "Fr" in c['meetings'][0]['days']:
                            writer.writerow(["Friday", start_time, end_time,
                                            start_date, end_date, room_name.strip(),
                                            int(room_num)
                                            ])
            index += 1
            request = requests.get(url + term + "&page=" + str(index))
            json_data = request.json()

    file.close()
    #room_df = pd.DataFrame(room_df)
    #room_df.columns = ["Days", "Start_time", "End_time", "Start_date", "End_date", "Building", "Room"]
    #room_df = room_df.sort_values(by=["Building", "Start_time"])
    #return

room_generate()