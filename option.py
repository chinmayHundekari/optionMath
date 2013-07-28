"""
Black Scholes Option pricing
============================

"""
import math
from scipy.stats import norm


class Option:
    def __init__(self, k, s, rf, t, vol=0.1):
        self.k = float(k)
        self.s = float(s)
        self.rf = float(rf)
        self.vol = float(vol)
        self.t = float(t)
        self.calc_D()

    def calc_D(self):
        self.d1 = ((math.log(self.s/self.k) +
                   (self.rf + math.pow(self.vol, 2) / 2) * self.t) /
                   (self.vol * math.sqrt(self.t)))
        self.d2 = self.d1 - self.vol * math.sqrt(self.t)

    def get_call(self):
        self.calc_D()
        return (norm.cdf(self.d1) * self.s - norm.cdf(self.d2) *
                self.k * math.exp(-self.rf * self.t))

    def get_put(self):
        self.calc_D()
        return (norm.cdf(-self.d1) * -1.0 * self.s + norm.cdf(-self.d2)
                * self.k * math.exp(-self.rf * self.t))

    def get_delta(self, d=0.01, callorput='C'):
        if callorput == 'C':
            return norm.cdf(self.d1)
        else:
            return -norm.cdf(-self.d1)

    def get_theta(self, callorput='C'):
        t1 = self.t
        _b_ = math.e**-(self.rf* t1)
        if callorput == 'C':
            theta = -self.s * norm.pdf(self.d1) * self.vol / (2 * self.t ** 0.5) - (1.0+self.rf) * self.k * _b_ *  norm.cdf(self.d2)
        else:
            theta = -(-self.s * norm.pdf(self.d1) * self.vol /(2 * self.t **0.5) + (1.0+self.rf) *self.k * _b_ * norm.cdf(-self.d2))
        return theta / 365


    def get_vega(self):
        return self.s * norm.pdf(self.d1) * (self.t) ** 0.5 / 100

    def get_iv(self, price, callorput='C'):
        upper = 1000.0
        lower = 0.0
        IV = 500.0
        for i in xrange(1, 1000):
            if callorput == 'C':
                optPrice = Option(self.k, self.s, self.rf,
                                  self.t, IV/1000.0).get_call()
            else:
                optPrice = Option(self.k, self.s, self.rf,
                                  self.t, IV/1000.0).get_put()
            if optPrice > price:
                upper = IV
            else:
                lower = IV
            IV = (lower + upper) / 2
            if (abs(optPrice - price) < 0.1):
                break
        return IV/1000.0

    def print_greeks(self, price, callorput):
        self.vol = self.get_iv(price, callorput)
        self.calc_D()
        delta = self.get_delta(callorput=callorput)
        theta = self.get_theta(callorput=callorput)
        vega = self.get_vega()
        print "Delta :", delta
        print "Theta :", theta
        print "Vega  :", vega
        print "Vol   :", self.vol * 100

    def getGreeks(self, price, callorput):
        self.vol = self.get_iv(price, callorput)
        self.calc_D()
        delta = self.get_delta(callorput=callorput)
        theta = self.get_theta(callorput=callorput)
        vega = self.get_vega()
        return delta, theta, vega, self.vol

  
    def getProbITM(self, be, bo):
        v = self.vol * math.sqrt(self.t*256)/math.sqrt(256)
        if be:
            becdf = 1 - norm.cdf(be[0],self.s,self.s*v)
        else:
            becdf = 1.0
        if bo:
            bocdf = 1.0 - norm.cdf(bo[0],self.s,self.s*v)
        else:
            bocdf = 0.0
        print "Probability of ITM",(becdf-bocdf) * 100, "%"
        return becdf-bocdf
