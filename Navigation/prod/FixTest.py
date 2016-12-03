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
        self.assertNotEqual(-1,entry.find("Log file"))
        self.assertIsInstance(theFix, Fix.Fix)
        
    def test100_030_ShouldConstructFixWithNamedFile(self):
        theFix = Fix.Fix('myLogFile.txt')
        try:
            theLogFile = open('myLogFile.txt', 'r')
            entry = theLogFile.readline()
            del theLogFile
            self.assertNotEquals(-1, entry.find("Log file"))                                
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, Fix.Fix, "major:  log file failed to create")
        os.remove('myLogFile.txt')


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
#        inputs:
#            sightingFile: string, mandatory, unvalidated, format = f.xml (len(f) >= 1)
#        outputs:
#            returns:  string with file name
#            also:    writes path of Sighting file to log file
#
#            Happy path
#                right return value
#                also: writes an the path to log file:"Sighting file:path" f.xml
#            Sad path
#                singtingFile:
#                missing 
#                length error ->(.xml)
#                nonstring ->123
#                nonXML -> setSightingFile("sightingFile.txt")
#                string without .xml -> abc
#                nonexistent file -> setSightingFile(missing.xml)

#    Happy path
    def test200_010_ShouldReturnThePathofSightingFile(self):
        expectedName = "abc.xml"
        theFix = Fix.Fix()
        returnedValue = theFix.setSightingFile(expectedName)
        self.assertNotEqual(-1,returnedValue.find(expectedName))
        
    def test200_020_ShouldWriteEntryofSightingFile(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[1].find("Sighting file")) 
        myLogFile.close()       
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
    
    def test200_940_ShouldRaiseExceptionOnLengthErrorFileNameParm(self):
        expectedDiag = self.className + "setSightingFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(".xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
     
    def test200_950_ShouldRaiseExceptionOnNonexistentFile(self):
        expectedDiag = self.className + "setSightingFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("missing.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
    
    def test200_960_ShouldRaiseExceptionOnNonXMLFileNameParm(self):
        expectedDiag = self.className + "setSightingFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("sightingFile.txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

#-----------------------------------------------------------------
#    Acceptance Test: 300
#        Analysis - setStarFile
#        inputs:
#            StarFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  string contains file name
#            also:    writes path of Star file to log file
#
#            Happy path
#                right return value
#                also: writes an the path to log file:"Star file:path" f.txt
#            Sad path
#                missing 
#                length error ->(.txt)
#                nonstring ->123
#                nonTXT -> ("StarFile.xml")
#                string without .txt -> abc
#                nonexistent file -> (missing.txt)

#    Happy path
    def test300_010_ShouldReturnThePathofStarFile(self):
        expectedName = "stars.txt"
        theFix = Fix.Fix()
        returnedValue = theFix.setStarFile(expectedName)
        self.assertNotEqual(-1,returnedValue.find(expectedName))
        
    def test300_020_ShouldWriteEntryofStarFile(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        theFix.setStarFile("stars.txt")
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[2].find("Star file")) 
        myLogFile.close() 
              
#     Sad Path
    def test300_910_ShouldRaiseExceptionOnEmptyFileNameParm(self):
        expectedDiag = self.className + "setStarFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
         
    def test300_920_ShouldRaiseExceptionOnIntegerFileNameParm(self):
        expectedDiag = self.className + "setStarFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(123)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
         
    def test300_930_ShouldRaiseExceptionOnWrongFormatFileNameParm(self):
        expectedDiag = self.className + "setStarFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("abc")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
    
    def test300_940_ShouldRaiseExceptionOnLengthErrorFileNameParm(self):
        expectedDiag = self.className + "setStarFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
     
    def test300_950_ShouldRaiseExceptionOnNonexistentFile(self):
        expectedDiag = self.className + "setStarFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("missing.txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
    
    def test300_960_ShouldRaiseExceptionOnNonTXTFileNameParm(self):
        expectedDiag = self.className + "setStarFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("StarsFile.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])


#-----------------------------------------------------------------
#    Acceptance Test: 400
#        Analysis - setAriesFile
#        inputs:
#            AriesFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  string contains file name
#            also:    writes path of Aries file to log file
#
#            Happy path
#                right return value
#                also: writes an the path to log file:"Aries file:path" f.txt
#            Sad path
#                missing 
#                length error ->(.txt)
#                nonstring ->123
#                nonTXT -> ("AriesFile.xml")
#                string without .txt -> abc
#                nonexistent file -> (missing.txt)

#    Happy path
    def test400_010_ShouldReturnThePathofAriesFile(self):
        expectedName = "aries.txt"
        theFix = Fix.Fix()
        returnedValue = theFix.setAriesFile(expectedName)
        self.assertNotEqual(-1,returnedValue.find(expectedName))
        
    def test400_020_ShouldWriteEntryofAriesFile(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        theFix.setAriesFile("aries.txt")
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[2].find("Aries file")) 
        myLogFile.close() 
              
