lines = []
match = []
matched = []
with open("starFile.txt",'r') as starfile:
    for line in starfile:
        lines.append(line.strip('\n'))
starfile.close()
for line in lines:   
    if line.find('Alpheratz') != -1 :
        match.append(line.split('\t'))
for i in range(1,len(match)):
    times = match[i-1][1]
    timesmax = match[i][1]
    date = '01/11/17'
    if timesmax > date and times <= date:
        matched = match[i-1]
        print matched
latitude = matched[3]
print latitude    
#     else:
#         self.count += 1
date = '01/11/17'
date_1 = '01/12/17'
time = '23:50:50'
arieslines = []
datematch = []
aries1 = []
aries2 = []
with open("ariesFile.txt") as ariesfile:
    for line in ariesfile:
        arieslines.append(line.strip('\n'))
ariesfile.close()
for line in arieslines:   
    if line.find(date) != -1 or line.find(date_1) != -1:
        datematch.append(line.split('\t'))
print datematch     
for i in range(1,len(datematch)):
    timeStar = datematch[i-1][1]
    if time[0:2] == timeStar:
        aries1 = datematch[i-1]
        aries2 = datematch[i] 
print aries1
print aries2
        
#         aries2 = datematch[i]
# print time[0:2]
# print aries1[1],aries2 # verify



