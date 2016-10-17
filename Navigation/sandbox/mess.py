# import xml.etree.ElementTree as ET
#  
#  
# info = ET.parse("sightings.xml")
# sightings = info.getroot() 
# num = len(sightings)
# # for child in sightings:
#     print child.tag 
   
# bodys = info.getiterator("body")
# dates = info.getiterator("date")
# times = info.getiterator("time")
# observations = info.getiterator("observation")
# heights = info.getiterator("height")
# temperatures = info.getiterator("temperature")
# pressures = info.getiterator("pressure")
# horizons = info.getiterator("horizon")       
         
# while(i < num):
#     sightings[i] = bodys[i].text,dates[i].text,times[i].text,observations[i].text,heights[i].text,temperatures[i].text,pressures[i].text,horizons[i].text
#     if 

    
# 
# if (bodys[0] < bodys[1]):
#     print 1,bodys[0].text,bodys[1].text
# else:
#     print 2,bodys[0].text,bodys[1].text
# 
# if (times[0] > times[1]):
#     print 1
# else:
#     print 2
#     
# if (dates[0] > dates[1]):
#     print 1
# else:
#     print 2
#     
# for i in range(len(bodys)):
#     print i 
    
# n = len(bodys)
# print n
# print "tag:",bodys[0].tag
# print "text",bodys[0].text
# print "tag:",bodys[1].tag
# print "text",bodys[1].text
# 
# print len(sightings)


# filename = "abc.xml"
# tagStart = str(filename).find('.xml')
# print tagStart
# print len(filename)
# print len(".xml")
# print len(filename)-len(".xml") 
# import datetime

# f = open("log.txt",'w')
# time = datetime.datetime.now().replace(microsecond=0).isoformat(' ')
# startLog = ["LOG:\t",time,"\tStart of log\n"]
# f.writelines(startLog)
# f.close()

