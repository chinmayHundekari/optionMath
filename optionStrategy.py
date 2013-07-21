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

def plotStrategy(strats, min1=0.9, max1=1.1):
	stratvals = []
	min = 100000
	max = 0
	xticks = []
	for row in strats:
	    valstr = row.split(' ')[2]
	    if valstr == 'Stock':
	        val = float(row.split(' ')[3])
	        xticks.append(val)
	    else:
	        val = float(valstr)
            if val < min:
                min = val
            if val > max:
            	max = val
            stratvals.append(val)
            xticks.append(val)
	yvals = []
	xvals = []
	max = max * max1  
	min = min * min1
	for i in drange(min, max, (max - min) / 200.0 ):
		xvals.append(i)
		sum = 0
		for strat in strats:
			sum = sum + processOptionStrategy(strat, i)
		yvals.append(sum)
		if i in stratvals:
			xticks.append(i)
		if len(yvals) >3:
			if (abs(yvals[-1] + yvals[-2]) < abs(yvals[-1] - yvals[-2])):
				xticks.append(i-(max - min) / 200.0)
	plt.plot(xvals, yvals)
	plt.axhline(0, color='black')
	plt.xticks(xticks)
	plt.setp(plt.xticks()[1], rotation=60)
	plt.grid(b=True, which='major', color='g', linestyle='--')
	
	plt.show()

def listStrategy(strats, xticks):
	stratvals = []
	yticks = []
	for row in strats:
	    valstr = row.split(' ')[2]
	    if valstr == 'Stock':
	        val = float(row.split(' ')[3])
	        xticks.append(val)
	    else:
	        val = float(valstr)
                xticks.append(val)
            stratvals.append(val)
	for i in xticks:
		sum = 0
		for strat in strats:
			sum = sum + processOptionStrategy(strat, i)
		yticks.append([i,sum])
        for i in range(0, len(xticks)):
            print yticks[i][0],"\t", yticks[i][1]
	
	
