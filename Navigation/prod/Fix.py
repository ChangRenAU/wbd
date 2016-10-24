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
            raise ValueError(self.className + methodName + "file cannot be created or appended") 
        
        writetime = self.getTime()             
        startofLog = ["LOG:\t",writetime,"\tStart of log\n"]
        self.openlogFile.writelines(startofLog)
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
         
        self.openlogFile = open(self.logFile,'a+')
        writetime = self.getTime()
        startofSighting = ["LOG:\t",writetime,"\tStart of sighting file:\t",self.sightingFile,"\n"]
        self.openlogFile.writelines(startofSighting)
        self.openlogFile.close()
          
        return self.sightingFile
    
    def setAriesFile(self):
        pass
    
    def setStarFile(self):
        pass
      
    def getSightings(self):
        methodName = "getSightings:  "        
        approximateLatitude = "0d0" 
        approximateLongitude = "0d0"        
        if (self.sightingFile == None):
            raise ValueError(self.className + methodName + "No sighting file has been set.")
        info = self.getTree(self.sightingFile)
        sightings = info.getroot()
        num = len(sightings)                    
        #get Elements by tag name
        bodies = info.getiterator("body")
        dates = info.getiterator("date")
        times = info.getiterator("time")
        observations = info.getiterator("observation")
        heights = info.getiterator("height")
        temperatures = info.getiterator("temperature")
        pressures = info.getiterator("pressure")
        horizons = info.getiterator("horizon")             
        #tag or text is missing
        for child in info.findall("sighting"):
            tagofbody = child.find("body")
            if tagofbody == None:
                raise ValueError(self.className + methodName + "missing tag of body")
            else:
                body = tagofbody.text
                if body == None:
                    raise ValueError(self.className + methodName + "missing content of body")
                    
            try:
                tagofdate = child.find("date")  
            except:
                raise  ValueError(self.className + methodName + "missing tag of date")    
            if tagofdate == None:
                raise ValueError(self.className + methodName + "missing tag of date")
            else:
                date = tagofdate.text
                try:
                    time.strptime(date,"%Y-%m-%d")  
                except:  
                    raise ValueError(self.className + methodName + "wrong format of date")   
 
            tagoftime = child.find("time")
            if tagoftime == None:
                raise ValueError(self.className + methodName + "missing tag of time")
            else:
                observedtime = tagoftime.text
                try:
                    time.strptime(observedtime, "%H:%M:%S")
                except:
                    raise ValueError(self.className + methodName + "wrong format of time") 

        for i in range(0,num):                              
            nums = str(observations[i].text).split('d')
            start, end = map(float,nums)
            if (start >= 90 or start < 0 or end < 0 or end >= 60 or (start == 0.0 and end < 0.1)):
                raise ValueError(self.className + methodName + "invalid observation")   
            if heights[i].text is None:
                heights[i].text = 0
            try:
                heights[i].text = float(heights[i].text)
            except:    
                raise ValueError(self.className + methodName + "invalid height")   
            if heights[i].text < 0:
                raise ValueError(self.className + methodName + "invalid height")
            
            if temperatures[i].text is None:
                temperatures[i].text = 72
            try:
                temperatures[i].text = float(temperatures[i].text)
            except:    
                raise ValueError(self.className + methodName + "invalid height")  
            if temperatures[i].text < -20 or temperatures[i].text > 120:
                raise ValueError(self.className + methodName + "invalid temperature")
            
            if pressures[i].text is None:
                pressures[i].text = 1010
            try:
                pressures[i].text = float(pressures[i].text)
            except:    
                raise ValueError(self.className + methodName + "invalid height")  
            if pressures[i].text < 100 or pressures[i].text > 1100:
                raise ValueError(self.className + methodName + "invalid pressure")
            
            if horizons[i].text is None:
                horizons[i].text = "Natural"
            elif horizons[i].text not in ['Natural','Artificial']:
                raise ValueError(self.className + methodName + "invalid horizon")               
                  
            sightings[i] = bodies[i].text,dates[i].text,times[i].text,observations[i].text,heights[i].text,temperatures[i].text,pressures[i].text,horizons[i].text
              
        for i in range(0,num):
            for j in range(i+1,num):
                if dates[i].text > dates[j].text:
                    sightings[i],sightings[j] = sightings[j],sightings[i]
                elif dates[i].text == dates[j].text and times[i].text > times[j].text:
                    sightings[i],sightings[j] = sightings[j],sightings[i]  
                elif dates[i].text == dates[j].text and times[i].text == times[j].text and bodies[i].text > bodies[j].text:
                        sightings[i],sightings[j] = sightings[j],sightings[i]
             
        anAngle = Angle.Angle()
        for i in range(0,num):        
            observedAltitudes = anAngle.setDegreesAndMinutes(sightings[i][3])
            adjustedAltitudes = self.calculateAdjustedAltitude(sightings[i][4],sightings[i][6],sightings[i][5],sightings[i][7],observedAltitudes)         
            self.openlogFile = open(self.logFile,'a+')
            logofSighting = ["LOG:\t",self.getTime(),"\t",sightings[i][0],"\t",sightings[i][1],"\t",sightings[i][2],"\t",adjustedAltitudes,"\n"]
            self.openlogFile.writelines(logofSighting)
            self.openlogFile.close()    

        self.openlogFile = open(self.logFile,'a+')
        endofSighting = ["LOG:\t",self.getTime(),"\tEnd of sighting file:\t",self.sightingFile,"\n"]
        self.openlogFile.writelines(endofSighting)
        self.openlogFile.close() 
          
        return (approximateLatitude, approximateLongitude) 
    
    def getTree(self,sightingfilename):
        if sightingfilename == None:
            raise ValueError("no sighting file has been set")
        else:
            tree = ET.parse(sightingfilename)
        return tree
 
    def calculateAdjustedAltitude(self, height, pressure, temperature, horizon, observedAltitude):
        if (horizon == "Natural"):
            dip = (-0.97 * math.sqrt(height)) / 60.0
        else:
            dip = 0.0    
         
        refraction = (-0.00452 * float(pressure)) / (273 + ((float(temperature) - 32.0 ) / 1.8 ))/ math.tan(math.radians(observedAltitude))
        adjustedAltitude = observedAltitude + dip + refraction
        anAngle = Angle.Angle()
        anAngle.setDegrees(adjustedAltitude)
        result = anAngle.getString()
        return result  

    def getTime(self):    
        timenow = datetime.datetime.utcnow().replace(microsecond=0).isoformat(' ') 
        timezone = "-06:00"
        time = timenow + timezone
        return time   