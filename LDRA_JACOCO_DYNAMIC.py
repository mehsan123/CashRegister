
import fnmatch
import os
import sys
import xml.etree.ElementTree as ET
import xmltodict
import json
from junit_xml import TestSuite, TestCase
#List of all the Global Data
workarearoot=''   
sourceRoot=''
projectDir=''
#List of all the Source files to be excluded
Filter_Source =[]
#Name of the Set inside of the TCF
SystemTesting = 'systemTesting'
file_coverage = []
sourceRoot=''

######################################################################################
#  Class FunctionCoverage 
# To Get all elements of violations
# covElementType defined whether the coverage is for funcntion or file
######################################################################################
class CoverageElement():
    def __init__(self, covElementType, covElementName, covType, covLines, preCov,curCov, combCov, reqCov, covStatus ):
        self.covElementType = covElementType
        self.covElementName = covElementName
        self.covType = covType
        self.covLines = covLines
        self.preCov = preCov
        self.curCov = curCov
        self.combCov = combCov
        self.reqCov = reqCov
        self.covStatus = covStatus
     
    def __str__(self):
        return (self.covElementType, self.covElementName, self.covType, self.covLines, self.preCov, self.curCov, self.combCov , self.reqCov, self.covStatus )    
        
    def printCoverageElement (self):
        return(self.covElementType +' ' + self.covElementName +' ' + self.covType +' ' + self.covLines +' ' + self.preCov +' ' + self.curCov +' ' + self.combCov +' ' + self.reqCov +' ' + self.covStatus )
        
    def getcovElementType(self):
        return (self.covElementType)
        
    def getcovElementName(self):
        return (self.covElementName)
        
    def getcovType(self):
        return (self.covType)
        
    def getcovLines(self):
        return (self.covLines)
    
    def getcovpreCov(self):
        return (self.preCov)
        
    def getcurCov(self):
        return (self.curCov)
        
    def getcocombCov(self):
        return (self.combCov)
    
    def getreqCov(self):
        return (self.reqCov)
    
    def getcovStatus (self):
        return (self.covStatus)
        
        
#End Class CoverageElement

#####################################################################
def main():
    init()
    runanalysis(workarearoot)
    
    
######################################################################################
#  Function init 
# This function init initialize all the command line argument
######################################################################################
def init():
    global workarearoot, toolsuiteroot

    toolsuiteroot = sys.argv[1]+'\\'

    workarearoot = sys.argv[2]+'\\'
    print('TOOLSUITE ROOT: ROOT: '+toolsuiteroot)
    print('WORKAREA ROOT: '+workarearoot)
    if not os.path.exists(workarearoot):
        os.makedirs(workarearoot)
#################
#  Function findFiles 
# This function will receive the file format needed and returns all the files 
# With this file format
######################################################################################
def findFiles(workarearoot,format):
    print("Finding "+format+ " files...",workarearoot)
    fileName = []
    for r, d, f in os.walk(workarearoot):
        for item in f:
            if item.endswith(format):
                if item != "contents.ldra":
                    print("Found "+format+" File",item)
                    fileNamePath = str(os.path.join(r,item))
                    fileName.append(fileNamePath)
    if len(fileName) ==0 :
        print("No "+format+" file has been found!")
        
    else:
        for i in fileName:
            print("fileName",i)
    return fileName

            
#################
#  Function runanalysis 
# This function runs all the four phases of the static analysis
######################################################################################
def runanalysis(workarearoot):
    #print('Static Analysis is started for: '++prjpath+'\\'+prjname)
    #cppcodestandard = '''"Name of Stanadrd"'''
    #ccodestandard = '''"Name of Standard for c code"'''
    
    #/112n34q run all phases of static analysis
    #-reanalyse_changed_set analyzes set if file has added/removed from set
    #-continue_system_analysis continues analysis even if a file fails analysis
    #-generate_code_review=HTML force generation of HTML code review report.

    
    #command5=(sourceRoot+'Cashregister.exe ')
    #os.system(command5)
    fileName = findFiles(workarearoot,'.ldra')
    #Generating XML for Code Coverage
    for i in fileName:
        xml_file=i[:-5]+'_coverage.xml'
        
        command6 = '{}integration_util.exe /arg=0 /1={} /2={} '.format(toolsuiteroot,xml_file, i)
        os.system(command6)
        
        xml=sendXml(xml_file)
        file_coverage = parseXml(xml)
        jacocoFile=i[:-5]+'_jacoco_coverage.xml'
        jacocoWriter(jacocoFile)

    
