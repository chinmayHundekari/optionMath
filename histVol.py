import pandas as pd
import bp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import scipy.io as sio
import time, csv
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da


def read_symbols(s_symbols_file):

    ls_symbols=[]
    file = open(s_symbols_file, 'r')
    for line in file.readlines():
        str_line = str(line)
        if str_line.strip(): 
            ls_symbols.append(str_line.strip())
    file.close()
    
    return ls_symbols  

def getData(startDate, endDate, symbols, cache=1):
    ldt_timestamps = du.getNYSEdays(startDate, endDate, dt.timedelta(hours=16))
    if (cache  == 1):
        dataobj = da.DataAccess('Yahoo')#, cachestalltime=0)
    else:
        dataobj = da.DataAccess(('Yahoo'), cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    return d_data

def showGraph(stock, d_data, rolling_std):
    quotes = d_data[stock]
    ldt_timestamps = rolling_std.index
    fig = plt.figure()
    fig.set_size_inches(10,7)
    ax1 = fig.add_subplot(111)
    ax1.plot(ldt_timestamps, list(quotes), 'b-')
    ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax2=ax1.twinx()
    ax2.plot(ldt_timestamps, list(rolling_std[stock]), 'r-')
    fig.autofmt_xdate()
    #print quotes
    plt.title(stock)
    str = "data/" + stock + ".png"
    print stock
    fig.savefig(str)
    fig.clf()
    
    
    
if __name__ == '__main__':
    dt_start = dt.datetime.now()-dt.timedelta(720)#dt.datetime(2012, 1, 1)
    dt_end = dt.datetime.now()
    ls_symbols = read_symbols('data/symbols.txt')
    d_data = getData(dt_start,dt_end,ls_symbols,1)
    rolling_std20 = pd.rolling_std(d_data['close'],20,min_periods=20)
    rolling_std50 = pd.rolling_std(d_data['close'],50,min_periods=50)
    rolling_std = rolling_std20#/rolling_std50
    for sym in ls_symbols:
	    showGraph(sym, d_data['close'], rolling_std)
        
    
    