#     Sad Path
    def test400_910_ShouldRaiseExceptionOnEmptyFileNameParm(self):
        expectedDiag = self.className + "setAriesFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
         
    def test400_920_ShouldRaiseExceptionOnIntegerFileNameParm(self):
        expectedDiag = self.className + "setAriesFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(123)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
         
    def test400_930_ShouldRaiseExceptionOnWrongFormatFileNameParm(self):
        expectedDiag = self.className + "setAriesFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("abc")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
    
    def test400_940_ShouldRaiseExceptionOnLengthErrorFileNameParm(self):
        expectedDiag = self.className + "setAriesFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
     
    def test400_950_ShouldRaiseExceptionOnNonexistentFile(self):
        expectedDiag = self.className + "setAriesFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("missing.txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
    
    def test400_960_ShouldRaiseExceptionOnNonTXTFileNameParm(self):
        expectedDiag = self.className + "setAriesFile:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("AriesFile.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

          
#-----------------------------------------------------------------
#    Acceptance Test: 500
#        Analysis - getSightings
#            inputs
#                none
#            outputs
#                Returns tuple(approximateLatitude, approximateLongitude) with value("0d0","0d0")
#            state change
#                navigational calculations and Geographic Position are written to the log file.
#                also:write sighting Error to log file

#
#            Happy path
#                nominal case: should return("0d0","0d0")
#                nominal case: "sighting Error " should be written into log.txt
#                nominal case: log should be logged be in chronological order
#                nominal case: the following information "Pollux      2017-04-14     23:50:14     15d01.5     27d59.1     84d33.4" should be written in to logfile.
#            Sad path 
#                Sighting file has not been set. 
#                Aries file has not been set. 
#                Star file has not been set. 


#    Happy path
    def test500_010_ShouldReturnSpecificValue(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")        
        theFix.setStarFile("stars.txt")        
        theFix.setAriesFile("aries.txt")
        assumedLatitude = "N27d59.5"            
        assumedLongitude = "85d33.4"            
        approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)   
        self.assertEquals(("0d0","0d0"), approximatePosition)

        
    def test500_020_ShouldWriteSightingErrorIntoLogFile(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")        
        theFix.setStarFile("stars.txt")        
        theFix.setAriesFile("aries.txt")
        assumedLatitude = "N27d59.5"            
        assumedLongitude = "85d33.4"            
        approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)   
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[5].find("Sighting errors:\t")) 
        print entry[5]
        myLogFile.close()
        
    def test500_030_ShouldLogSightingInChronologicalOrder(self):         
        expectedSighting1 = "Pollux"
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")        
        theFix.setStarFile("stars.txt")        
        theFix.setAriesFile("aries.txt")
        assumedLatitude = "N27d59.5"            
        assumedLongitude = "85d33.4"            
        approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)            
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1, entry[4].find(expectedSighting1))
        myLogFile.close()
        
    def test500_040_ShouldCalculateAdjustedAltitudeAndGeographicPositionRight(self):
        expectedInformation = "Pollux\t2017-04-14\t23:50:14\t15d1.5\t27d59.1\t84d33.4\tN27d59.5\t85d33.4\t292d44.6\t174"
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")        
        theFix.setStarFile("stars.txt")
        theFix.setAriesFile("aries.txt")
        assumedLatitude = "N27d59.5"            
        assumedLongitude = "85d33.4"            
        approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)         
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1, entry[4].find(expectedInformation))
        myLogFile.close()
        
    def test500_050_ShouldWriteApproximatePositionIntoLogFile(self):
        expectedInformation = "Approximate latitude:\tN29d6.8\tApproximate longitude:\t82d52.9"
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")        
        theFix.setStarFile("stars.txt")        
        theFix.setAriesFile("aries.txt")
        assumedLatitude = "N27d59.5"            
        assumedLongitude = "85d33.4"            
        approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)   
        myLogFile = open("log.txt",'r')
        entry = myLogFile.readlines()
        self.assertNotEqual(-1,entry[-1].find(expectedInformation)) 
        myLogFile.close()
    
#    Sad path
    def test500_910_shouldRaiseExceptionWithNotSightingFileSet(self):
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("stars.txt")
            theFix.setAriesFile("aries.txt")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
    
    def test500_920_shouldRaiseExceptionWithNotStarFileSet(self):
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("sightings.xml")
            theFix.setAriesFile("aries.txt")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test500_930_shouldRaiseExceptionWithNotSightingFileSet(self):
        expectedDiag = self.className + "getSightings:  "
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("sightings.xml")
            theFix.setStarFile("stars.txt")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])           