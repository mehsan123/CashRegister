import fnmatch
import os
import sys
import urllib
import xml.etree.ElementTree as ET
import xmltodict
import json
from junit_xml import TestSuite, TestCase
from html.parser import HTMLParser
from datetime import date
import datetime
testCases=[]

workarearoot=''   
sourceRoot=''

class LDRA_TestCase():
    def __init__(self, TCNo, TCProc, TCFile, TCInput, TCOutput, TCStatus,TCSet, TCSeq, TCDescription ):
        self.TCNo = TCNo
        self.TCProc = TCProc
        self.TCFile = TCFile
        self.TCInput = TCInput
        self.TCOutput = TCOutput
        self.TCStatus = TCStatus
        self.TCSet = TCSet
        self.TCSeq = TCSeq
        self.TCDescription = TCDescription

     
    def __str__(self):
        return (self.TCNo, self.TCProc, self.TCFile, self.TCInput, self.TCOutput, self.TCStatus, TCSet, TCSeq) 
        
    def printCoverageElement (self):
        return(self.TCNo +' ' + self.TCProc +' ' + self.TCFile +' ' + self.TCInput +' ' + self.TCOutput +' ' + self.TCStatus+ self.TCDescription)
        
    def getTCNo(self):
        return (self.TCNo)
        
    def getcovElementName(self):
        return (self.covElementName)
        
    def getTCProc(self):
        return (self.TCProc)
        
    def getTCFile(self):
        return (self.TCFile)
    
    def getTCInput(self):
        return (self.TCInput)
        
    def getTCOutput(self):
        return (self.TCOutput)
        
    def getTCStatus(self):
        return (self.TCStatus)
        
    def getTCSet(self):
        return (self.TCSet) 
    
    def getTCSeq(self):
        return (self.TCSeq)     

    def getTCDescription(self):
        return (self.TCDescription) 
        
               
    
    def setTCNo(self):
        self.TCNo = TCNo
        
    def setcovElementName(self):
        self.covElementName = covElementName
        
    def setTCProc(self):
        self.TCProc = TCProc
        
    def setTCFile(self):
        self.TCFile = TCFile
    
    def setTCInput(self):
        self.TCInput = TCInput
        
    def setTCOutput(self):
        self.TCOutput = TCOutput
        
    def setTCStatus(self):
        self.TCStatus = TCStatus
        
    def setTCSet(self):
        self.TCSet = TCSet
    
    def setTCSeq(self):
        self.TCSeq = TCSeq     
        
    def setTCDescription(self,TCDescription):
        self.TCDescription = TCDescription 
        print(self.TCDescription)
        
    
        
######################################################################################
def init():
    global sourceRoot, workarearoo
    sourceRoot = sys.argv[1]

    #from fourth argument locate directory for specified project
##########################################
def html_parser():
    init()


def arrayTrim(line):
    l=[]
    l = str(line).split(" ")
    l2=[]
    l3=''
    l[0]=l[0][l[0].find("'")+1:] #removing the first b' at the beginning of everyline
    
    for i in l:
        if i != '':
            if i != ' ':
                if l.index(i) == (len(l)-1):  
                    l2.append(i[:-5])
                else:
                    l2.append(i)
    if ('ordering' in l2):
        l2[l2.index('FAIL')]= l2[l2.index('FAIL')]+' ' + l2[l2.index('stub')]+' ' + l2[l2.index('ordering')]
        l2.remove('ordering')
        l2.remove('stub')
    if ('hit' in l2):
        l2[l2.index('FAIL')]= l2[l2.index('FAIL')]+' '+l2[l2.index('stub')]+' '+ l2[l2.index('hit')]+' '+l2[l2.index('count')]
        l2.remove('stub')
        l2.remove('hit')
        l2.remove('count')
    if ('VALIDATION' in l2):
        l2[l2.index('FAILED')]= l2[l2.index('FAILED')]+' '+l2[l2.index('VALIDATION')]
        l2.remove('VALIDATION')
        
    if ('Case' in l2 and 'Procedure' in l2):
        l2[l2.index('Test')]= l2[l2.index('Test')]+' '+l2[l2.index('Case')]
        l2.remove('Case')
    return l2

def findFiles(sourceRoot):
    print("Finding THR files...",sourceRoot)
    fileName = []
    for r, d, f in os.walk(sourceRoot):
        for item in f:
            if item.endswith(".thr.txt"):
                print("Found THR File",item)
                fileNamePath = str(os.path.join(r,item))
                fileName.append(fileNamePath)
    if len(fileName) ==0 :
        print("No THR file has been found!")
        
    else:
        for i in fileName:
            print("fileName",i)
            parseThr(str(i))
        
