'''
Created on Sep 9, 2016

@author: cici
'''
import Navigation.prod.Angle as Angle

angle1 = Angle.Angle()
angle2 = Angle.Angle()
angle3 = Angle.Angle()
angle4 = Angle.Angle()

#Attempt to set an invalid value should result in ValueError exception bearing a diagnostic message
angle1Degrees = angle1.setDegreesAndMinutes("45d50")
angle2Degrees = angle2.setDegrees(-19.5)
angle3Degrees = angle3.setDegreesAndMinutes("700d1")
print angle1Degrees
print angle2Degrees
print angle3Degrees

try:
    invalidAngle = angle2.setDegreesAndMinutes()
except ValueError as raisedException:
    diagnosticString = raisedException.arg[0]
  
#---------------add------------------    
addedDegree1 = angle1.add(angle2)
addedDegree3 = angle2.add(angle3)

   
#--------------subtract--------------
subtractedDegrees = angle4.subtract(angle1)

      
#--------------compare--------------
angle1.setDegrees(45.0) 
angle2.setDegrees(45.1)

try:
    angle1.compare(42.0)
except ValueError as raisedException:
    diagnosticString = raisedException.arg[0]
    
#-------------getString-------------
angle1String = angle1.getString()
angle2String = angle2.getString()
angle3.setDegrees(45.123)
angle3String = angle3.getString()
print angle3String

#-------------getDegrees-------------
angle1Degrees = angle1.getDegrees()
angle2Degrees = angle2.getDegrees()
angle3Degrees = angle3.getDegrees()    
