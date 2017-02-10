import csv
import numpy as np
from __init__ import userVals

class candleLogic:

    def OHLCV(self, data):
        # Call imported user1 class
        mydata = open('EURUSD_Hist_Week3.csv')
        dataread = csv.reader(mydata, delimiter=',')
        csvData = list(dataread)

        # OHLC variables to return in array
        o = csvData[data][2]
        h = csvData[data][3]
        l = csvData[data][4]
        c = csvData[data][5]
        v = csvData[data][1]
        return float(o), float(h), float(l), float(c), int(v)

    # Define clean function routes for returning proper data
    def Open(self, data):
        return self.OHLCV(data)[0]

    def High(self, data):
        return self.OHLCV(data)[1]

    def Low(self, data):
        return self.OHLCV(data)[2]

    def Close(self, data):
        return self.OHLCV(data)[3]

    def Volume(self, data):
        return self.VolumeGet(data)

    def getData(self, data):
        u = userVals()
        numList = []
        for x in range(u.warmUpPeriod, data):
            numList.append(self.Close(x))
        return numList

    def getDataHA(self, data):
        numList = []
        for x in range(0, userVals.count):
            numList.append(self.HA_Close(x))
        return numList

    def getDataHAlow(self):
        numList = []
        for x in range(0, userVals.count):
            numList.append(self.HA_Low(x))
        return numList

    def getDataHAhigh(self):
        numList = []
        for x in range(0, userVals.count):
            numList.append(self.HA_High(x))
        return numList

    def getDataVolume(self):
        numList = []
        for x in range(0, userVals.count):
            numList.append(self.Volume(x))
        return numList

    def haCandles(self, data):
        haClose = (self.OHLCV(data)[0] + self.OHLCV(data)[1] + self.OHLCV(data)[2] + self.OHLCV(data)[3]) / 4
        haOpen = (self.OHLCV(data-1)[0] + self.OHLCV(data-1)[0]) / 2
        haHigh = np.max([self.OHLCV(data)[1], haOpen, haClose])
        haLow = np.min([self.OHLCV(data)[2], haOpen, haClose])
        return haOpen, haHigh, haLow, haClose

    def HA_Open(self, data):
        return self.haCandles(data)[0]

    def HA_High(self, data):
        return self.haCandles(data)[1]

    def HA_Low(self, data):
        return self.haCandles(data)[2]

    def HA_Close(self, data):
        return self.haCandles(data)[3]