def parseThr(sourceRoot):
    print("Parsing the file name: ",sourceRoot)
    testCases=[]
    f=open(sourceRoot,'rb')
    print(sourceRoot)

    flag1 =0
    flag2=0
    f2=open("f.txt",'w')

    
    for line in f:
        if "Set :" in str(line):    
            l=str(line).split(" ")
            setName = l[l.index(":")+1]
            print('Set Name is: '+setName)

        if "Set:" in str(line):    
            print('Set Nameee')
            l=str(line).split(" ")
            while("" in l) :
                l.remove("")
            setName = l[l.index("Set:")+1][:-5]
            print('Set Name is: '+setName)       
            
    
        if "Sequence :" in str(line):    
            l=str(line).split(" ")
            seqName = l[l.index(":")+1]
            print('Sequence Name is: '+seqName)
            
        
        if "Sequence" in str(line):    
            l=str(line).split(" ")
            while("" in l) :
                l.remove("")
            l[0]=l[0][l[0].find("'")+1:]
            seqName = l[l.index("Sequence")+1]
            print('Sequence Name is: '+seqName)
            
        if "Test Case Regression Summary Table" in str(line):
            flag1 = 1
            print("flag is :",flag1)
            
        if "Test Case 1 :" in str(line) or 'Test Case 1 :' in str(line) :
            print(line)
            flag1 = 0
            flag2 = 0
            #print("flag is :",flag1)
            break
            
        
        if flag1 == 1 :
            l2=[]
            l2=arrayTrim(line)
            if "INPUTS" in l2:
                print('TITLE found')
                tcNoCol     = l2.index('TEST')
                tcProcCol   = l2.index('PROCEDURE')-1
                tcFileCol   = l2.index('FILE')-1
                tcInCol     = l2.index('INPUTS')-4
                tcOutCol    = l2.index('OUTPUTS')-4
                tcStatusCol = l2.index('STATUS')-4
                print("Columns are: ", tcNoCol, tcProcCol, tcFileCol, tcInCol, tcOutCol, tcStatusCol, ' ')
                flag2=1
            if ("Test Case" in l2) and ("Suspended%"in l2):
                print('Harness Text Report')
                print(l2)
                tcNoCol     = l2.index('Test Case')
                tcProcCol   = l2.index('Procedure')
                tcFileCol   = l2.index('File')
                tcInCol     = l2.index('Inputs')
                tcOutCol    = l2.index('Outputs')
                tcStatusCol = l2.index('Status')
                print("Columns are: ", tcNoCol, tcProcCol, tcFileCol, tcInCol, tcOutCol, tcStatusCol, ' ')
                flag2=1
                
        if flag1 ==1 and flag2 == 1 :
            l2=[] 
            l2=arrayTrim(line)
            
            #print(l2)
            #print(len(l2))
            
            if len(l2)>3:
                if l2[tcNoCol] != '=' or l2[tcNoCol] != '-' :
                    if 'TEST' not in l2:
                        if '*' not in l2 or '=' not in l2:
                        
                            if ('PASS' in l2 or 'FAIL' in l2 or 'FAIL stub ordering' in l2 or 'FAILED VALIDATION' in l2 or 'FAIL stub hit count' in l2):
                                #f2.write("The rest are "+' ' +l2[tcInCol]+ ' ' +l2[tcOutCol]+ ' '+l2[tcStatusCol]+'\n')
                                
                                testInput = l2[tcInCol]
                                testOut = l2[tcOutCol]
                                testCaseNo=l2[tcNoCol]
                                testCasefile = l2[tcFileCol]
                                testCaseproc = l2[tcProcCol]
                                testStatus = l2[tcStatusCol]
                                testCases.append(LDRA_TestCase(testCaseNo, testCasefile, testCaseproc,testInput, testOut, testStatus,setName,seqName,' '  ))
                                f2.write(testCaseNo+' '+testCasefile+' '+ testCaseproc+' '+testInput+' '+ testOut+' '+ testStatus+' '+setName+' '+seqName+'\n')
                                testCaseNo=''
                                testCasefile = ''
                                testCaseproc = ''
                                testInput = ''
                                testOut = ''
                                testStatus = ''

                            else:
                                #print(l2)
                                #f2.write("Tests are"+' '+l2[tcNoCol]+' '+l2[tcProcCol]+' '+l2[tcFileCol]+'\n')
                                testCaseNo  = l2[tcNoCol]
                                testCasefile = l2[tcFileCol]
                                testCaseproc= l2[tcProcCol]
            
            elif len(l2) == 3:
                print('length is 3')
                print(l2)                    
                l2=[]
                l2=arrayTrim(line)
                #f2.write("Tests are 3::: "+l2[tcNoCol]+' ' + l2[tcProcCol]+'\n')
                if ('VALIDATION' in l2):
                    print('Validation Error !!!!!')
                    testStatus = 'FAILED VALIDATION'
                    testCases.append(LDRA_TestCase(testCaseNo, testCasefile, testCaseproc,'0', '0', testStatus,setName,seqName,' '  ))
                    f2.write(testCaseNo+' '+testCasefile+' '+ testCaseproc+' '+'0'+' '+ '0'+' '+ testStatus+' '+setName+' '+seqName+'\n')
                testCaseNo  = l2[tcNoCol]
                testCaseproc = l2[tcProcCol]
                
                
            elif len(l2) == 2:

                l2=[]
                l2=arrayTrim(line)

                #f2.write("Tests are 2::: "+l2[tcNoCol]+'\n')
                testCasefile = l2[tcNoCol]
    
    #parseError(sourceRoot)
    parseDescription(sourceRoot)
    junit_generator(testCases,sourceRoot)
            
