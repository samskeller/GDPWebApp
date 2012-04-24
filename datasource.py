'''
Written by Justin Norden, Cole Stephan, and Sam Keller

04/09/2012

This is our class for extracting the data we need from our data set on GDP
'''
import MySQLdb
import dbconstants

def getConnection():
    ''' Gets a connection to the SQL database so we can query the database'''
    connection = MySQLdb.connect(host=dbconstants.host,
                                 user=dbconstants.user,
                                 passwd=dbconstants.passwd,
                                 db=dbconstants.db)
    return connection

def queryDatabase(function, startYear, endYear, yearRange, fip, industry):
    ''' Returns data from the SQL database. Depending upon the function the user is running,
    the data can be returned in a number of different forms.'''
    connection = getConnection()
    cursor = connection.cursor()
    if function == 'getGDP' or function == 'volatility':
        queryYearsString ="(yearString='%s'" % (startYear)
        for i in range(yearRange-1):
            queryYearsString += " OR yearString ='%s'" % (str(int(startYear)+i+1))
        queryYearsString += ')'
        query = "SELECT yearString,gdpString FROM gdpData WHERE %s AND industryString='%s' AND fip=%s" % (queryYearsString,industry,fip)
        cursor.execute(query)
        gdpData = cursor.fetchall()
        cursor.close()
        connection.close()
        return gdpData
    if function == 'growthRate':
        query = "SELECT gdpString FROM gdpData WHERE (yearString='%s' or yearString='%s') AND" % (startYear,endYear)\
                + " industryString='%s' AND fip='%s' ORDER BY yearString" % (industry, fip) 
        cursor.execute(query)
        gdpGrowthRate = cursor.fetchall()
        cursor.close()
        connection.close()
        return gdpGrowthRate
    if function == 'avgGDP':
        queryYearsString ="(yearString='%s'" % (startYear)
        for i in range(yearRange-1):
            queryYearsString += " OR yearString ='%s'" % (str(int(startYear)+i+1))
        queryYearsString += ')'
        query = "SELECT gdpString FROM gdpData WHERE %s AND industryString='%s' AND fip=%s" % (queryYearsString,industry,fip)
        cursor.execute(query)
        avgGDP = cursor.fetchall()        
        cursor.close()
        connection.close()
        return avgGDP
    

def main():
    pass

if __name__ == '__main__':
    main()
