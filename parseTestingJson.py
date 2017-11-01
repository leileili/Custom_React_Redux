#!/usr/bin/python3

import json
import re
import xml.etree.ElementTree as etree

def findLongestWord(wordList):
    longest = 0
    which = 0
    for counter in range(0, len(wordList)):
        if len(wordList[counter]) > longest:
            which = counter
            longest = len(wordList[counter])
    #print(wordList[which])
    return longest


def returnLinesWithExtraPadding(extraPadding, fileNamePadding = 0):
    return '|------'+'-' * (extraPadding+fileNamePadding) + '-------------------------------------------------|\n'

data = {}
suiteData = []

with open('testLog.json') as json_data:
    data = json.load(json_data)
    data.pop('coverageMap', None)
    suiteData = data['testResults']

tree = etree.parse('coverageOutput/clover.xml')
attrbChecked = False
fileNameChecked = False
firstTimeRan = True
fileName = ''
fileList = []
fileCoveredResults = []
obj = {}
packageMetrics = False

for element in tree.iter():
    #print(element.tag)
    if re.match(r'coverage|line|project', element.tag ):
        continue
    if firstTimeRan:
        fileName = 'Total'
        firstTimeRan = False
    if element.tag == 'package':
        packageMetrics = True
    if element.tag == 'metrics':
        if packageMetrics:
            packageMetrics = False
            continue
        obj = element.attrib
    if element.tag == 'file':
        fileName = element.attrib['name']
    if fileName is not '' and obj is not None:
        fileCoveredResults.append({fileName: obj})
        fileList.append(fileName)
        fileName = ''
        obj = None

resultsCoverage = ''
coveragePadding = findLongestWord(fileList)
coverageHeader = '| File Name            covered:    |   statments   |    conditionals   |   methods   |\n'
resultsCoverage += returnLinesWithExtraPadding(coveragePadding, 4)
resultsCoverage += coverageHeader;
resultsCoverage += returnLinesWithExtraPadding(coveragePadding, 4)

### formating of the code coverage line by line

for file in fileCoveredResults:
    for fName, details in file.items():
        coveredStatments = int(details['coveredstatements'])
        statements = int(details['statements'])
        coveredConditionals = int(details['coveredconditionals'])
        conditionals = int(details['conditionals'])
        coveredMethods = int(details['coveredmethods'])
        methods = int(details['methods'])

        statementsResults = ''
        conditionalResults = ''
        methodResults = ''

        sPad = 0
        cPad = 0
        mPad = 0

        if coveredStatments == 0 or statements == 0:
            statementsResults = '00.0'
        else:
            statementsResults = str(round((int(details['coveredstatements'])/int(details['statements'])*100),1))
            if len(statementsResults)==3:
                sPad = '0'
                sPad += statementsResults
                statementsResults = sPad
            elif len(statementsResults)==5:
                statementsResults = ' 100'


        if coveredConditionals == 0 or conditionals == 0:
            conditionalResults = '00.0'
        else:
            conditionalResults = str(round((int(details['coveredconditionals'])/int(details['conditionals'])*100),1))
            if len(conditionalResults)==3:
                cPad = '0'
                cPad += conditionalResults
                conditionalResults = cPad
            elif len(conditionalResults)==5:
                conditionalResults = ' 100'


        if coveredMethods == 0 or methods == 0:
            methodResults = '00.0'
        else:
            methodResults = str(round((int(details['coveredmethods'])/int(details['methods'])*100),1))
            if len(methodResults)==3:
                mPad = '0'
                mPad += methodResults
                methodResults = mPad
            elif len(methodResults)==5:
                methodResults = ' 100'

        resultsCoverage += '| ' + fName + '              ' + (' ' * (coveragePadding-len(fName))) +  statementsResults + '%            ' +  conditionalResults + '%           ' + methodResults + '%      |\n'


resultsCoverage += returnLinesWithExtraPadding(coveragePadding, 4)

schema = []
fileNames = []

### get the names of the schemes to render etc...
for test in suiteData:
    fileNames.append(re.match(r'.+(?:\\|\/)(.*\.js)$', test['name']).group(1))
    for result in test['assertionResults']:
        resultRender = re.match(r'Checking to see if (.+?) renders successfully', result['title'])
        resultInnerCom = re.match(r'Checking to see if (.+?) has the correct component built (.+?) in', result['title'])
        resultTableLength = re.match(r'Checking if Table \w+ (has Columns length of \d+)', result['title'])
        if resultRender:
            schema.append(resultRender.group(1))
        elif resultInnerCom:
            schema.append(resultInnerCom.group(2))
        elif resultTableLength:
            schema.append(resultTableLength.group(1))



results = ''
extraPadding = findLongestWord(schema)
fileNamePadding = findLongestWord(fileNames)

numTotTestCheck = data['numTotalTests']
numFailedTestCheck = data['numFailedTests']
numTotalTestCheck = data['numTotalTests']

testResults = 0

if numTotTestCheck != 0 or numFailedTestCheck != 0 or numTotalTestCheck != 0:
    testResults = str(round(((data['numTotalTests']-data['numFailedTests'])/data['numTotalTests'])*100,2))


lines = returnLinesWithExtraPadding(extraPadding+4)
atFirstGlance = '| At First Glance                                                                    |\n'
totalTime = '| Time Elapsed: '+ str(data['startTime']) +'                                                        |\n'
failedTest= '| Number of Failed Test: '+ str(data['numFailedTests']) +'                                                          |\n'
passedTest = '| Number of Passed Test: '+ str(data['numPassedTests']) + '   '+ ' ' * (1 - len(str(data['numPassedTests']))) + '                                                      |\n'
totalTest = '| Total Test: '+ str(data['numTotalTests']) +' across '+ str(data['numTotalTestSuites']) +' suites giving us a '+ testResults  +'% pass rate '+ ' '*(1-len(str(data['numTotalTests']))) + '                      |\n'

