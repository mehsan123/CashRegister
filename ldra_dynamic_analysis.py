
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
    SourceMatches = []
    HeaderMatches =[]
    tcfName=''
    if len(sys.argv) < 4:
        print('Please pass the Source Directory Parameter')
        print('The second parameter is the toolsuite path. contestbed and contbbuild import should be in this folder')
        print('The third parameter is the folder you want to store the analysis results')
        print('The Fourth parameter is the Project Directory')
        print('')
        sys.exit(0)
        
    #run through all steps
    init()
    SourceMatches = findAllSourceCode(SourceMatches)
    tcfName = createTCF(SourceMatches, HeaderMatches)
    print("TCF Name is:" + tcfName)
    runanalysis(tcfName)
    parseXml(tcfName)
    #dynamicJsonFormatter(tcfName)
    #xmltojson (WORKAREA+'Coverage.xml',WORKAREA+'coverage.json')
    #xmltojson (workarearoot+tcfName[-17:-4]+"_dyn.xml",workarearoot+tcfName[-17:-4]+'_dyn.json')
    #junit_creator(tcfName)
    #junit_creator()
    
    
######################################################################################
#  Function init 
# This function init initialize all the command line argument
######################################################################################
def init():
    global sourceRoot, toolsuiteroot, workarearoot, projectDir
    sourceRoot = sys.argv[1]+"\\"
    toolsuiteroot = sys.argv[2]+'\\'
    workarearoot = sys.argv[3]+'\\'
    projectDir =  sys.argv[4]+'\\'
    print('Source Root: '+sourceRoot)
    print('TOOLSUITE ROOT: ROOT: '+toolsuiteroot)
    print('WORKAREA ROOT: '+sourceRoot)
    print('Project Directory is:'+ projectDir)
    #from fourth argument locate directory for specified project
    if not os.path.exists(workarearoot):
        os.makedirs(workarearoot)
######################################################################################
#  Function findAllSourceCode 
# This function finds all the source codes that are in the format .c and .cpp 
######################################################################################
def findAllSourceCode(SourceMatches):
    for root, dirnames, filenames in os.walk(sourceRoot):
    
       
        for filename in fnmatch.filter(filenames, '*.c'):
            if('inszt_' not in filename):
                SourceMatches.append('      File = '+ os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, '*.cpp'):
            if('inszt_' not in filename):
                SourceMatches.append('      File = '+ os.path.join(root, filename))
    print ('The Number of Source code before filtering: '+str(len(SourceMatches)))
    return(SourceMatches)
    
######################################################################################
#  Function createPTF 
# This function will create a TCF file
######################################################################################
def createTCF(SourceMatches, HeaderMatches):
    tcfName= SystemTesting+'.tcf'
    f = open(sourceRoot+tcfName,'w+')
    f.write('# Begin Testbed  Set \n')
    f.write('\n   SET_TYPE = SYSTEM ')
    f.write('\n   SET_NAME = SystemTesting\n')
    f.write('\n   #Begin Source Files\n\n')
    f.write('\n'.join (SourceMatches))
    f.write('\n\n   # End Source Files\n')
    f.write('\n   # Begin Sysearch Include File Entries\n')
    f.write('\n'.join(HeaderMatches))
    #f.write('\nInsertInclude_203 = $(LDRA_CONFIG_ROOT)\LdraSystemHeaders.h\n')
    f.write('\n   # End Sysearch Include Files Entries\n')
    f.write('\n # End Testbed Set\n')
    f.write('\n# Begin Options')
    f.write('\n   open_all_includes = True')
    #f.write('   sysearch = F:\\LDRA\\sysearch_system.dat')
    f.write('\n   include = True')
    f.write('\n# End Options')

    f.close()
    return tcfName


        
