import bhavtoshlab as bl 
import csv
import time
import matplotlib.pyplot as plt
import numpy as np

kilo = 1000.00
print(bl.RESOURCE_LISTS)
lockin = bl.SR830LockIn_interface(2)
lockin.setInputVoltage(0.45)

file_name = 'freqvsvoltageLRnoironcore.csv'
header = ['Frequency', 'R']
x1 =np.zeros(100)
y1=np.zeros(100)
with open(file_name, 'w', encoding='UTF8') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(header)
     
    for freq in range(1,101):
        lockin.setFrequency(freq*1000)
        lockin.autoTimeConstant()
        lockin.autoSensetivity()
        time.sleep(3)
        lockin.getFrequency()
        x1[freq-1]=lockin.getFrequency()
        lockin.getVoltageR()
        y1[freq-1]=lockin.getVoltageR()

        print(lockin.getFrequency(),lockin.getVoltageR(),x1[freq-1],y1[freq-1])
        writer.writerow([lockin.getFrequency(),lockin.getVoltageR()])  

plt.scatter(x1,y1,label="phase")
plt.xlabel('frequency(khz)')
plt.ylabel('phase')
plt.title('frequency vs voltage LR')
plt.grid()
plt.legend()
plt.show()

    