def testCaseTrim(line):
    l=[]
    l = str(line).split(" ")
    l2=[]
    l3=''
    l[0]=l[0][l[0].find("'")+1:] #removing the first b' at the beginning of everyline
    
    for i in l:
        if i != '':
            if i != ' ':
                if l.index(i) == (len(l)-1):  
                    l2.append(i[:-5])
                else:
                    l2.append(i)

    return l2
def parseDescription (sourceRoot):                    
    f=open(sourceRoot,'rb')
    l=''
    flag1=0
    TCNo=[]
    for test in testCases:
        TCNo.append(test.getTCNo())
    for line in f:
        if ("=== Test Case"  in str(line)):
            l= testCaseTrim(str(line))
            if(l[3].isnumeric()):
                flag1 =1
                testNo=l[3]
        if flag1 ==1:
            if ('Description' in str(line)):
                l= testCaseTrim(str(line))
                print("Discription found in Test Case:",testNo)
                print(l)
                testCases[int(testNo)-1].setTCDescription(l[1:])
                flag1 =0
    for i in testCases:
        print(i.getTCDescription())
                
                
            

            
##############################################################################
##################################################################
#'''<?xml version="1.0" encoding="UTF-8" ?>                                                                                                     # 
#   <testsuites id="20140612_170519" name="New_configuration (14/06/12 17:05:19)" tests="225" failures="1262" time="0.001">                     #
#      <testsuite id="codereview.cobol.analysisProvider" name="COBOL Code Review" tests="45" failures="17" time="0.001">                        #
#         <testcase id="codereview.cobol.rules.ProgramIdRule" name="Use a program name that matches the source file name" time="0.001">         #
#            <failure message="PROGRAM.cbl:2 Use a program name that matches the source file name" type="WARNING">                              #
#WARNING: Use a program name that matches the source file name                                                                                  #
#Category: COBOL Code Review – Naming Conventions                                                                                               #
#File: /project/PROGRAM.cbl                                                                                                                     #
#Line: 2                                                                                                                                        #
#      </failure>                                                                                                                               #         
#    </testcase>                                                                                                                                #
#  </testsuite>                                                                                                                                 #
#</testsuites>'''                                                                                                                               #
#                                                                                                                                               #
# '''                                                                                                                                           #
#def testMultiTestCasesToConsole():                                                                                                             #
#    ''' Demonstrates a single test suite with multiple test cases, one of which                                                                #
#        has failure info. Output to console.                                                                                                   #
#    '''                                                                                                                                        #
#                                                                                                                                               #
#    test_cases = [TestCase('Test1', 'some.class.name', 123.345, 'I am stdout!', 'I am stderr!')]                                               #
#    test_cases.append(TestCase('FileCheck: PropertyServer', '', .0452, '', ''))                                                                #
#    test_cases[0].add_failure_info('Invalid File \'DNC.exe\'.')                                                                                #
#    ts = [TestSuite("DirectorITG2", test_cases)]                                                                                               #
#    # pretty printing is on by default but can be disabled using prettyprint=False                                                             #
#    print(TestSuite.to_xml_string(ts)))'''                                                                                                     #
#################################################################################################################################################

def junit_generator(testCases,sourceRoot):
    jtest_cases=[]
    today = datetime.datetime.now()
    today=today.strftime("%H%M")
    today=str(today)
    time=today[-5:]
    time=time.replace('-','')
    print("Today's date:", time)
    for i in testCases:
        testDiscription = i.getTCDescription()
        testCaseNo = i.getTCNo()
        testCaseNo='Test Case '+ str(testCaseNo)
        testCasefile = i.getTCFile()
        testCaseproc = i.getTCProc()
        testInput = i.getTCInput()
        testOut = i.getTCOutput()
        testStatus = i.getTCStatus()
        setName = i.getTCSet()
        seqName = i.getTCSeq()
        jtest_cases.append(TestCase(testCaseNo,testCaseproc,int(today),testDiscription, testStatus))
    ts = [TestSuite(setName, jtest_cases)]
    with open (sourceRoot+".junit", mode='w') as f :
        TestSuite.to_file(f, ts)   
    f.close()
        
def textParser(textStart, textEnd):
    startt_flag=0
    for line in f:
        if textStart in line:
            startt_flag=1    
        elif flag == 1:
            print('Oh well')
            
            
            
    
    
    
def main()  : 
    html_parser()  
    findFiles(sourceRoot)



if __name__ == "__main__":
    main()