results += lines
results += atFirstGlance
results += totalTime
results += failedTest
results += passedTest
results += totalTest

schemaBodyResults = ''
seen = []


for test in suiteData:
    if len(test['assertionResults']) is 0:
        continue
    fileName = re.match(r'.+(?:\\|\/)(.*\.js)$', test['name']).group(1)
    schemaHeader = '| Schema ' + '| ' +fileName + ' ' * (extraPadding+fileNamePadding-len(fileName)) + '                    Pass/Fail      |\n'
    results += lines
    results += schemaHeader
    results += lines
    for result in test['assertionResults']:
        tempName = re.match(r'Checking to see if (?:Table )?(.+?) renders successfully', result['title'])
        tempName2 = re.match(r'Checking to see if (.+?) has the correct component (.+?) built in', result['title'])
        tempName3 = re.match(r'Checking if Table \w+ (has Columns length of \d+)', result['title'])
        if tempName:
            tempLine = '| ' + tempName.group(1) + ' ' * (extraPadding+fileNamePadding - len(tempName.group(1))) + '                               ' + result['status'] +'       |\n'
            seen = []
            results += tempLine
        elif tempName2 and not tempName2.group(2) in seen:
            tempLine = '|   * ' + tempName2.group(2) + ' ' * (extraPadding+fileNamePadding - len(tempName2.group(2))) + '                           ' + result['status'] +'       |\n'
            seen.append(tempName2.group(2))
            results += tempLine
        elif tempName3 and not tempName3.group(1) in seen:
            tempLine = '|   * ' + tempName3.group(1) + ' ' * (extraPadding+fileNamePadding - len(tempName3.group(1))) + '                           ' + result['status'] +'       |\n'
            seen.append(tempName3.group(1))
            results += tempLine

results += lines


##################### WHTIE BOX TEST ###################

whiteBoxData = []


# padding 1 is always required
def buildResults(header, body, padding1=0, padding2=0):
    resultsCoverage = ''
    lines = returnLinesWithExtraPadding(padding1, padding2)
    resultsCoverage += lines
    resultsCoverage += header
    resultsCoverage += lines
    resultsCoverage += body
    resultsCoverage += lines
    return resultsCoverage

def whiteSpaceCounter(word):
    return len(word) - len(word.lstrip(' '))

def replaceWhiteSpace(word,space):
    howManyTimes = space % 4
    appendToMe = ''
    end = '> '
    for counter in range(0,space):
        appendToMe += '-'
    appendToMe += end
    appendToMe += str(word)
    return appendToMe

with open('parsedWhiteBox') as file:
    whiteBoxData = file.read()

bodyOutput = ''
whichTestData = re.match(r'.+?Which Test(.+)', whiteBoxData, re.DOTALL).group(1)
whichTestArr = whichTestData.split('\n')

whichSummaryData = re.match(r'Summary Test\n(.+?)Which Test', whiteBoxData, re.DOTALL).group(1)
whichSummaryArr = whichSummaryData.split('\n')

whiteBoxData = whiteBoxData.split('\n')
padding = findLongestWord(whiteBoxData)


def checkSpecialCase(case):
    words = case.split(':')
    return (len(words[0]),len(words[1])-1)

#Summary test
for line in whichSummaryArr:
    if line == '':
        break
    space = whiteSpaceCounter(line)
    word = ''
    if re.match(r'\s*(.+:\s*\w+)',line, re.DOTALL):
        result = re.match(r'\s*(.+:\s*\w+)',line, re.DOTALL)
        word = replaceWhiteSpace(result.group(1), space)
        paddingStuff = checkSpecialCase(result.group(1))
        if space == 0:
            temp = '| ' + word + ' ' + ' ' * (padding-paddingStuff[0]-paddingStuff[1]) + '                                     |\n'
        else:
            temp = '| ' + word + ' ' + ' ' * (padding - paddingStuff[0] - paddingStuff[1]-space-2) + '                                  |\n'
        bodyOutput+=temp

bodyOutput +=  returnLinesWithExtraPadding(29, 0 )
bodyOutput += '| Detailed Results '+ ' '*65 + ' |\n'
bodyOutput +=  returnLinesWithExtraPadding(29, 0 )


#'Which test'
for line in whichTestArr:
    space = whiteSpaceCounter(line)
    word = ''
    if re.match(r'\s*(\w+:\s*\w+)',line):
        result = re.match(r'\s*(\w+:\s*\w+)', line)
        word = replaceWhiteSpace(result.group(1), space)
        paddingStuff = checkSpecialCase(result.group(1))
        if space == 0:
            temp = '| ' + word + ' ' + ' ' * (padding-paddingStuff[0]-paddingStuff[1]) + '                                     |\n'
        else:
            temp = '| ' + word + ' ' + ' ' * (padding - paddingStuff[0] - paddingStuff[1]-space-2) + '                                       |\n'
        bodyOutput+=temp

header = '| At First Glance                                                                    |\n'
whiteBoxResults = buildResults(header,bodyOutput, 29, 0)



###########OUTPUT RESULTS#####################
print()
print('                            PRINTING OUT CODE COVERAGE')
print(resultsCoverage)
print('                            PRINTING SCHEMA DRIVEN TEST')
print(results)
print('                            PRINTING WHITE BOX TESTING')
print(whiteBoxResults)