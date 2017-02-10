import numpy as np
import csv
from __init__ import userVals
import talib
import matplotlib.pyplot as plt


class Backtester(object):
    # Variables for state mangagement
    def __init__(self):
        u = userVals()
        self.initialCash = 5000
        self.totalTrades = 0
        self.tradeWins = 0
        self.tradeLosses = 0
        self.tradeLots = 0
        self.entryPrice = 0
        self.profit = 0
        self.loss = 0
        self.currentPosition = "None"
        self.initialPoint = u.warmUpPeriod
        self.status = True
        self.accountHistory = [self.initialCash]
        self.filename = "./Data/Forex/USDCAD_Hist_M15.csv"

    # Warm Up data for backtesting
    def warmUp(self):
        u = userVals()
        mydata = open(self.filename)
        dataread = csv.reader(mydata, delimiter=',')
        self.csvData = list(dataread)
        self.warmUpDataOpen = []
        self.warmUpDataHigh = []
        self.warmUpDataLow = []
        self.warmUpDataClose = []
        self.warmUpDataVolume = []
        self.warmUpDate = []
        for x in range(0, u.warmUpPeriod-1):
            open_ = self.csvData[x][2]
            high = self.csvData[x][3]
            low = self.csvData[x][4]
            close = self.csvData[x][5]
            volume = self.csvData[x][1]
            date = self.csvData[x][0]
            self.warmUpDataOpen.append(float(open_))
            self.warmUpDataHigh.append(float(high))
            self.warmUpDataLow.append(float(low))
            self.warmUpDataClose.append(float(close))
            self.warmUpDataVolume.append(float(volume))
            self.warmUpDate.append(date)
        return self.warmUpDataOpen, self.warmUpDataHigh, self.warmUpDataLow, self.warmUpDataClose, self.warmUpDataVolume, self.warmUpDate

    # Load data for backtesting feed forward
    def feedData(self, data):
        u = userVals()
        mydata = open(self.filename)
        dataread = csv.reader(mydata, delimiter=',')
        self.csvData = list(dataread)
        self.wO = self.warmUp()[0]
        self.wH = self.warmUp()[1]
        self.wL = self.warmUp()[2]
        self.wC = self.warmUp()[3]
        self.wV = self.warmUp()[4]
        self.wD = self.warmUp()[5]
        for x in range(u.warmUpPeriod, data):
            open_ = self.csvData[x][2]
            high = self.csvData[x][3]
            low = self.csvData[x][4]
            close = self.csvData[x][5]
            volume = self.csvData[x][1]
            date = self.csvData[x][0]
            self.wO.append(float(open_))
            self.wH.append(float(high))
            self.wL.append(float(low))
            self.wC.append(float(close))
            self.wV.append(float(volume))
            self.wD.append(date)
        return self.wO, self.wH, self.wL, self.wC, self.wV, self.wD


    # Place long entry signals here
    def tradeLong(self):
        if (self.SMA1[-1] > self.SMA2[-1]): return True
        return False

    # Place short entry signals here

    def tradeShort(self):
        #if (self.EMA1[-1] < self.EMA2[-1]): return True
        if (self.SMA1[-1] < self.SMA2[-1]): return True
        return False

    # Backtesting Function
    def main(self):
        u = userVals()
        mydata = open(self.filename)
        dataread = csv.reader(mydata, delimiter=',')
        self.csvData = list(dataread)
        for x in range(u.warmUpPeriod, len(self.csvData)):
            feed = self.feedData(x)
            open_= feed[0]
            high = feed[1]
            low = feed[2]
            close = feed[3]
            self.volume = feed[4]
            date = feed[5]

            # Create indicators here
            self.SMA1 = talib.SMA(np.array(self.close), timeperiod=15)
            self.SMA2 = talib.SMA(np.array(self.close), timeperiod=30)
            self.SMAHigh = talib.SMA(np.array(self.high), timeperiod=5)
            self.SMALow = talib.SMA(np.array(self.low), timeperiod=5)

            # Trade Logic 
            if self.currentPosition == "None":
                # Entry Signals
                if (self.tradeLong() == True ):
                    self.entryPrice = close[-1]
                    self.totalTrades = self.totalTrades + 1
                    self.tradeLots = abs((self.initialCash *userVals.risk)/abs(self.entryPrice - low[-2]))
                    self.currentPosition = "Long"

                elif (self.tradeShort() == True ):
                    self.entryPrice = close[-1]
                    self.totalTrades = self.totalTrades + 1
                    self.tradeLots = abs((self.initialCash *userVals.risk)/abs(self.entryPrice - high[-2]))
                    self.currentPosition = "Short"

            elif self.currentPosition != "None":
                # Exit Signals
                if self.currentPosition == "Long":
                    # Exit Long Position 
                    if (self.close[-1] < self.SMALow[-1]):                    
                        exitClose = close[-1]
                        pips = exitClose - self.entryPrice
                        pipValue = 1/exitClose/10
                        newCash = self.initialCash + (pipValue*pips*(self.tradeLots))

                        # Decide if trade was win or loss
                        if exitClose > self.entryPrice:
                            self.tradeWins = self.tradeWins +1
                            self.profit = (newCash - self.initialCash) + self.profit

                        elif exitClose < self.entryPrice:
                            self.tradeLosses = self.tradeLosses + 1
                            self.loss = (self.initialCash - newCash) + self.loss

                        self.initialCash = newCash
                        self.currentPosition = "None"
                        self.accountHistory.append(self.initialCash)

                elif self.currentPosition == "Short":

                    if (self.close[-1] > self.SMAhigh[-1]):
                        exitClose = close[-1]
                        pips = exitClose - self.entryPrice
                        pipValue = 1/exitClose/10
                        newCash = self.initialCash + (pipValue*pips*(self.tradeLots))

                        # Decide if trade was win or loss
                        if exitClose < self.entryPrice:
                            self.tradeWins = self.tradeWins +1
                            self.loss = (self.initialCash - newCash) + self.loss

                        elif exitClose > self.entryPrice:
                            self.tradeLosses = self.tradeLosses + 1
                            self.profit = (newCash - self.initialCash) + self.profit

                        self.initialCash = newCash
                        self.currentPosition = "None"
                        self.accountHistory.append(self.initialCash)

        print "Account:", self.initialCash, "Total Trades:", self.totalTrades, "Wins:", self.tradeWins, "Losses:", self.tradeLosses, "Profit:", self.profit, "Losses:", self.loss
        plt.xlabel('Total Trades')
        plt.ylabel('Balance')
        plt.plot(np.array([x for x in range(len(self.accountHistory))]), np.array(self.accountHistory))
        plt.savefig('BacktestForex.png')

if __name__ == "__main__":
  b = Backtester()
  print b.main()
