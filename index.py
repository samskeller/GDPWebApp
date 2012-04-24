#!/usr/bin/python
''' index.py

    Written by Justin Norden, Cole Stephan, and Sam Keller
    
    04/20/2012

    This code helps to display a webpage containing our online application for manipulation
    GDP data for the United States. This code was adapted from the code of Jeff Ondich.
    
    If the user wants to, he or she can click on the links to see our source code for the page
    as well as our datasource.py code, which has the class and methods that will extract our
    data from our data set. 
    
    The starting webpage only asks the user to identify what function they want to pick.
    Once they have picked a function, the Go button takes them to one of four templates where
    the user is prompted for more information. Once the user has specified more parameters
    to get whatever data they want, the Get Data button outputs the data from our database. 
'''

import cgi
import datasource
import HTMLCode
import cgitb
cgitb.enable()
import math

def sanitizeUserInput(s):
    '''Sanitizes the user's input and takes out any symbols '''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        s = s.replace(ch, '')
    return s

def chooseAndExecuteFunction(function, link1, link2, link3):
    '''This function runs a lot of our main code. This function is called every time we
    load any new page. If the user has just gotten to our main webpage, then function is 
    an empty string and we print out the functionTemplate.html file. If we've specified
    a function, though, we open the correc template and, if the user has selected parameters,
    we print out the resulting data.
    '''
    if function == 'getGDP':
        # User has selected the "Get GDP" function
        output = open('GDPTemplate.html').read() % (link1, link2, link3)
        print "Content-type: text/html\r\n\r\n"
        print output
        if len(form) == 5:
            retrieveAndPrintGDP()
        else:
            # The user either just got to the page or tried to manually change the form
            print 'Please enter the proper parameters'
    elif function == 'growthRate':
        # User has selected the "Growth Rate" function  
        output = open('GrowthTemplate.html').read() % (link1, link2, link3)
        print "Content-type: text/html\r\n\r\n"
        print output
        if len(form) == 5:
            calculateAndPrintGrowthRate()
        else:
            # The user either just got to the page or tried to manually change the form
            print 'Please enter the proper parameters'
    elif function == 'avgGDP':
        # User has selected the "Average GDP" function
        output = open('AVGTemplate.html').read() % (link1, link2, link3)
        print "Content-type: text/html\r\n\r\n"
        print output
        if len(form) == 5:
            calculateAndPrintAvgGDP()
        else:
            # The user either just got to the page or tried to manually change the form
            print 'Please enter the proper parameters'
    elif function == 'volatility':
        # User has selected the "Volatility" function
        output = open('VolatilityTemplate.html').read() % (link1, link2, link3)
        print "Content-type: text/html\r\n\r\n"
        print output
        if len(form) == 5:
            calculateAndPrintVolatility()
        else:
            # The user either just got to the page or tried to manually change the form
            print 'Please enter the proper parameters'
    else:
        # If no function has been chosen, we must be at the original page and
        # the user has to select a function
        output = open('functionTemplate.html').read() % (link1, link2, link3)
        print "Content-type: text/html\r\n\r\n"
        print output
        

def getFormData():
    '''Get the data about the industry, state, start year, and end year from the form'''
    industry = sanitizeUserInput(str(form['industry'].value))
    state = sanitizeUserInput(str(form['state'].value))
    startYear = sanitizeUserInput(str(form['StartYear'].value))
    endYear = sanitizeUserInput(str(form['EndYear'].value))
    return startYear,endYear,state,industry
    
