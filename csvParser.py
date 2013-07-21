from option import Option
import csv
import datetime as dt
import operator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import dateutil.parser as dpa
import numpy as np
import pandas as pd

def parseDate(row):
    d = int(row.split('-')[0])
    month = row.split('-')[1]
    y = int(row.split('-')[2])
    months = {'Jan' : 1,
               'Feb' : 2,
               'Mar' : 3,
               'Apr' : 4,
               'May' : 5,
               'Jun' : 6,
               'Jul' : 7, 
               'Aug' : 8,
               'Sep' : 9,
               'Oct' : 10,
               'Nov' : 11,
               'Dec' : 12
    }
    m = months[month]
    return dt.datetime(y,m,d)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        if (start_date + dt.timedelta(n)).weekday() >= 5:
            continue  
        yield start_date + dt.timedelta(n)
 
def getBusinessDays(fromDate, toDate):
    count = 0
    for single_date in daterange(fromDate, toDate):
        count = count + 1
    return count

def processNSEOptionsFile(fi,fo):
    rf = 0.10
    v = 0.1467
    fmt = '%Y-%m-%d'
    days = 250.0
    writer = csv.writer(fo)
    reader = csv.reader(fi)
    headerline = reader.next()
    outputRow = 'strike','date','underlying','close','dte','iv'
    writer.writerow(outputRow)
    sortedlist = sorted(reader, key=operator.itemgetter(4), reverse=False)
    for row in sortedlist:
        row_symbol = row[0]
        row_date = parseDate(row[1])
        row_expiry = parseDate(row[2])
        row_dte = getBusinessDays(row_date, row_expiry)
        row_strike = int(row[4])
        row_close = float(row[5])
        row_uling = float(row[15])
        try:
            row_iv = Option(row_strike,row_uling,rf,row_dte/days,v).get_iv(row_close,row[3][:1]) * 100.0
        except:
            print "IV incorrect. Setting to 0."
            row_iv = 0.0
        outputRow = str(row_strike),row_date.strftime(fmt),str(row_uling),str(row_close),str(row_dte),'%2.2f' % row_iv
        writer.writerow(outputRow)

def getStrike(reader, strike):
    #row = {date, underlying, close,,implied_volatility}
    optdict = []
    reader.next()
    for row in reader:
        if int(row[0]) == strike:
            r1 = dpa.parse(row[1])
            r1 = [r1] + row[2:]
            optdict.append(r1 )   
    return optdict

def ivandcloseGraph(optdict, strike):
    row_0 = [row[0] for row in optdict] 
    row_2 = [row[2] for row in optdict] 
    row_4 = [row[4] for row in optdict] 
    dates = mdates.date2num(row_0)
    ax1=plt.subplot(111)
    p1, = ax1.plot_date(dates, row_4, 'b-', label='Implied Volatility')
    plt.ylabel("Implied Volatility")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True)
    ax2=ax1.twinx()
    p2, = ax2.plot_date(dates, row_2, 'r-', label='Close')
    plt.ylabel("Close")
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(bbox_to_anchor=(0.01, 1.12, 1., .112), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)
    ax1.legend(bbox_to_anchor=(0.01, 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)
    myFmt = mdates.DateFormatter('%d-%m')
    ax1.xaxis.set_major_formatter(myFmt)
    plt.show()
    print "Implied Volatility : ",row_4[-1]
    print "Close              : ",row_2[-1]
    
def ivandstdGraph(optdict, strike):
    row_0 = [row[0] for row in optdict] 
    row_1 = [float(row[1]) for row in optdict] 
    row_2 = [float(row[1]) for row in optdict] 
    row_4 = [row[4] for row in optdict] 
    dates = mdates.date2num(row_0)
    ax1=plt.subplot(211)
    p1, = ax1.plot_date(dates, row_4, 'b-', label='Implied Volatility')
    plt.ylabel("Implied Volatility")
    ax2=ax1.twinx()
    row_1np = np.array(row_1)
    row_1std = pd.rolling_std(row_1np, 5,5)
    p2, = ax2.plot_date(dates, row_1std, 'r-', label='Std Dev')
    plt.ylabel("Std Dev")
    myFmt = mdates.DateFormatter('%d-%m')
    ax1.xaxis.set_major_formatter(myFmt)
    ax3 = plt.subplot(212)
    p2, = ax3.plot_date(dates, row_2, 'r-', label='Close')
    plt.ylabel("Close")
    plt.show()
    
if __name__ == '__main__':
    fi = open('OPTSTK_TCS_CE_13-07-2012_TO_12-07-2013.csv', 'rb')
    fo = open('TCS_CE_14-04-2013_TO_12-07-2013.csv', 'wb')
    processNSEOptionsFile(fi,fo)
    fi = open('TCS_CE_14-04-2013_TO_12-07-2013.csv', 'rb')
    reader = csv.reader(fi)
    strike = 1520
    optdict = getStrike(reader,strike)
    ivandcloseGraph(optdict, strike)
    ivandstdGraph(optdict, strike)