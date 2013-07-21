## Download daily intra day charts from yahoo finance
## symbolList.txt:(<Yahoo symbol>,<image_finename>)
##  ^NSEI,NSEI
##	ACC.NS,ACC
##	AMBUJACEM-EQ.NS,AMBUJACEM-EQ
##	AXISBANK.NS,AXISBANK
 
import urllib
import csv
import os
from datetime import date
fi = open("symbolList.csv", "rb")
symList = csv.reader(fi)
dt = date.today()
if not os.path.exists("./Intraday_YAHOO"):
    os.makedirs("./Intraday_YAHOO")
direc = "./Intraday_YAHOO/"+str(dt.year)+str(dt.month).zfill(2)+str(dt.day).zfill(2)
if not os.path.exists(direc):
    os.makedirs(direc)
 
for row in symList:
	print row[0],row[1]
	url_chart = "http://chart.finance.yahoo.com/z?s=" + row[0] + "&t=1d&q=&l=off&z=m&a=v&p=s&lang=en-US&region=US"
	file_chart = direc+"/"+row[1]+".jpg"
	
	urllib.urlretrieve(url_chart, file_chart)