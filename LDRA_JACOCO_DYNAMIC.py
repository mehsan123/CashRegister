
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
    coverage_calculator()
    
    
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
    fileName_with_path = []
    fileName = []
    for r, d, f in os.walk(workarearoot):
        for item in f:
            if item.endswith(format):
                if item != "contents.ldra":
                    print("Found "+format+" File",item)
                    fileNamePath = str(os.path.join(r,item))
                    fileName_with_path.append(fileNamePath)
                    fileName.append(item)
    if len(fileName_with_path) ==0 :
        print("No "+format+" file has been found!")
        
    else:
        for i in fileName_with_path:
            print("fileName",i)
    return (fileName_with_path, fileName)

            
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
    fileName,file_just_name = findFiles(workarearoot,'.ldra')
    count = 0
    #Generating XML for Code Coverage
    for i in fileName:
        count = count + 1
        xml_file=i[:-5]+'_coverage.xml'
        
        command6 = '{}integration_util.exe /arg=0 /1={} /2={} '.format(toolsuiteroot,xml_file, i)
        os.system(command6)
        
        xml=sendXml(xml_file)
        file_coverage = parseXml(xml)
        jacocoFile=i[:-5]+'_jacoco_coverage.xml'
        coberturaFile = i[:-5]+'_cobertura.xml'
        jacocoWriter(jacocoFile)
        coberturaGenerator(coberturaFile,file_just_name[count-1][:-5])

    
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
                        print('Procedure Coverage'+obj.get('source'))
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
    jfile.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    #jfile.write('<!DOCTYPE report PUBLIC "-//JACOCO//DTD Report 1.0//EN" "report.dtd">\n')
    jfile.write('<report name="'+jacocoFile[:-20]+'">\n')
    jfile.write('  <sessioninfo id="unknownhost-TBD" start="0000000000000" dump="0000000000000"/>\n')
    jfile.write('  <package name="'+jacocoFile[:-20]+'">\n')
    flag_file = 0
    flag_proc =0
    print(file_coverage)
    coverage_array=[]
    count = 0
    for i in file_coverage:
        if i.getcovType() == 'Statement Coverage':
            coverage_array.append('LINE')
        elif i.getcovType() == 'Branch/Decision Coverage':
            coverage_array.append('BRANCH')
        elif i.getcovType() == 'Modified Condition / Decision Coverage':
            coverage_array.append('COMPLEXITY')
        elif  i.getcovType() == 'Not Applicable' :
            print('?????')
        else: 
            print('Not Found')
    for i in file_coverage:
    
        count = count + 1
        
        if i.getcovElementType() == 'File Coverage' and flag_file ==0:
            flag_file = 0
            flag_proc = flag_proc+1
            file_name = i.getcovElementName()
            if i.getcovType() =='Statement Coverage':
                jfile.write('    <sourcefile name="'+file_name+'">\n')
            if i.getcovStatus() !="Not Applicable":
                jfile.write('      <counter type="'+coverage_array[count-1]+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('      <counter type="'+coverage_array[count-1]+'" missed="0" covered="0"/>\n')
                
            if i.getcovType() =='Modified Condition / Decision Coverage':
                jfile.write('    </sourcefile>\n')            
        
        elif i.getcovElementType() == 'Procedure Coverage' and flag_proc ==3:
            flag_proc = 0
            flag_file = flag_file +  1 # In order to close the node for the file name 
            jfile.write('    <class name="'+file_name+'">\n')
            if i.getcovType() =='Statement Coverage':
                jfile.write('      <method name="'+i.getcovElementName()+'" desc="'+coverage_array[count-1]+'" line="'+str(i.getcovLines())+'">\n')

            if i.getcovStatus() !="Not Applicable":
                jfile.write('        <counter type="'+coverage_array[count-1]+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('      <counter type="'+coverage_array[count-1]+'" missed="0" covered="0"/>\n')
                
        elif i.getcovElementType() == 'Procedure Coverage' and flag_proc ==0:
            flag_proc = 0
            flag_file = flag_file +  1 # In order to close the node for the file name
            if i.getcovType() =='Statement Coverage':
                jfile.write('      <method name="'+i.getcovElementName()+'" desc="'+coverage_array[count-1]+'" line="'+str(i.getcovLines())+'">\n')
            if i.getcovStatus() !="Not Applicable":
                jfile.write('        <counter type="'+coverage_array[count-1]+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('        <counter type="'+coverage_array[count-1]+'" missed="0" covered="0"/>\n')
            
            if i.getcovType() =='Modified Condition / Decision Coverage':
                jfile.write('      </method>\n')
        
        elif  i.getcovElementType() == 'File Coverage' and flag_file >=3:
            flag_file =0
            file_name = i.getcovElementName()
            if i.getcovType() =='Statement Coverage':
                
                jfile.write('    </class>\n')
                jfile.write('    <sourcefile name="'+file_name+'">\n')
      
            if i.getcovStatus() !="Not Applicable":
                jfile.write('      <counter type="'+coverage_array[count]+'" missed="'+str(i.getreqCov())+'" covered="'+str(i.getcovLines())+'"/>\n')
            else:
                jfile.write('      <counter type="'+coverage_array[count]+'" missed="0" covered="0"/>\n')
    jfile.write('  </package>\n')
    jfile.write('</report>')        

def coverage_calculator():
    file_match = 0
    file_name =""
    files_name=[]
    
    statement_count = 0
    statement_accum = 0
    branch_accum = 0
    branch_count =0
    mcdc_count = 0
    mcdc_accum = 0
    total_statement = 0
    total_branch =0
    total_mcdc =0
    
    function_statement_count = 0
    function_statement_accum = 0
    function_branch_accum = 0
    function_branch_count =0
    function_mcdc_count = 0
    function_mcdc_accum = 0
    function_total_statement = 0
    function_total_branch =0
    function_total_mcdc =0
    
    function_total_branch_percentage=0
    function_total_mcdc_percentage=0
    total_statement_percentage = 0
    total_branch_percentage =0
    function_total_statement_percentage=0
    total_mcdc_percentage=0
    no_lines_valid=0
    no_lines_covered=0
    function_no_lines_valid=0
    function_no_lines_covered=0
    
    overal_coverage=[]
    for i in file_coverage:
        if i.getcovElementType() == 'File Coverage':
            if i.getcovType() == 'Statement Coverage':
                if i.getcurCov() != 'Not Applicable':
                    statement_accum = statement_accum + int(i.getcurCov())
                    #print(statement_accum)
                    statement_count = statement_count+1
                    no_lines_valid = int(no_lines_valid) + int(i.getcovLines())
                    
            if i.getcovType() == 'Branch/Decision Coverage':        
                if i.getcurCov() != 'Not Applicable':
                    branch_accum = int(branch_accum) + int(i.getcurCov())
                    branch_count= branch_count+1
                    
            if i.getcovType() == 'Modified Condition / Decision Coverage':        
                if i.getcurCov() != 'Not Applicable':
                    mcdc_accum = int(mcdc_accum) + int(i.getcurCov())
                    mcdc_count= mcdc_count+1
                    
  
        if i.getcovElementType() == 'Procedure Coverage':
            if i.getcovType() == 'Statement Coverage':
                if i.getcurCov() != 'Not Applicable':
                    function_statement_accum = int(function_statement_accum) + int(i.getcurCov())
                    #print(statement_accum)
                    function_statement_count = function_statement_count+1
                    function_no_lines_valid = int(function_no_lines_valid) + int(i.getcovLines())
                
            if i.getcovType() == 'Branch/Decision Coverage':        
                if i.getcurCov() != 'Not Applicable':
                    function_branch_accum = function_branch_accum + int(i.getcurCov())
                    function_branch_count= function_branch_count+1
            
            if i.getcovType() == 'Modified Condition / Decision Coverage':        
                if i.getcurCov() != 'Not Applicable':
                    function_mcdc_accum = function_mcdc_accum + int(i.getcurCov())
                    function_mcdc_count= function_branch_count+1
    
    if statement_count !=0:
        total_statement_percentage = statement_accum / statement_count
        no_lines_covered = int(no_lines_valid) * total_statement_percentage
        
    if function_statement_count !=0:
        function_total_statement_percentage= function_statement_accum / function_statement_count
        function_no_lines_covered = int(function_no_lines_valid)* function_total_statement_percentage
    
    print("Percentage Statement Coverage is:",str(total_statement))
    print("Percentage function_Statement Coverage is:",str(function_total_statement))
    
    if branch_count !=0:
        total_branch_percentage = branch_accum / branch_count
    
    if function_branch_count !=0:
        function_total_branch_percentage = function_branch_accum / function_branch_count
        
    print("Percentage Branch Coverage is:",str(total_branch))   
    print("Percentage function_Branch Coverage is:",str(function_total_branch))   
    
    if mcdc_count !=0:
        total_mcdc_percentage = mcdc_accum/ mcdc_count
    
    if function_mcdc_count !=0:
        function_total_mcdc_percentage = function_mcdc_accum/ function_mcdc_count
    
    print("Percentage MCDC Coverage is:",str(total_mcdc))
    print("Percentage function_MCDC Coverage is:",str(total_mcdc))
    
    overal_coverage = [total_statement_percentage,total_branch_percentage,total_mcdc_percentage,function_total_statement_percentage,function_total_branch_percentage,function_total_mcdc_percentage,no_lines_valid, function_no_lines_valid, no_lines_covered, function_no_lines_covered]
    
    return (overal_coverage)


def getCovYouNeed(elementName, coverageType):
    for i in file_coverage:
        if i.getcovElementName() == elementName :
            if i.getcovType() == coverageType:
                return (i)
               


def coberturaGenerator(coberturaFile, ProjectName):
    overal_coverage = coverage_calculator()
    print(overal_coverage)
    print(str(overal_coverage[0]))
    flag_file = 0
    flag_proc = 0
  
    file_name=''
    cfile= open(coberturaFile,mode='w')
    cfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    cfile.write('<!DOCTYPE coverage SYSTEM "http://cobertura.sourceforge.net/xml/coverage-04.dtd">\n')
    cfile.write ('<coverage lines-valid="'+ str(overal_coverage[6]))
    cfile.write ('"  lines-covered="' + str(overal_coverage[8]))
    cfile.write('"  line-rate="'+ str(overal_coverage[0]))
    cfile.write('"  branches-valid="'+str(overal_coverage[7]))
    cfile.write('"  branches-covered="'+str(overal_coverage[9]))
    cfile.write('"  branch-rate="'+ str(overal_coverage[1]))
    cfile.write('"  timestamp="1234"')
    cfile.write('  complexity="1.0"')
    cfile.write('  version="0.1">\n')
    cfile.write('<sources>\n')
    cfile.write('	<source>'+ProjectName+'</source>\n')
    cfile.write('</sources>\n')
    
    #writing Packages in C we gonna have one Package called Project.LDRA
    
    cfile.write('<packages>\n')
    cfile.write('	<package name="'+ProjectName)
    cfile.write('"  line-rate="'+str(overal_coverage[0]))
    cfile.write('"  branch-rate="'+str(overal_coverage[1]))
    cfile.write('"  complexity="0"')
    
    cfile.write(' >\n')

    #writing classes in cobertura which is equivalent as file name
    for i in file_coverage:
        if (i.getcovElementType() == 'File Coverage' and flag_file ==0 and i.getcovType() == 'Statement Coverage'):
            cfile.write('	<classes>\n')        
            flag_file = 1
            flag_proc=0
            cfile.write('	<class name="')
            cfile.write(i.getcovElementName())
            cfile.write('"  filename="')
            cfile.write(i.getcovElementName())
            cfile.write('"  complexity="0"')
            cfile.write('  line-rate="')
            cfile.write(str(i.getcocombCov()))
            cfile.write('"  branch-rate="')
            branch= getCovYouNeed(i.getcovElementName(),'Branch/Decision Coverage')
                
            if branch.getcocombCov() == "Not Applicable":
                cfile.write("N/A")
            else:
                cfile.write(str(branch.getcocombCov()))
            cfile.write('" >\n')
            

         
        elif (i.getcovElementType() == 'Procedure Coverage' and flag_proc== 0 and i.getcovType() == 'Statement Coverage' and i.getcovStatus() !="Not Applicable"):
            flag_proc = 1
            cfile.write('		<methods>\n')
            cfile.write('			<method name="'+ i.getcovElementName()+'"  signature="()V"  line-rate="'+i.getcocombCov())
            cfile.write('"  branch-rate="')
            branch= getCovYouNeed(i.getcovElementName(),'Branch/Decision Coverage')
            
            if branch.getcocombCov() == "Not Applicable":
                cfile.write('N/A')
            else:
                cfile.write(str(branch.getcocombCov()))
                
            cfile.write('"  complexity="0" >\n')
            cfile.write('                <lines><line number="'+i.getcovLines()+'"  hits="1" /></lines>\n')
            cfile.write('            </method>\n')

        
        
        elif(i.getcovElementType() == 'Procedure Coverage' and flag_proc== 1 and i.getcovType() == 'Statement Coverage' and i.getcovStatus() !="Not Applicable"):
            cfile.write('			<method name="'+ i.getcovElementName()+'" signature="()V"  line-rate="'+i.getcocombCov())
            cfile.write('"  branch-rate="')
            branch= getCovYouNeed(i.getcovElementName(),'Branch/Decision Coverage')
            if branch.getcocombCov() == "Not Applicable":
                cfile.write('N/A')
            else:
                cfile.write(str(branch.getcocombCov()))
            cfile.write('"  complexity="0" >\n')
            cfile.write('                <lines><line number="'+i.getcovLines()+'" hits="1" /></lines>\n')
            cfile.write('            </method>\n')            
        
        elif (i.getcovElementType() == 'File Coverage' and flag_file ==1 and i.getcovType() == 'Statement Coverage'):
            cfile.write('		</methods>\n')        
            cfile.write('       <lines></lines>\n')
            cfile.write('    </class>\n')         
            flag_proc=0
            cfile.write('	<class name="')
            cfile.write(i.getcovElementName())
            cfile.write('" filename="')
            cfile.write(i.getcovElementName())
            cfile.write('"  complexity="0"')
            cfile.write('  line-rate="')
            cfile.write(i.getcocombCov())
            cfile.write('"  branch-rate="')
            branch= getCovYouNeed(i.getcovElementName(),'Branch/Decision Coverage')
            if branch.getcocombCov() == "Not Applicable":
                cfile.write('N/A"')
            else:
                cfile.write(str(branch.getcocombCov()))
            cfile.write('" >\n')

    cfile.write('		</methods>\n')
    cfile.write('       <lines></lines>\n')
    cfile.write('    </class>\n')
            
    cfile.write('    </classes>\n')
    cfile.write('    </package>\n')
    cfile.write('</packages>\n')
    cfile.write('</coverage>\n')
        
            
            
            



    flag_file = 0
    flag_proc =0
    
    print(file_coverage)
    for i in file_coverage:
        if i.getcovElementType == 'filecoverage':
            print("Non")
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

    
