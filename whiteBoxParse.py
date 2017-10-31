import re
import sys

#USE THIS FILE TO SAVE GREP RESULTS INTO A FILE

data = sys.argv[1]


testResults = re.findall(r'\s*\w+:\s+(?:passed|failed)',data) #list(set())

#print(testResults)

testSummaryRe = re.findall(r'Summary\:(.+)Test .+?\:',data)
tempHolder = testSummaryRe[0]

testSummary = re.findall(r'\s*[^\\\n]+:\s+(?:[^\\\n]+)',tempHolder)
testSummary = [e[2:len(e)] for e in testSummary]


if testSummary:
    with open('parsedWhiteBox', 'w') as file:
        file.write('Summary Test\n')
        for results in testSummary:
            results += '\n'
            file.write(results)




def whiteSpaceCounter(word):
    return len(word) - len(word.lstrip(' '))

first = testResults[0]


#print('PRINTING TEST RESULTS')
with open('parsedWhiteBox', 'a') as file:
    firstRun = True
    file.write('Which Test\n')
    for results in testResults:
        if results == first and not firstRun:
            break
        firstRun = False
        if results[0].islower():
            results = results[1:len(results)]
        results += '\n'
        file.write(results)