import re
class Angle():

    def __init__(self,angle=0):
        self.angle = angle
            
    def setDegrees(self, degrees=0):
        
        if(not(isinstance(degrees,(int,float)))):
            raise ValueError("This degrees should be an int or float.")
        try:
            temp=float(degrees)  
            self.angle = round(temp%360.0,1)
            return self.angle
                
        except ValueError:
            print("ValueError!!!")
                  
    def setDegreesAndMinutes(self, angleString=None):
       
        try:
            
            nums=str(angleString).split('d')
            start,end = map(float,nums)
            
            #check to see if the start is 
            if not re.search(r'\.',str(start)):
                raise ValueError("ValueError!")
            
            if start > 0:
                self.angle = round((start%360 + end/60.0)%360,1)
                return self.angle
            
            elif start < 0 and (start%360 - end/60) > 0:
                self.angle = round((start%360 - end/60.0),1)
                return self.angle
            
            elif start < 0 and (start%360 - end/60) < 0:
                self.angle = round((start%360 - end/60 + 360.0),1)
                return self.angle
                
            else:
                raise ValueError("Value Error.Input error.")
                
        except ValueError:
            print("Value Error.Input error.")
   
   
    def add(self, angle):
       
        try:
            
            self.angle += float(angle)
            return self.angle
        
        except ValueError:
            print("Input error, ValueError!!!")
    
    def subtract(self, angle):
        
        try:

            self.angle -= float(angle)
            return self.angle
        
        except ValueError:
            print("Input error, ValueError!!!")
            
    
    def compare(self, angle):

        try:
            temp = float(angle)
            if self.angle>temp:
                return 1
            elif self.angle<temp:
                return -1
            else:
                return 0
            
        except ValueError:
            print("Input error, ValueError!!!")

    
    def getString(self):
        
        self.start = int(self.angle)
        self.end = (self.angle - self.start)*60
        return   str(self.start)+'d'+str(self.end)
    
    
    def getDegrees(self):
              
        return self.angle