import csv
import time
import pyvisa
import bhavtoshlab_11 as bl

def main():
    R= 22000
    voltage = 0.452
    # Open connection to your instrument
    ITc= bl.ITC503_temperature_Controller(4)
    Lockincu = bl.SR830LockIn_interface(3)
    Lockincv = bl.SR830LockIn_interface(2)
    #ITc._setSweepStep(0.1,[310,33.7,330])
    ITc.set_SetPoint(100)
    ITc.flush()
    Lockincv.setInputVoltage(voltage)
    # #ITc.setSweeps({{1:{'set_point':300,'sweep_time':0.1,'hold_time':7}},{2:{'set_point':33.7,'sweep_time':0.1,'hold_time':7}},{3:{'set_point':340,'sweep_time':0.1,'hold_time':7}}})
    ITc._setSweepStep(1,{'set_point':200,'sweep_time':20,'hold_time':1}) # the 20 calculated for 5k/min sweep_time = (final-initial)/(how much kelvin per minutes)
    ITc._setSweepStep(2,{'set_point':100,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(3,{'set_point':200,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(4,{'set_point':100,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(5,{'set_point':200,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(6,{'set_point':100,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(7,{'set_point':200,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(8,{'set_point':100,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(9,{'set_point':200,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(10,{'set_point':100,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(11,{'set_point':200,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(12,{'set_point':100,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(13,{'set_point':200,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(14,{'set_point':100,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(15,{'set_point':200,'sweep_time':20,'hold_time':1})
    ITc._setSweepStep(16,{'set_point':100,'sweep_time':20,'hold_time':1})
   #ITc._setSweepStep(1,{'set_point':310,'sweep_time':0.6,'hold_time':11})
    
    ITc.orm.write('$S1')
    #inst.query('T 300')
    # Set up CSV file and writer
    current_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    csv_filename = f"2kmindata_temp_time_stamp{current_time}.csv"
    csv_file = open(csv_filename, mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Time', 'Temp','Vx','Vy','Vr','theta','Ix','Iy','Ir','Itheta','R'])

    try:
        
        #query_commands = ['R 1','R 1']
        counter =0
        while True:
            for i in range(2):
                # Query the instrument
                current_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
                response = ITc.get_Temperature(1)
                responselockinVx = Lockincv.getVoltageX()
                responselockinVy = Lockincv.getVoltageY()
                responselockinVr = Lockincv.getVoltageR()
                responselockintheta = Lockincv.getPhase()

                responselockinIx = float(Lockincu.getVoltageX())
                responselockinIy = float(Lockincu.getVoltageY())
                responselockinIr = float(Lockincu.getVoltageR())
                responselockinItheta = Lockincu.getPhase()
               
                resistance= float(responselockinVr)/(responselockinIr/R)
                # print(f"Time: {current_time}, Temp: {(float(response))}, Vx : {(float(responselockinVx))}, Vy : {(float(responselockinVy))},VR : {(float(responselockinVr))},theta : {(float(responselockintheta))}")
                # print(f"Time: {current_time}, Temp: {(float(response))}, Vx : {(float(responselockinIx))}, Vy : {(float(responselockinIy))},VR : {(float(responselockinIr))},theta : {(float(responselockinItheta))}")
                # # Get current time
                
               # Lockin.autoSensetivity()


                
                # Write time and response value to CSV
                csv_writer.writerow([current_time,  (float(response)),(float(responselockinVx)),(float(responselockinVy)),(float(responselockinVr)),(float(responselockintheta)) ,(float(responselockinIx)),(float(responselockinIy)),(float(responselockinIr)),(float(responselockinItheta)), ((abs(resistance)))])
               # print(f"Time: {current_time}, Temp: {(float(response))}")
                Lockincu.autoSensetivity(abs(responselockinIr))
                Lockincv.autoSensetivity(abs(float((responselockinVr))))
                # Sleep for a while before the next query
                #time.sleep(1)  # Adjust the sleep time as needed

            # Check if user wants to stop the loop
            #stop = input("Press '1' and Enter to save CSV and exit, or press Enter to continue: ")
            

    except KeyboardInterrupt:
        ITc.orm.write('$C0')
        print("\nLoop stopped by user.")
        Lockincu.autoSensetivity(0.7)
        Lockincv.autoSensetivity(0.7)

    finally:
        # Close CSV file and instrument connection
        csv_file.close()
        #inst.close()
        print("CSV file closed and instrument connection closed.")

if __name__ == "__main__":
    main()