def sendXml(tcfName):
    if len(tcfName) != 0:
        xml_file = ET.parse(tcfName)
    
        return(xml_file)
        
    else:
        print("Bad XML File")
    
def parseXml(xml_file):
    

    root = xml_file.getroot()
    
    for node in root.findall("files"):
        for obj in node:
            print(obj.get('source'))
            print(obj)
            if(obj.tag == 'file'):
                for file in obj:
                    if(file.get('type') is  None  ):
                        print("no type",file)
                    else:
                        print(file.get('type'))
                        
                    if(file.tag == 'filecoverage'):
                        print('File Coverage'+obj.get('source'))
                        if (file.get('description') == None):
                        
                            file_coverage.append(CoverageElement('File Coverage',obj.get('source'),file.get('type'), file.get('lines'),file.get('prevpcnt'), file.get('currpcnt'), file.get('combinedpcnt'), file.get('requiredpcnt'), file.get('status')))
                            print('File Coverage',obj.get('source'),file.get('type'), file.get('lines'),file.get('prevpcnt'), file.get('currpcnt'), file.get('combinedpcnt'), file.get('requiredpcnt'), file.get('status'))
                        else:
                            file_coverage.append(CoverageElement('File Coverage',obj.get('source'),file.get('type'), "Not Applicable","Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable"))
                    elif (file.tag =='function'):
                        print('File Coverage'+obj.get('source'))
                        for coverage in file :
                            if(coverage.get('description')  is None ):
                                file_coverage.append(CoverageElement('Procedure Coverage',file.get('name'),coverage.get('type'), coverage.get('lines'),coverage.get('prevpcnt'), coverage.get('currpcnt'), coverage.get('combinedpcnt'), coverage.get('requiredpcnt'), coverage.get('status')))
                                print('Procedure Coverage',file.get('name'),coverage.get('type'), coverage.get('lines'),coverage.get('prevpcnt'), coverage.get('currpcnt'), coverage.get('combinedpcnt'), coverage.get('requiredpcnt'), coverage.get('status'))
                            else:
                                file_coverage.append(CoverageElement('Procedure Coverage',file.get('name'),coverage.get('type'), "Not Applicable","Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable"))
                    else:
                        
                        print("-----------------Not file coverage nor function coverage------------------")
                        print(file.get('source'))
                        print("-----------------------------------")
            
    return file_coverage        
