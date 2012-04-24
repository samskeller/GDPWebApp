''' createInsertStatements.py

    Justin Norden, Cole Stephan, Sam Keller

    A script for converting some GDP data into SQL for use in MySQL.
'''

import sys
import csv

makeTables = '''DROP TABLE IF EXISTS gdpData;
CREATE TABLE gdpData (
  fip text,
  industryString text,
  yearString text,
  gdpString text
);

'''
print makeTables

reader = csv.reader(open(sys.argv[1]))
titleRow = reader.next()[4:]

states = {}
for row in reader:
    row = map(str.strip, row)
    # this got rid of our information on sub industries (spaces indicated a sub ind)
    states[row[0],row[2]] = row[1:]


overallStates = []

for state in states:
    for k in range(len(titleRow)):
        fip = state[0]
        stateRow = states[state]
        stateName = stateRow[0]
        yearString = titleRow[k]
        gdpString = stateRow[k+3]
        industryString = stateRow[2]
        queryGDPData = "INSERT INTO gdpData (fip, industryString, yearString, gdpString)"
        queryGDPData +=   " VALUES ('%s', '%s', '%s', '%s');" % (fip, industryString, yearString, gdpString)
        print queryGDPData