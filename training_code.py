import bhavtoshlab as bl 
import csv
import time
import matplotlib.pyplot as plt
import numpy as np

kilo = 1000.00
print(bl.RESOURCE_LISTS)
lockin = bl.SR830LockIn_interface(2)
lockin.setInputVoltage(0.45)

file_name = 'lCR.csv'
header = ['Frequency', 'VR', 'VX' , 'VY' , 'phase']
x =np.zeros(100)
y=np.zeros(100)
with open(file_name, 'w', encoding='UTF8') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(header)
     
    for freq in range(1,101):
        lockin.autoSensetivity()
        lockin.autoTimeConstant()  
        lockin.setFrequency(freq*300) 
        time.sleep(5)
        lockin.getFrequency()
        lockin.getVoltageR()
        lockin.getVoltageX()
        lockin.getVoltageY()
        lockin.getPhase()
        data1,data2=lockin.getFrequency(),lockin.getVoltageR()
        data3,data4,data5=  lockin.getVoltageX(),lockin.getVoltageY(),lockin.getPhase()
        x[freq-1]=data1
        y[freq-1]=data2
        print(data1,data2,data3,data4,data5)
        writer.writerow([data1,data2,data3,data4,data5])  
       

plt.scatter(y,x,label="random data")
plt.xlabel('frequency(khz)')
plt.ylabel('voltage')
plt.title('frequency vs voltage Sweep')
plt.grid()
plt.legend()
plt.show()

    