def getYearInformation(startYear, endYear):
    '''getYearInformation simply take the startYear and endYear from the form and returns the
    number of years between the two as well as the start and end year. If the startYear is 
    after the endYear, we assume the user meant to switch the two and so the year range is 
    still the difference and we swap the start and end year. If the user doesn't enter a
    start year or end year, or if the user manually changes the form to enter incorrect parameters,
    we assume the largest possible year range.
    '''
    try:
        startYearInt = int(startYear)
        if int(startYear) < 1997 or int(startYear) > 2009:
            # If the user has manually changed the year to be a different number
            startYear = '1997'
    except ValueError:
        # Most likely the user hasn't selected a year and the year == 'default'
        startYear = '1997'
    try:
        endYearInt = int(endYear)
        if int(endYear) < 1997 or int(endYear) > 2009:
            endYear = '2009'
    except ValueError:
        endYear = '2009'
    if int(endYear) > int(startYear):
        yearRange = int(endYear) - int(startYear) + 1
    elif int(startYear) > int(endYear):
        # If the start year is greater than the end year, switch the years
        yearRange = int(startYear) - int(endYear) + 1
        startYear, endYear = endYear, startYear
    else:
        yearRange = 1
    return yearRange, startYear, endYear

def findVariablesGetData(function):
    '''This function is an efficient way to get all of the data from the form, calculate the
    end year and, if needed, change the years to proper values. Essentially this function returns
    the data requested as well as all of the parameters used to get that data'''
    # Get parameters from the form
    startYear,endYear,state,industry = getFormData()
    # Get the correct year data
    yearRange, startYear, endYear = getYearInformation(startYear, endYear)
    # Go to the datasource.py file and query the databasee with the right parameters
    # We use only the first two parts of the 'state' string since we store each state as the state's
    # fip number and then the name (eg 01Alabama). We only want the fip here to query the database
    data = datasource.queryDatabase(function, startYear, endYear, yearRange, state[:2], industry)
    return data, startYear, endYear, state, industry, yearRange
    

def buildTable(data, yearRange):
    ''' This function uses the data and the year range to build an html table out of the data
    where one column is the year and the other is the GDP'''
    tableOutput = HTMLCode.tableHeader
    for i in range(yearRange):
        # Make sure the years and GDPs are actual numbers
        assert data[i][0] == str(int(data[i][0]))
        assert data[i][1] == str(int(data[i][1]))
        # Build the table from our HTMLCode.py file
        table = HTMLCode.tableHTML % (data[i][0], data[i][1])
        tableOutput += table
    return tableOutput

def makeGraph(data):
    '''makeGraph builds the right data input to be used on the graphHTML html code from the
    file HTMLCode.py. It returns the full html code needed to make the graph'''
    dataListAsInts = []
    for i in data:
        # Add data, one point at a time, to the correct format
        oneDataPoint = [i[0], int(i[1])]
        dataListAsInts.append(oneDataPoint)
    dataListAsString = str(dataListAsInts)
    # Get the Google Developer code from HTMLCode.py and make the graph
    output = HTMLCode.graphHTML % (dataListAsString)
    return output

def retrieveAndPrintGDP():
    '''First retrieves the gdp data from the database and then prints the data'''
    data, startYear, endYear, state, industry, yearRange = findVariablesGetData('getGDP')
    if str(data) == '()':
        # Likely the user has tried to manually change the form. Let them know that they can't do that!
            print "You have entered incorrect parameters in the form. Please enter correct parameters."
    else:
        print '============== GDP Data =============='
        firstHeading = '<p> The state you picked was: %s <p>' % state[2:]
        secondHeading = '<p>The industry you picked was: %s <p>' % industry
        print firstHeading, secondHeading
        
        # Build the table
        table = buildTable(data, yearRange)
        print table
        
        # Make the graph
        graph = makeGraph(data)
        print graph

def calculateAndPrintGrowthRate():
    '''Calculates and prints the growth rates for a given state and start and end year. Queries
    the database to make this possible'''
    data, startYear, endYear, state, industry, yearRange = findVariablesGetData('growthRate')
    if str(data) == '()':
        # Likely the user has tried to manually change the form. Let them know that they can't do that!
            print "You have entered incorrect parameters in the form. Please enter correct parameters."
    else:
        # Make sure that the GDPs are actually numbers
        assert data[0][0] == str(int(data[0][0]))
        assert data[1][0] == str(int(data[1][0]))
        startYearGDP = int(data[0][0])
        endYearGDP = int(data[1][0])
        growthRate = (endYearGDP - startYearGDP) / float(startYearGDP) * 100
        
        print '============== GDP Growth Rate =============='
        firstHeading = '<p> The state you picked was: %s <p>' % state[2:]
        secondHeading = '<p>The industry you picked was: %s <p>' % industry
        print firstHeading, secondHeading
        
        # Get the header and build the table. We don't use the buildTable function here since
        # we aren't including information for years between the start and end year
        tableOutput = HTMLCode.tableHeader
        tableOutput += HTMLCode.tableHTML % (startYear, startYearGDP)
        tableOutput += HTMLCode.tableHTML % (endYear, endYearGDP)
        print tableOutput
        
        print '<p>The growth rate for your parameters is: ' + str(growthRate)[:4] + '%<p>'
    
