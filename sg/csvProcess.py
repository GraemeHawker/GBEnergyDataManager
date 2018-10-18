""" Functionality to simply the loading and writing of csv files
"""
import csv

def csvToList(fn,h):
    
    #Requires a file name and weather or not headers are included; returns 2-D list - outerlist length = No of Cols; inner list length = No of Rows
    # inputs: 
    # - fn = filename, string
    # - h = header flag, int, either 0 (treat headers seperately) or 1 (including headers in main lists
    # outputs
    # - 1 - main 2- D list
    # - 2 - Number of columns
    # - 3 - Number of rows
    # - 4 - (optional) Seperate list of headers if header flag specified as 1.
    
    #Open csv file and setup csv Reader 
    with open (fn, 'r') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        #Variable to collect data
        csvData = []
        headers = []

        #Deal with first row seperately, count columns. 
        r1 = next(csvReader)
        nr = len(r1)
        
        #If header flag is on place first row in headers variable, Otherwise add as first entry in dataliast
        if h ==1:
            headers = r1
        else:
            if nr ==1:
                csvData.append(r1[0])
            else:
                csvData.append(r1)
    
        #For all other rows append to datalist and check length is consistant
        for row in csvReader:
            if len(row) != nr:
                print('Input csv file does not have consistant line length')
                return 
            if nr == 1:
                csvData.append(row[0])
            else:
                csvData.append(row)
        
        #Count number of data entries, and zip to change order 
        nd = len(csvData)
        if nr > 1:
            csvL = [list(x) for x in list(zip(*csvData))]
        else:
            csvL = csvData
            
    if headers == []:
        return csvL, nr, nd
    else:
        return csvL, nr, nd, headers
                
                
def listToCsv(fn, dataList, headers):

    # Some data quality checking
    nc = len(dataList)
    if nc != len(headers):
        print('Length of headers incompatable with number of data columns in listToCSV')
        return 0
    
    nr = len(dataList[0])
    for c in dataList:
        if len(c) != nr: 
            print('Length of data columns are not consistant in listToCSV')
            return 0
    
    
    with open(fn, 'w', newline ='') as fileOut:
        fileWriter = csv.writer(fileOut, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)        
        fileWriter.writerow(headers)
        for rr in zip(*dataList):
            fileWriter.writerow(rr)
    
    return 1
        