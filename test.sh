#!/bin/bash

#Bash script for testing UI project at netelastic

npm test
clear
python3 cleanUpLogs.py
env DEBUG="*" node whiteBoxTest.js &> whiteBoxResults.log
egrep '***Test.+?stackTrace' whiteBoxResults.log | xargs -0 python3 whiteBoxParse.py
python3 parseTestingJson.py