def calculateAndPrintAvgGDP():
    '''Calculates and prints the average GDP for a given state and year range. We query the 
    database across all of those years and use a simple algorithm to find the average GDP'''
    data, startYear, endYear, state, industry, yearRange = findVariablesGetData('avgGDP')
    if str(data) == '()':
        # Likely the user has tried to manually change the form. Let them know that they can't do that!
        print "You have entered incorrect parameters in the form. Please enter correct parameters."
    else:
        print '============== Average GDP =============='
        firstHeading = '<p> The state you picked was: %s <p>' % state[2:]
        secondHeading = '<p>The industry you picked was: %s <p>' % industry
        thirdHeading = '<p>The year range you selected was: %s to %s <p>' % (startYear, endYear)
        print firstHeading, secondHeading, thirdHeading
        print '<p>'
        
        # Calculate the average GDP:
        sum = 0
        for i in data:
            sum += int(i[0])
        averageGDP = sum/float(yearRange)
        print 'The average GDP for your parameters was: $' + str(averageGDP)[:8] + ' million'

def calculateAndPrintVolatility():
    '''Calculates and prints the Volatility of the data selected by the user. The volatility
    is calculated using a complicated algorithm shown below. '''
    data, startYear, endYear, state, industry, yearRange = findVariablesGetData('volatility')
    if str(data) == '()':
            print "You have entered incorrect parameters in the form. Please enter correct parameters."
    else:
        print '============== GDP Volatility ==============='
        firstHeading = '<p> The state you picked was: %s <p>' % state[2:]
        secondHeading = '<p>The industry you picked was: %s <p>' % industry
        thirdHeading = '<p>The year range you selected was: %s to %s <p>' % (startYear, endYear)
        print firstHeading, secondHeading, thirdHeading
        print '<p>'
        
        # Calculate the volatility
        sum = 0
        totalDistribution = 0
        for i in data:
           sum += int(i[1])
        averageValue = sum / len(data)
        for i in data:
           totalDistribution += pow(int(i[1]) - averageValue, 2)
        volatility = 100*((math.sqrt(totalDistribution/len(data)))/int(yearRange))/averageValue
        
        print '<p>The volatility index is a measure of change in a trend.</p>'
        print '<p>The values can range from 1 to much higher, where 1 corresponds to perfect alignment with'
        print 'a trend and higher values correspond to more deviation.</p>'
        print '<p>The volatility of the GDP during the specified year range was: ' + str(volatility)[:4]
        
        graph = makeGraph(data)
        print graph
   
   

if __name__ == '__main__':

    # Get the user input from the CGI parameters.
    form = cgi.FieldStorage()
    
    # If the user wants to see our source files, let them!
    if 'showsource' in form:
        sourceFileToShow = form['showsource'].value
    else:
        sourceFileToShow = ''
    
    # If the function has been selected, get it from the form
    if 'Function' in form:
        function = form['Function'].value
    else:
        function = ''
    
    if len(sourceFileToShow) > 0:
        print "Content-type: text/plain\r\n\r\n"
        print open(sourceFileToShow).read()
    
    else:
        link1 = '<p><a href="index.py?showsource=index.py">index.py source</a></p>\n'
        link2 = '<p><a href="index.py?showsource=datasource.py">datasource.py source</a></p>\n'
        link3 = '<p><a href="index.py?showsource=readme.html">README</a></p>\n'
        
        chooseAndExecuteFunction(function, link1, link2, link3)
            