def jacocoWriter(jacocoFile):
    file_name=''
    jfile= open(jacocoFile,mode='w')
    jfile.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
    jfile.write('<!DOCTYPE report PUBLIC "-//JACOCO//DTD Report 1.0//EN" "report.dtd">\n')
    jfile.write('<report name="'+jacocoFile[:-20]+'">\n')
    jfile.write('  <sessioninfo id="unknownhost-TBD" start="0000000000000" dump="0000000000000"/>\n')
    jfile.write('  <package name="'+jacocoFile[:-20]+'">\n')
    flag_file = 0
    flag_proc =0
    print(file_coverage)
    for i in file_coverage:
        
        if i.getcovElementType() == 'File Coverage' and flag_file ==0:
            flag_file = 0
            flag_proc = flag_proc+1
            file_name = i.getcovElementName()
            if i.getcovType() =='Statement Coverage':
                jfile.write('    <sourcefile name="'+file_name+'">\n')
            if i.getcovStatus() !="Not Applicable":
                jfile.write('      <counter type="'+i.getcovType()+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('      <counter type="'+i.getcovType()+'" missed="0" covered="0"/>\n')
                
            if i.getcovType() =='Modified Condition / Decision Coverage':
                jfile.write('    </sourcefile>\n')            
        
        elif i.getcovElementType() == 'Procedure Coverage' and flag_proc ==3:
            flag_proc = 0
            flag_file = flag_file +  1 # In order to close the node for the file name 
            jfile.write('    <class name="'+file_name+'">\n')
            if i.getcovType() =='Statement Coverage':
                jfile.write('      <method name="'+i.getcovElementName()+'" desc="'+i.getcovStatus()+'" line="'+str(i.getcovLines())+'">\n')

            if i.getcovStatus() !="Not Applicable":
                jfile.write('        <counter type="'+i.getcovType()+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('      <counter type="'+i.getcovType()+'" missed="0" covered="0"/>\n')
                
        elif i.getcovElementType() == 'Procedure Coverage' and flag_proc ==0:
            flag_proc = 0
            flag_file = flag_file +  1 # In order to close the node for the file name
            if i.getcovType() =='Statement Coverage':
                jfile.write('      <method name="'+i.getcovElementName()+'" desc="'+i.getcovStatus()+'" line="'+str(i.getcovLines())+'">\n')
            if i.getcovStatus() !="Not Applicable":
                jfile.write('        <counter type="'+i.getcovType()+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('        <counter type="'+i.getcovType()+'" missed="0" covered="0"/>\n')
            
            if i.getcovType() =='Modified Condition / Decision Coverage':
                jfile.write('      </method>\n')
        
        elif  i.getcovElementType() == 'File Coverage' and flag_file >=3:
            flag_file =0
            file_name = i.getcovElementName()
            if i.getcovType() =='Statement Coverage':
                
                jfile.write('    </class>\n')
                jfile.write('    <sourcefile name="'+file_name+'">\n')
      
            if i.getcovStatus() !="Not Applicable":
                jfile.write('      <counter type="'+i.getcovType()+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('      <counter type="'+i.getcovType()+'" missed="0" covered="0"/>\n')
    jfile.write('  </package>\n')
    jfile.write('</report>')        
def dynamicJsonFormatter():
    dictionary = {}
    ls=[]
    with open(workarearoot+tcfName[-17:-4]+"_dyn.json", mode='a') as jfile:
        for i in range (0, len(file_coverage)):
            dictionary[file_coverage[i].getcovElementName()] = file_coverage[i].printCoverageElement
            ls.append(dictionary)
        json_object = json.dumps(dictionary, indent = 4, sort_keys = False)
        jfile.write(json_object)
        
def xmltojson (xml_name,json_name):
    xmlfile=open(xml_name,'r')
    obj= xmltodict.parse(xmlfile.read())
    
    jsonfile=open(json_name,'w')
    
    jsonfile.write(json.dumps(obj))
    print('Json file is written in to :\n'+json_name)
    jsonfile.close()    
    
def junit_creator():
    test_case=[]
    ts =[]
    for i in range (0, len(file_coverage)):
        if (file_coverage[i].getcovLines() != "Not Applicable"):
            test_case.append(TestCase (file_coverage[i].getcovElementType(), file_coverage[i].getcovElementName(), int(file_coverage[i].getcovLines()), file_coverage[i].getcovType() ,file_coverage[i].getcocombCov()))
        else : 
            test_case.append(TestCase (file_coverage[i].getcovElementType(), file_coverage[i].getcovElementName() ,0, file_coverage[i].getcovType() ,''))
        ts = [TestSuite(tcfName[-17:-4],test_case)]
   
    with open(workarearoot+tcfName[-17:-4]+'_dyn.junit', mode='a') as f:
        TestSuite.to_file(f, ts)       
                        
    print ("Junit file : "+ workarearoot + tcfName[-17:-4]+'_dyn.junit is written successfully ')


                        
                
        
        
        
        
if __name__ == "__main__":
    main()