#################
#  Function runanalysis 
# This function runs all the four phases of the static analysis
######################################################################################
def runanalysis(tcfName):
    #print('Static Analysis is started for: '++prjpath+'\\'+prjname)
    #cppcodestandard = '''"Name of Stanadrd"'''
    #ccodestandard = '''"Name of Standard for c code"'''
    
    #/112n34q run all phases of static analysis
    #-reanalyse_changed_set analyzes set if file has added/removed from set
    #-continue_system_analysis continues analysis even if a file fails analysis
    #-generate_code_review=HTML force generation of HTML code review report.
    os.system('dir')
    command1=sourceRoot+'Clean.bat '+sourceRoot
    os.system(command1)
    
    command2 = '{}contestbed.exe {} /112n34021q -reanalyse_changed_set -generate_code_review=HTML -tb_workfiledir={} -build_cmd="Build.bat" -startin_dir={} -auto_macro -auto_macro_value="0" -exhdir={}'.format(toolsuiteroot,tcfName, workarearoot, sourceRoot, projectDir) #pass ptf as parameter
    os.system(command2)
    
    command4=sourceRoot+'Build.bat '+sourceRoot 
    os.system(command4)
    

    #command5=(sourceRoot+'Cashregister.exe ')
    #os.system(command5)
    
    command5=(sourceRoot+'Cashregister.exe < HLR_Input_Add_Products.txt')
    os.system(command5)
    
    
    command6 = '{}integration_util.exe /arg=3 /1={}Result.xml /2={} /3='.format(toolsuiteroot,workarearoot, workarearoot+tcfName[-17:-4]+'.ldra')
    os.system(command6)
    #Dynamic Analysis
    print('TCF Name is: '+tcfName)
    print('Project Directory is: '+projectDir)
    
    
    command7 = '{}contestbed.exe {} /32faya  -tb_workfiledir={} -exhdir={} '.format(toolsuiteroot,tcfName, workarearoot, projectDir) #pass ptf as parameter
    
    os.system(command7)
    
    
    print('TCF Name is:'+tcfName[len(tcfName):-4])
    command8 = '{}integration_util.exe /arg=0 /1={}{}.xml /2={} '.format(toolsuiteroot,workarearoot,tcfName[-17:-4]+'_dyn',workarearoot+tcfName[-17:-4]+'.ldra')
    os.system(command8)

def parseXml(tcfName):
    
    
    xml_file = ET.parse(workarearoot+tcfName[-17:-4]+'_dyn.xml')
    print("XML file : "+str(xml_file)+ " is now open")
    root = xml_file.getroot()
    
    for node in root.findall("files"):
        for obj in node:
            if(obj.tag == 'file'):
                print(obj.tag)
                for file in obj:
                    if(file.tag == 'filecoverage'):
                        if (file.get('description') is None):
                        
                            file_coverage.append(CoverageElement('File',obj.get('source'),file.get('type'), file.get('lines'),file.get('prevpcnt'), file.get('currpcnt'), file.get('combinedpcnt'), file.get('requiredpcnt'), file.get('status')))
                        else:
                            file_coverage.append(CoverageElement('File',obj.get('source'),file.get('type'), "Not Applicable","Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable"))
                    elif (file.tag =='function'):
                        for coverage in file :
                            if(coverage.get('description')  is None ):
                                file_coverage.append(CoverageElement('Procedure',file.get('name'),coverage.get('type'), coverage.get('lines'),coverage.get('prevpcnt'), coverage.get('currpcnt'), coverage.get('combinedpcnt'), coverage.get('requiredpcnt'), coverage.get('status')))
                            else:
                                file_coverage.append(CoverageElement('Procedure',file.get('name'),coverage.get('type'), "Not Applicable","Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable", "Not Applicable"))
                    else:
                        print("-----------------Not file coverage nor function coverage------------------")

def dynamicJsonFormatter(tcfName):
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
    
def junit_creator(tcfName):
    test_case=[]
    ts =[]
    for i in range (0, len(file_coverage)):
        if (file_coverage[i].getcovLines() is not "Not Applicable"):
            test_case.append(TestCase (file_coverage[i].getcovElementType(), file_coverage[i].getcovElementName(), int(file_coverage[i].getcovLines()), file_coverage[i].getcovType() ,file_coverage[i].getcocombCov()))
        else : 
            test_case.append(TestCase (file_coverage[i].getcovElementType(), file_coverage[i].getcovElementName() ,0, file_coverage[i].getcovType() ,''))
        ts = [TestSuite(tcfName[-17:-4],test_case)]
   
    with open(workarearoot+tcfName[-17:-4]+'_dyn.junit', mode='a') as f:
        TestSuite.to_file(f, ts)       
                        
    print ("Junit file : "+ workarearoot + tcfName[-17:-4]+'_dyn.junit is written successfully ')


                        
                
        
        
if __name__ == "__main__":
    main()
