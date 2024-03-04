import numpy as np
import matplotlib.pyplot as plt



n = 2
data1 = np.genfromtxt('freq vs voltage104c.csv',delimiter=',',dtype=np.float64)
data2=np.genfromtxt('freqvsphase lcr.csv',delimiter=',',dtype=np.float64)
data3=np.genfromtxt('freqvsphase2bnc.csv',delimiter=',',dtype=np.float64)
xdata=data1[:,1]
ydata=data1[:,0]
xdata1=data2[:,1]
ydata1=data2[:,0]
xdata2=data3[:,1]
ydata2=data3[:,0]
plt.scatter(xdata,ydata,label="1 BNC WITHOUT LCR phase")
#plt.scatter(xdata2,ydata2,label="2 BNC WITHOUT LCR phase")
#plt.scatter(xdata1,ydata1-ydata2,label="2BNC + LCR phase- 2BNC")
plt.xlabel('frequency(khz)')
plt.ylabel('voltage')
plt.title('frequency vs phase')
plt.grid()
plt.legend()
plt.show()