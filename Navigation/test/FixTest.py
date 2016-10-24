import os
import unittest
import Navigation.prod.Fix as Fix


# import os.path
class FixTest(unittest.TestCase):
      

    def setUp(self):
        self.className = "Fix."
        try:
            os.remove("log.txt")
        except:
            pass
        
    def tearDown(self):
        pass

#    Acceptance Test: 100
#        Analysis - Contructor
#            inputs
#                logfile:string, optional, unvalidated
#            outputs
#                returns: instance of Fix
#                also: writes an entry to log file:Start of log
#
#            Happy path
#                logFile:
#                   omitted -> Fix()
#                   new logfile ->Fix("myLog.txt")
#                   existing logfile ->Fix("myLog.txt") assuming myLog.txt ex
#            Sad path
#                logFile:
#                nullstring ->Fix("") 
#                nonstring -> Fix(12)

#
#    Happy path
    def test100_010_ShouldCreateInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix(), Fix.Fix)
    
    def test100_020_ShouldConstructFixWithDefaultFile(self):
        theFix = Fix.Fix()
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readline()
        self.assertNotEqual(-1,entry.find("Start of log\n"))
        self.assertIsInstance(theFix, Fix.Fix)

#    Sad path
    def test100_910_ShouldRaiseExceptionOnEmptyFileNameParm(self):
        expectedDiag = self.className + "__init__:  "
        with self.assertRaises(ValueError) as context:
            Fix.Fix("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test100_920_ShouldRaiseExceptionOnIntegerFileNameParm(self):
        expectedDiag = self.className + "__init__:  "
        with self.assertRaises(ValueError) as context:
            Fix.Fix(12)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

#-----------------------------------------------------------------
#    Acceptance Test: 200
#        Analysis - setSightingFile
#            inputs
#                XML file
#            outputs
#                A string having the value passed as the "sightingFile".
#            state change
#                write following entry to log file
#                Start of sighting file f.xml
#
#            Happy path
#                right return value
#                also: writes an entry to log file:Start of sighting file f.xml
#            Sad path
#                singtingFile:
#                null 
#                nonstring ->123
#                string without .xml -> abc

#    Happy path
    def test200_010_ShouldReturnTheSightingFile(self):
        expectedName = "abc.xml"
        theFix = Fix.Fix()
        returnedValue = theFix.setSightingFile(expectedName)
        self.assertEqual(expectedName,returnedValue)
        
    def test200_020_ShouldWriteEntryofSightingFile(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[1].find("Start of sighting file")) 
                
#     Sad Path
    def test200_910_ShouldRaiseExceptionOnEmptyFileNameParm(self):
        expectedDiag = self.className + "setSightingFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
         
    def test200_920_ShouldRaiseExceptionOnIntegerFileNameParm(self):
        expectedDiag = self.className + "setSightingFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(123)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
         
    def test200_930_ShouldRaiseExceptionOnWrongFormatFileNameParm(self):
        expectedDiag = self.className + "setSightingFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("abc")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
          
#-----------------------------------------------------------------
#    Acceptance Test: 300
#        Analysis - getSightings
#            inputs
#                none
#            outputs
#                Returns tuple(approximateLatitude, approximateLongitude) with value("0d0","0d0")
#            state change
#                Navigational calculations are written to the log file.
#                also:write following entry to log file
#                End of sighting file f.xml
#
#            Happy path
#                nominal case: should return("0d0","0d0")
#                nominal case: "End of sighting file" should be written into log.txt
#                nominal case: log should be logged be in chronological order
#                nominal case: AdjustedAltitude should be 15d01.5

#            sad path
#                body tag is missing
#                body content is empty
#                date tag is missing
#                date content is not in "yyyy-mm-dd" format
#                time tag is missing
#                time content is not in "hh:mm:ss" format
#                observation degree part is G.E. 90 or minute part G.E. 60 
#                observation altitude LT. 0.1
#                height content is not a numeric
#                height content is not G.E. 0
#                temperature content is not an integer -> abc
#                temperature content is not in range G.E. -20 L.E.120
#                pressure content is not an integer -> abc
#                pressure content is not in range G.E.100 L.E.1100
#                horizon content is neither "Artificial" nor "Natural"

#    Happy path
    def test300_010_ShouldReturnSpecificValue(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        theFix.getSightings()
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[-1].find("End of sighting file")) 
        
    def test300_020_ShouldWriteEndofSightingFileIntoLogFile(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        theFix.getSightings()
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[-1].find("End of sighting file")) 
    
    def test300_030_ShouldLogSightingInChronologicalOrder(self):         
        expectedSighting1 = "Aldebaran"
        expectedSighting2 = "Peacock"
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml") 
        theFix.getSightings()
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1, entry[2].find(expectedSighting1))
        self.assertNotEqual(-1, entry[3].find(expectedSighting2))
        
    def test300_040_ShouldCalculateAdjustedAltitudeRight(self):
        expectedAltitude = "15d1.5"
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        theFix.getSightings()
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1, entry[2].find(expectedAltitude))
        
#     sad path 
  
    def test300_910_ShouldRaiseErrorWithBodyTagMissing(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("missbodytag.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
    
    def test300_911_ShouldRaiseErrorWithEmptybody(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("emptybody.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
           
    def test300_920_ShouldRaiseErrorWithDateTagMissing(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("missdatetag.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
    
    def test300_921_ShouldRaiseErrorWithWrongFormatDate(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("wrongformatdate.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
  
    def test300_930_ShouldRaiseErrorWithTimeTagMissing(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("misstimetag.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
 
    def test300_931_ShouldRaiseErrorWithWrongFormatTime(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("wrongformattime.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
 
    def test300_940_ShouldRaiseErrorWithOver90DegreeObservation(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("over90degreeobservation.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test300_941_ShouldRaiseErrorWithOver60MinuteObservation(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("over60minuteobservation.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
 
    def test300_942_ShouldRaiseErrorWithLessThanOpoint1bservationAltitude(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("less0.1altitude.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
 
    def test300_950_ShouldRaiseErrorWithStringHeight(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("stringheight.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
  
    def test300_951_ShouldRaiseErrorWithLessThan0Height(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("lessthan0height.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_960_ShouldRaiseErrorWithStringPressure(self):
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("stringpressure.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_962_ShouldRaiseErrorWithMoreThan1100Pressure(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("morethan1100pressure.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test300_962_ShouldRaiseErrorWithLessThan100Pressure(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("lessthan100pressure.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_970_ShouldRaiseErrorWithStringTemperature(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("stringtemperature.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_971_ShouldRaiseErrorWithMoreThan120Temperature(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("morethan120temperature.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test300_972_ShouldRaiseErrorWithLessThanMinus20Temperature(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("lessthanminus20temperature.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_980_ShouldRaiseErrorWithWrongHorizon(self):         
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("wronghorizon.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])