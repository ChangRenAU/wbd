# num = [1,4,6,2,1,3,7,5]
# n=len(num)
# for i in range(0,n):         
#     for j in range(i,n):
#         if num[i] >= num[j]:
#             num[i],num[j] = num[j],num[i]
#         else:
#             num[i],num[j] = num[i],num[j]
# print num

import xml.etree.ElementTree as ET

info = ET.parse("sightings.xml")
sightings = info.getroot()
num = len(sightings)
bodies = info.getiterator("body")
dates = info.getiterator("date")
times = info.getiterator("time")
observations = info.getiterator("observation")
heights = info.getiterator("height")
temperatures = info.getiterator("temperature")
pressures = info.getiterator("pressure")
horizons = info.getiterator("horizon")
#         sightings[i] = bodies[i],dates[i],times[i],observations[i],heights[i],temperatures[i],pressures[i],horizons[i]
for i in range(0,num):
    sightings[i] = bodies[i].text,dates[i].text,times[i].text,observations[i].text,heights[i].text,temperatures[i].text,pressures[i].text,horizons[i].text

for i in range(0,num):
    for j in range(i+1,num):
        if dates[i].text > dates[j].text:
            sightings[i],sightings[j] = sightings[j],sightings[i]
        elif dates[i].text == dates[j].text and times[i].text > times[j].text:
            sightings[i],sightings[j] = sightings[j],sightings[i]  
        elif dates[i].text == dates[j].text and times[i].text == times[j].text and bodies[i].text > bodies[j].text:
            sightings[i],sightings[j] = sightings[j],sightings[i]
#         else:
#             sightings[i],sightings[j] = sightings[i],sightings[j]
for i in range(0,num):
    print sightings[i]