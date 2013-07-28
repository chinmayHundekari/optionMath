import matplotlib.pyplot as plt

## Long 250 95 Call 5.5
def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step
		
def processOptionStrategy(strat, price_point):
	strategy = strat.split(' ') 
	if (strategy[2] == 'Stock'):
		volume = float(strategy[1])
		price = float(strategy[3])
	else:
            try:
                volume = float(strategy[1])
                strike = float(strategy[2])
                price = float(strategy[4])
            except:
                print "dumbass...numbers"
	if strategy[0] == 'Long':
		if strategy[3] == 'Call':
			if price_point < strike:
				return -(price * volume)
			else:
				return (((price_point - strike) * volume) -(price * volume))
		elif strategy[3] == 'Put':
			if price_point > strike:
				return -(price * volume)
			else:
				return (((strike - price_point) * volume) -(price * volume))
		elif strategy[2] == 'Stock':
                    return (price_point - price) * volume
		else:
			print "dumbass...Call or put"
	elif strategy[0] == 'Short':
		if strategy[3] == 'Call':
			if price_point < strike:
				return (price * volume)
			else:
				return ((price * volume)) - ((price_point - strike) * volume)
		elif strategy[3] == 'Put':
			if price_point > strike:
				return (price * volume)
			else:
				return ((price * volume)) - ((strike - price_point) * volume)
		elif strategy[2] == 'Stock':
                    return (price - price_point) * volume
		else:
			print "dumbass...Call or put"
	else:
		print "dumbass...Long or short"

def listStrategy(strats):
	stratvals = []
	yticks = []
	xticks = []
	max = 0
	min = 1000000
	for row in strats:
	    valstr = row.split(' ')[2]
	    if valstr == 'Stock':
	        val = float(row.split(' ')[3])
	        xticks.append(val)
	    else:
	        val = float(valstr)
                xticks.append(val)
            if val < min:
                min = val
            if val > max:
            	max = val
            stratvals.append(val)
        xticks.append(min * 0.9)
        xticks.append(max * 1.1)
	for i in xticks:
		sum = 0
		for strat in strats:
			sum = sum + processOptionStrategy(strat, i)
		yticks.append((i,sum))
        yticks.sort()
        breakeven = []
        breakodd = [] 
        for i in range(0,len(yticks)-1):
            if ((yticks[i][1] < 0) and (yticks[i+1][1] > 0)):
                y1 = yticks[i][1]
                y21 = yticks[i+1][1] - y1
                x1 = yticks[i][0]
                x21 = yticks[i+1][0] - x1
                breakeven.append(-y1 * x21 / y21 + x1)
            elif ((yticks[i][1] > 0) and (yticks[i+1][1] < 0)):
                y1 = yticks[i][1]
                y21 = yticks[i+1][1] - y1
                x1 = yticks[i][0]
                x21 = yticks[i+1][0] - x1
                breakodd.append(-y1 * x21 / y21 + x1)
#        print breakeven, breakodd
#        print yticks
        
        return yticks, breakeven, breakodd
	
def plotStrategy(strats):
    ticks, be, bo = listStrategy(strats)
    xvals = [tick[0] for tick in ticks]
    yvals = [tick[1] for tick in ticks]
    plt.plot(xvals, yvals)
    plt.axhline(0, color='black')
    xvals = xvals +  be + bo
    plt.xticks(xvals, rotation=45)
    plt.grid(b=True, which='major', color='g', linestyle='--')
    plt.show()
	
    