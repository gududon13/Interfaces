import pyvisa as pv
import time
import csv
import bhavtoshlab_11 as bl
import matplotlib.pyplot as plt
import pandas as pd 

# RESOURCE_LISTS = pv.ResourceManager().list_resources()
# print(RESOURCE_LISTS)

Temp_Calibration = 12
TempController = bl.ITC503_temperature_Controller('GPIB0::24::INSTR')
Agilent = bl.Oscilloscope('GPIB0::19::INSTR')
InitialTime = time.time()
VariableTime = 0

time.sleep(5)

current_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
csv_filename = f"P-E Loop {current_time}.csv"
csv_file = open(csv_filename, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'Temp','File'])

Counter = 0
try:
    while True:
        VariableTime = time.time() - InitialTime
        Temperature = float(TempController.get_Temperature(1)) - Temp_Calibration
        Agilent.get_values(str(Counter)+'_X.csv','1')
        Agilent.get_values(str(Counter)+'_Y.csv','2')

        csv_writer.writerow([VariableTime,Temperature,str(Counter)])
        Counter += 1

        File1 = pd.read_csv('C:\\Users\\Satyaki Kundu\\Desktop\\CRN_New\\New folder\\'+str(Counter)+'_X.csv',names=['Time','Voltage'])
        File2 = pd.read_csv('C:\\Users\\Satyaki Kundu\\Desktop\\CRN_New\\New folder\\'+str(Counter)+'_Y.csv',names=['Time','Voltage'])

        plt.plot(File1['Voltage'],File2['Voltage'])

        time.sleep(5)

except KeyboardInterrupt:
    print('Loop broken')

csv_file.close()
Agilent.system.close()
print("CSV file closed and instrument connection closed.")

plt.show()