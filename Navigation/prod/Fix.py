import datetime
import time
import math
import os
import Angle
import xml.etree.ElementTree as ET

class Fix():

    def __init__(self,logFile = "log.txt"):
        self.className = "Fix."
        methodName = "__init__:  "
        self.logFile = logFile
        self.openlogFile = None
        self.sightingFile = None
        self.ariesFile = None
        self.starFile = None
        self.sightingList = []
        self.count = 0
        self.star = None
        self.shastar = None
        self.aries1 = None
        self.aries2 = None
        self.approximateLatitude = "0d0"           
        self.approximateLongitude = "0d0"
        
        if(not(isinstance(self.logFile,str))):
            raise ValueError(self.className + methodName + "invalid filename")
        if len(self.logFile) < 1:
            raise ValueError(self.className + methodName + "invalid filename")
        try:
            if not os.path.isfile(self.logFile):
                self.openlogFile = open(self.logFile,'w+')    
            else: 
                self.openlogFile = open(self.logFile,'a+')
        except:
            raise ValueError(self.className + methodName + "log file cannot be created or appended") 

        logFilePath = os.path.abspath(self.logFile)  
        logofLogFile = ["LOG:\t",self.getTime(),"\tLog file:\t",logFilePath,"\n"]
        self.openlogFile.writelines(logofLogFile)
        self.openlogFile.close()
        
    def setSightingFile(self,sightingFile = None):
        methodName = "setSightingFile:  "
        self.sightingFile = sightingFile
        if(not(isinstance(self.sightingFile,str))):
            raise ValueError(self.className + methodName + "invalid filename")
        tag = self.sightingFile.find(".xml")
        n = len(self.sightingFile)-len(".xml")
        if (tag != n ) | (n < 1):
            raise ValueError(self.className + methodName + "invalid filename")
        try:
            f = open(self.sightingFile,'r')
            f.close()
        except:
            raise ValueError(self.className + methodName + "cannot open sighting file")
        
        info = self.getTree(self.sightingFile,methodName)         
        self.count = self.checkSightingFile(info,methodName)           

        sightingFilePath = os.path.abspath(self.sightingFile) 
        self.openlogFile = open(self.logFile,'a+')
        logofSightingFile = ["LOG:\t",self.getTime(),"\tSighting file:\t",sightingFilePath,"\n"]
        self.openlogFile.writelines(logofSightingFile)
        self.openlogFile.close()
          
        return sightingFilePath
    
    def setAriesFile(self,ariesFile):
        methodName = "setAriesFile:  "
        self.ariesFile = ariesFile
        if(not(isinstance(self.ariesFile,str))):
            raise ValueError(self.className + methodName + "invalid filename")
        tag = self.ariesFile.find(".txt")
        n = len(self.ariesFile)-len(".txt")
        if (tag != n ) | (n < 1):
            raise ValueError(self.className + methodName + "invalid filename")
        try:
            f = open(self.ariesFile,'r')
            f.close()
        except:
            raise ValueError(self.className + methodName + "cannot open aries file")
                    
        ariesFilePath = os.path.abspath(self.ariesFile) 
        self.openlogFile = open(self.logFile,'a+')
        logofAriesFile = ["LOG:\t",self.getTime(),"\tAries file:\t",ariesFilePath,"\n"]
        self.openlogFile.writelines(logofAriesFile)
        self.openlogFile.close()
          
        return ariesFilePath
    
    def setStarFile(self,starFile):
        methodName = "setStarFile:  "
        self.starFile = starFile
        if(not(isinstance(self.starFile,str))):
            raise ValueError(self.className + methodName + "invalid filename")
        tag = self.starFile.find(".txt")
        n = len(self.starFile)-len(".txt")
        if (tag != n ) | (n < 1):
            raise ValueError(self.className + methodName + "invalid filename")
        try:
            f = open(self.starFile,'r')
            f.close()
        except:
            raise ValueError(self.className + methodName + "cannot open star file")            
        
        starFilePath = os.path.abspath(self.starFile) 
        self.openlogFile = open(self.logFile,'a+')
        logofStarFile = ["LOG:\t",self.getTime(),"\tStar file:\t",starFilePath,"\n"]
        self.openlogFile.writelines(logofStarFile)
        self.openlogFile.close()
          
        return starFilePath

    def getSightings(self,assumedLatitude = "0d0.0", assumedLongitude = "0d0.0" ):
        methodName = "getSightings:  "        
        sumCosSighting = 0.0
        sumSinSighting = 0.0 
        if self.sightingFile == None:
            raise ValueError(self.className + methodName + "no sighting file has been set")
        if self.ariesFile == None:
            raise ValueError(self.className + methodName + "no aries file has been set")
        if self.starFile == None:
            raise ValueError(self.className + methodName + "no star file has been set")
            
        sightings = self.sightingList
        sightings = sorted(sightings, key = lambda element: (element[1], element[2], element[0]))
        
        assumedLatitudeAngle = self.setAssumedLatitude(assumedLatitude)
        assumedLongitudeAngle = self.setAssumedLongitude(assumedLongitude)
        if assumedLatitudeAngle == 0:
            raise ValueError(self.className + methodName +"invalid assumedLatitude" )
        if assumedLongitudeAngle == 0:
            raise ValueError(self.className + methodName +"invalid assumedLongitude") 
                    
        anAngle = Angle.Angle()
        for i in range(0,len(sightings)):   
            observedAltitude = anAngle.setDegreesAndMinutes(sightings[i][3])
            adjustedAltitudeDegree = self.calculateAdjustedAltitude(sightings[i][4],sightings[i][5],sightings[i][6],sightings[i][7],observedAltitude)
            anAngle.setDegrees(adjustedAltitudeDegree)
            adjustedAltitude = anAngle.getString()
            latitude,longitudeDegree = self.getGeographicPosition(sightings[i][0],sightings[i][1],sightings[i][2])
            
            anAngle.setDegrees(longitudeDegree)
            longitude = anAngle.getString()
            anAngle.setDegreesAndMinutes(latitude)
            latitudeDegree = anAngle.getDegrees()
            
            azimuthTemp,distanceAdjustment = self.getAdjustments(longitudeDegree,latitudeDegree,assumedLongitudeAngle,assumedLatitudeAngle,adjustedAltitudeDegree)
            anAngle.setDegrees(azimuthTemp)
            azimuthAdjustment = anAngle.getString()
            
            self.openlogFile = open(self.logFile,'a+')
            logofSighting = ["LOG:\t",self.getTime(),"\t",sightings[i][0],"\t",sightings[i][1],"\t",sightings[i][2],"\t",adjustedAltitude,"\t",latitude,"\t",longitude,"\t",assumedLongitude,"\t",assumedLatitude,"\t",azimuthAdjustment,"\t",str(distanceAdjustment),"\n"]
            self.openlogFile.writelines(logofSighting)
            self.openlogFile.close() 
            
            sumCosSighting += distanceAdjustment * math.cos(azimuthTemp)
            sumSinSighting += distanceAdjustment * math.sin(azimuthTemp)  
        
        approximateLatitude = assumedLatitudeAngle.getDegrees() + sumCosSighting / 60.0            
        approximateLongitude = assumedLongitudeAngle.getDegrees() + sumSinSighting / 60.0         
        if approximateLatitude >= 270 and approximateLatitude <= 360:
            self.approximateLatitude = approximateLatitude - 360            
        if approximateLatitude > 90 and approximateLatitude < 270:    
            self.approximateLatitude = 180 - approximateLatitude                  
        approximateLatitudeString = str(int(self.approximateLatitude))+"d"+ str(abs(round((self.approximateLatitude-int(self.approximateLatitude))*60,1)))        
        if self.approximateLatitude < 0:
            approximateLatitudeString = approximateLatitudeString.replace("-","S")
        else:
            approximateLatitudeString = "N" + approximateLatitudeString
        
        approximateLongitudeAngle = Angle.Angle()
        approximateLongitudeAngle.setDegrees(approximateLongitude)
        self.approximateLongitude = approximateLongitudeAngle.getString()
        
        self.openlogFile = open(self.logFile,'a+')
        sightingErrors = ["LOG:\t",self.getTime(),"\tSighting errors:\t",str(self.count),"\n"]
        approximatePosition = ["LOG:\t",self.getTime(),"Approximate latitude\t:",approximateLatitudeString,"Approximate longitude\t:",self.approximateLongitude,"\n"]
        self.openlogFile.writelines(sightingErrors)
        self.openlogFile.writelines(approximatePosition)
        self.openlogFile.close() 
          
        return (approximateLatitudeString, self.approximateLongitude) 
    
    def getTree(self,sightingfilename,methodName):
        if sightingfilename == None:
            raise ValueError(self.className + methodName + "no sighting file has been set")
        else:
            try:
                tree = ET.parse(sightingfilename)
            except:
                raise ValueError(self.className + methodName + "no such sighting file")
        return tree
 
    def calculateAdjustedAltitude(self, height, temperature, pressure, horizon, observedAltitude):
        if (horizon == "Natural"):
            dip = (-0.97 * math.sqrt(height)) / 60.0
        else:
            dip = 0.0    
         
        refraction = (-0.00452 * float(pressure)) / (273 + ((float(temperature) - 32.0 ) / 1.8 ))/ math.tan(math.radians(observedAltitude))
        result = observedAltitude + dip + refraction

        return result 

    def getTime(self):    
        timenow = datetime.datetime.utcnow().replace(microsecond=0).isoformat(' ') 
        timezone = "-06:00"
        time = timenow + timezone
        return time 
    
    def checkSightingFile(self,info,methodName):
        count = 0 
        for child in info.findall("sighting"):
            tagofbody = child.find("body")
            if tagofbody == None:
                #raise ValueError(self.className + methodName + "missing tag of body")
                count = count + 1
                continue
            else:
                body = tagofbody.text
                if body == None:
                    #raise ValueError(self.className + methodName + "missing content of body")
                    count = count + 1    
            tagofdate = child.find("date")    
            if tagofdate == None:
                #raise ValueError(self.className + methodName + "missing tag of date")
                count = count + 1
                continue
            else:
                date = tagofdate.text
                try:
                    time.strptime(date,"%Y-%m-%d")  
                except:  
                    #raise ValueError(self.className + methodName + "wrong format of date")   
                    count = count + 1
                    continue 
            tagoftime = child.find("time")
            if tagoftime == None:
                #raise ValueError(self.className + methodName + "missing tag of time")
                count = count + 1
                continue            
            else:
                observedtime = tagoftime.text
                try:
                    time.strptime(observedtime, "%H:%M:%S")
                except:
                    #raise ValueError(self.className + methodName + "wrong format of time")
                    count = count + 1
                    continue                
            tagofob = child.find("observation")
            if tagofob == None:
                #raise ValueError(self.className + methodName + "missing tag of observation")
                count = count + 1
                continue
            
            else:
                observation = tagofob.text
                if observation == None:
                    #raise ValueError(self.className + methodName + "missing content of observation")
                    count = count + 1
                    continue
                nums = str(observation).split('d')
                start, end = map(float,nums)
                if (start >= 90 or start < 0 or end < 0 or end >= 60 or (start == 0.0 and end < 0.1)):
                    #raise ValueError(self.className + methodName + "invalid observation")
                    count = count + 1
                    continue                    
            tagofheight = child.find("height")    
            if tagofheight == None:
                height = 0
            else:
                height = tagofheight.text
                if height == None:
                    height = 0
                try:
                    height = float(height)
                except:    
                    #raise ValueError(self.className + methodName + "invalid height")   
                    count = count + 1
                    continue
                if height < 0:
                    #raise ValueError(self.className + methodName + "invalid height")
                    count = count + 1
                    continue
            tagoftemperature = child.find("temperature")
            if tagoftemperature == None:
                temperature = 72 
            else:
                temperature = tagoftemperature.text
                if temperature == None:
                    temperature = 72
                try:
                    temperature = float(temperature)
                except:    
                    #raise ValueError(self.className + methodName + "invalid temperature")  
                    count = count + 1
                    continue                
                if temperature < -20 or temperature > 120:
                    #raise ValueError(self.className + methodName + "invalid temperature")
                    count = count + 1
                    continue                
            tagofpressure = child.find("pressure")
            if tagofpressure == None:
                pressure = 1010 
            else:
                pressure = tagofpressure.text  
                if pressure == None:
                    pressure = 1010
                try:
                    pressure = float(pressure)
                except:    
                    #raise ValueError(self.className + methodName + "invalid pressure")  
                    count = count + 1
                    continue                
                if pressure < 100 or pressure > 1100:
                    #raise ValueError(self.className + methodName + "invalid pressure")
                    count = count + 1
                    continue            
            tagofhorizon = child.find("horizon")
            if tagofhorizon == None:
                horizon = 'Natural' 
            else:
                horizon = tagofhorizon.text 
                if horizon == None:
                    horizon = 'Natural'
                elif horizon not in ['Natural','Artificial']:
                    #raise ValueError(self.className + methodName + "invalid horizon")
                    count = count + 1
                    continue
            sightings = (body,date,observedtime,observation,height,temperature,pressure,horizon)
            self.sightingList.append(sightings)
          
        return count 
    
    def getGeographicPosition(self,body,date,Stime):
        anAngle = Angle.Angle()
        tempdate = datetime.datetime.strptime(date, '%Y-%m-%d')
        date = '{0:02}/{1}/{2}'.format(tempdate.month, tempdate.day, tempdate.year % 100)
        date_1 = '{0:02}/{1}/{2}'.format(tempdate.month, tempdate.day+1, tempdate.year % 100)
        lines = []
        arieslines = []
        bodymatch = []
        datematch = []
        with open(self.starFile,'r') as starfile:
            for line in starfile:
                lines.append(line.strip('\n'))
        starfile.close()
        for line in lines:   
            if line.find(body) != -1 :
                bodymatch.append(line.split('\t'))

        for i in range(1,len(bodymatch)):
            datemin = bodymatch[i-1][1]
            datemax = bodymatch[i][1]
            if date >= datemin and date < datemax:
                star = bodymatch[i-1]
                self.star = star[3]
                self.shastar = star[2]
        latitude = self.star
        SHAstar = anAngle.setDegreesAndMinutes(self.shastar)
               
        with open(self.ariesFile,'r') as ariesfile:
            for line in ariesfile:
                arieslines.append(line.strip('\n'))
        ariesfile.close()
        for line in arieslines: 
            if line.find(date) != -1 or line.find(date_1) != -1:
                datematch.append(line.split('\t'))      
                          
        for i in range(1,len(datematch)):
            timeStar = datematch[i-1][1]
            if Stime[0:2] == timeStar:
                aries1 = datematch[i-1]
                aries2 = datematch[i]
                self.aries1 = aries1[2]
                self.aries2 = aries2[2] 
        GHAaries1 = anAngle.setDegreesAndMinutes(self.aries1)
        GHAaries2 = anAngle.setDegreesAndMinutes(self.aries2) 
        s = self.getSeconds(Stime) 
        result = GHAaries1 + abs(GHAaries1 - GHAaries2) * (s/3600.0) + SHAstar        
       
        return latitude,result
    
    def getSeconds(self,Stime):
        h, m, s = Stime.split(':')
        return int(h) * 0 +int(m) * 60 + int(s)
    
    def setAssumedLatitude(self,assumedLatitude):
        if"-" in assumedLatitude:
            assumedLatitude = 0        
        if("N" not in assumedLatitude) and ("S" not in assumedLatitude):
            if assumedLatitude != "0d0.0":
                assumedLatitude = 0       
        if "N" in assumedLatitude:
            assumedLatitude = assumedLatitude.replace("N","")
        if "S" in assumedLatitude:
            assumedLatitude = assumedLatitude.replace("S","-")            
        if"0d0.0"in assumedLatitude:
            if"N" in assumedLatitude or "S" in assumedLatitude:
                assumedLatitude = 0
        assumedLatitudeAngle = Angle.Angle()        
        try:
            assumedLatitudeAngle.setDegreesAndMinutes(assumedLatitude)
        except:
            assumedLatitude = 0
        assumedLatitudeArray = assumedLatitude.split("d")
        if float(assumedLatitudeArray[0] >= 90 or float(assumedLatitudeArray[0]) <= -90):
            assumedLatitude = 0
    
        return assumedLatitudeAngle.getDegrees()
    
    def setAssumedLongitude(self,assumedLongitude):
        assumedLongitudeAngle = Angle.Angle()
        try:
            assumedLongitudeAngle.setDegreesAndMinutes(assumedLongitude)
        except:
            return 0
        
        return assumedLongitudeAngle.getDegrees()
    
    def getAdjustments(self,geoPositionLongitude,geoPositionLatitude,assumedLongitudeAngle,assumedLatitudeAngle,adjustedAltitude):                 
        LHA = geoPositionLongitude - assumedLongitudeAngle
        
        sinGeoLatitude = math.sin(math.radians(geoPositionLatitude))
        sinAssumedLa = math.sin(math.radians(assumedLatitudeAngle))
        cosAssumedLa = math.cos(math.radians(assumedLatitudeAngle))
        sinResult =  sinGeoLatitude * sinAssumedLa  
        cosResult = math.cos(math.radians(geoPositionLatitude)) * cosAssumedLa * math.cos(math.radians(LHA))              
        Result = sinResult + cosResult
        correctedAltitude = math.asin(Result)                
        
        distanceAdjustment = round((adjustedAltitude - math.degrees(correctedAltitude)) * 60.0,0)
                     
        aziDenominator = sinGeoLatitude - sinAssumedLa * math.sin(math.radians(distanceAdjustment))
        aziNumerator = cosAssumedLa * math.cos(math.radians(distanceAdjustment)) 
        result = aziNumerator/aziDenominator
        azimuthTemp = math.acos(result)
                
        return azimuthTemp, distanceAdjustment                                  