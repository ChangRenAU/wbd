class Angle():

    def __init__(self):
        self.angle = 0.0
        self.className = "Angle."
            
    def setDegrees(self, degrees=0):
        methodName = "setDegrees:  "
        
        if(not(isinstance(degrees,(int,float)))):
            raise ValueError(self.className + methodName + "invalid degrees")
        try:
            temp=float(degrees)  
            self.angle = temp%360.0
            return self.angle
                
        except ValueError:
            print("ValueError!!!")
                  
    def setDegreesAndMinutes(self, degrees=None):
        methodName="setDegreesAndMinutes:  "

        if(degrees == None):
            raise ValueError(self.className + methodName + "invalid angle")
        if(not(isinstance(degrees,str))):
            raise ValueError(self.className + methodName + "invalid angle")
       
        try:
            tag = degrees.index('d')
            if(tag == 0):
                raise ValueError
                       
            nums=str(degrees).split('d')
            start,end = map(float,nums)
            
            #degrees should be int 
            tagStart = str(start).find('.0')
            if(tagStart == -1):
                raise ValueError
            #minutes should greater than 0
            if("-" in str(end)):
                raise ValueError
            
            #minutes must have only one decimal place     
            tagEnd = str(end).find(".")
            if(tagEnd != -1):
                if((tagEnd == 0) or (len(str(end))-tagEnd > 2)):
                    raise ValueError
            
            if start >= 0.0:
                self.angle = float((start%360.0 + end/60.0)%360.0)
                
            elif start < 0.0 and (start%360.0 - end/60.0) > 0.0:
                self.angle = float(start%360.0 - end/60.0)
            
            elif start < 0.0 and (start%360.0 - end/60.0) < 0.0:
                self.angle = float(start%360.0 - end/60.0 + 360.0)
                
        except:
            raise ValueError(self.className + methodName + "invalid angle")
        
        return self.angle
      
    def add(self, angle = None):
        methodName = "add:  "
        if(angle == None):
            raise ValueError(self.className + methodName + "invalid angle")
        if(not(isinstance(angle,Angle))):
            raise ValueError(self.className + methodName + "invalid angle")
        try:            
            self.angle += angle.getDegrees()
            temp=float(self.angle)  
            self.angle = temp%360.0
            return self.angle
        
        except:
            raise ValueError(self.className + methodName + "ValueError")
    
    def subtract(self, angle = None):
        methodName = "subtract:  "
        if(angle == None):
            raise ValueError(self.className + methodName + "invalid angle")
        if(not(isinstance(angle,Angle))):
            raise ValueError(self.className + methodName + "invalid angle")
        
        try:
            self.angle -= angle.getDegrees()
            temp=float(self.angle)  
            self.angle = temp%360.0
            return self.angle
        
        except:
            raise ValueError(self.className + methodName + "ValueError")
                
    def compare(self, angle = None):
        methodName = "compare:  "
        if(angle == None):
            raise ValueError(self.className + methodName + "invalid angle")
        if(not(isinstance(angle,Angle))):
            raise ValueError(self.className + methodName + "invalid angle")
        
        if (self.angle > angle.getDegrees()):
            return 1
        elif (self.angle < angle.getDegrees()):
            return -1
        else:
            return 0
    
    def getString(self):
        
        temp = self.getDegrees()
        self.start = int(temp)
        self.end = round((temp - self.start)*60,1)
        wholestring = str(self.start)+'d'+str(self.end)
        return wholestring    
    
    def getDegrees(self):
        
        temp = self.angle
        degree= int(temp)
        if(degree == 0):
            tempMinute = temp
        else:
            tempMinute = temp % degree
        minute = round(tempMinute*60,1)/60
        temp = degree + minute
        return temp

