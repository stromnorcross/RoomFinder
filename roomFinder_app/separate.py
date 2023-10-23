import datetime
import json
import pandas as pd
import requests
import re

url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term="

# getting the term for url
date = datetime.datetime.now()
season = "2"
if (date.month <= 12 and date.month >= 7):
    season = "8"
term = "1" + str(date.year)[2:] + season


# aggregating all valid page numbers to one object that has all json for current term classes
index = 1
request = requests.get(url + term + "&page=" + str(index))
json_data = request.json()

while True:
    index+=1
    request2 = requests.get(url + term + "&page=" + str(index))
    json_data2 = request2.json()
    if not json_data2:
        print(index)
        break
    json_data += json_data2

# making data frame of classes
room_df = []
# for loop not working with aggregated json will take look again later
for c in json_data:
    room = re.split('(\d+)', str(c['meetings'][0]['facility_descr']))
    if len(room) > 1:
        room_name = room[0]
        room_num = room[1]
        arr = []
        if "Mo" in c['meetings'][0]['days']:
            arr.append(1)
        if "Tu" in c['meetings'][0]['days']:
            arr.append(2)
        if "We" in c['meetings'][0]['days']:
            arr.append(3)
        if "Th" in c['meetings'][0]['days']:
            arr.append(4)
        if "Fr" in c['meetings'][0]['days']:
            arr.append(5)
        room_df.append([arr, c['meetings'][0]['start_time'][0:8], c['meetings'][0]['end_time'][0:8],
                        c['meetings'][0]['start_dt'], c['meetings'][0]['end_dt'], room_name.strip(), int(room_num)
                        ])


room_df = pd.DataFrame(room_df)
room_df.columns = ["Days", "Start_time", "End_time", "Start_date", "End_date", "Building", "Room"]

room_df = room_df.sort_values(by=["Building", "Start_time"])
print(room_df)

# prev_row = room_df.iloc[0]
# result_df = []
# for row in room_df:
# 	if row["Building"]==prev_row["Building"] and row["Room"]==prev_row["Room"]:
# 		for day in row["Days"]:
# 			# if day in prev_row["Days"]:


# print(prev_row)
# print(room_df["Start_time"][0])
# print(room_df["Start_time"][10]<room_df["Start_time"][0])
