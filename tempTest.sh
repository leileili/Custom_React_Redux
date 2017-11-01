#!/bin/bash
#for debugging


env DEBUG="*" node whiteBoxTest.js &> whiteBoxResults.log
egrep '***Test.+?stackTrace' whiteBoxResults.log | xargs -0 python3 whiteBoxParse.py 
