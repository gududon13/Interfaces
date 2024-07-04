import numpy as np
import matplotlib.pyplot as plt
import pyvisa as pv
import multiprocessing as mp
import time


KILO = 1000
RESOURCE_LISTS = pv.ResourceManager().list_resources()

class SR830LockIn_interface:
    
    def __init__(self,adress=0):
        self.ad=RESOURCE_LISTS[adress]
        self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\r',read_termination='\r')
        
    def setInputVoltage(self,voltage):
        if(voltage <= 0.8):
            command= str('SLVL'+str(voltage))
            print(command)
            self.orm.write(command)
            
           
        else:
            print("High voltage i.e greater than '1v' is damaging for system so restricted")
        pass
    def getInputVoltage(self,unit = 'v'): 
        return self.orm.query('SLVL?')
    
    def setInputCurrent(self,current, unit = 'v'):
        pass
    def getInputCurrent(self):
        pass
    def setFrequency(self,freq,unit = 'khz'):
        command= str('FREQ'+str(freq))
        print(command)
        self.orm.write(command)
    def getFrequency(self,unit = 'khz'):
         return self.orm.query('FREQ?')
        
    def getImpedence(self,unit = 'ohm'):
        pass
    def getVoltageR(self,unit = 'v'):
         return self.orm.query('OUTP?3\r')
    def getVoltageX(self,unit = 'v'):
         return self.orm.query('OUTP?1')
    def autoSensetivity(self):
        vr = float(self.getVoltageR())
        if (vr)>= 0.2 and (vr)< 0.5 :
            self.orm.write('SENS25\r')
        elif(vr)>= 0.1 and (vr) < 0.2:
             self.orm.write('SENS24\r')
        elif(vr)>= 0.02 and (vr) < 0.05:
             self.orm.write('SENS23\r')
        elif(vr)>= 0.01 and (vr) < 0.02:
             self.orm.write('SENS22\r')
        elif(vr)>= 0.005 and (vr) < 0.01:
             self.orm.write('SENS21\r')
        elif(vr)>= 0.002 and (vr) < 0.005:
             self.orm.write('SENS19\r')
        elif(vr)>= 0.001 and (vr) < 0.002:
            self.orm.write('SENS19\r')
        elif(vr)>= 0.0002 and (vr) < 0.001:
             self.orm.write('SENS17\r')
        elif(vr)>= 0 and (vr) < 0.0001:
             self.orm.write('SENS15\r')
        else:
             self.orm.write('SENS26\r')
            

        
    def autoTimeConstant(self):
        fq = float(self.getFrequency())
        if (fq)>= 500 and (fq)< 1000 :
            self.orm.write('OFLT7')
        elif(fq)>= 1000 and (fq) < 2000:
             self.orm.write('OFLT6')
        elif(fq)>= 2000 and (fq) < 5000:
             self.orm.write('OFLT5')
        elif(fq)>= 5000 and (fq) < 10000:
             self.orm.write('OFLT4')
        elif(fq)>= 10000 and (fq) < 50000:
             self.orm.write('OFLT3')
        elif(fq)>= 50000 and (fq) < 103000:
             self.orm.write('OFLT1')
        else:
             self.orm.write('OFLT8')
        
    def autophase(self):
        pass
    def setPhase(self,phase):
        command= str('PHAS'+str(phase))
        print(command)
        self.orm.write(command)
    def getPhase(self):
        return self.orm.query('OUTP?4')
    def getVoltageY(self,unit = 'v'):
        return self.orm.query('OUTP?2')

class Temp_Controller336:
       
       def __init__(self,adress=1):
            self.ad=RESOURCE_LISTS[adress]
            self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\r',read_termination='\r')
            self.orm.query('C 3')
       def setHighTemp(self,Temp):
            self.orm.write('')
class SIGLENT_FUNCTION_GENERATOR:
      CHANNEL1 = "CH1:"
      CHANNEL2 = "CH2:"
      # WRITE COMMAND ONLY WORK IN DOUBLE QUOTATION
      def __init__(self,adress=0):
        self.ad=RESOURCE_LISTS[adress]
        self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\r',read_termination='\r')
     
      def getVoltage(self,channel):
           return self.orm.query(channel+str("VOLTage?"))
      def getFrequency(self,channel):
           return self.orm.query(channel+str("VOLTage?"))
      
class ITC503_temperature_Controller: 


     def __init__(self,adress=0):
         self.ad=RESOURCE_LISTS[adress]
         self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\r',read_termination='\r')
         self.ramprate = 0
         self.orm.write('$C3')

     def setPointer(self ,X_value,Y_value):
          self.orm.write(f'X{X_value}')
          self.orm.write(f'Y{Y_value}')
     def ResetPointer(self ,pointers):
          self.orm.write(f'X{0}')
          self.orm.write(f'Y{0}')
     def set_SetPoint(self,setpoint):
          self.orm.write(f'$T{setpoint}')
     def set_RampRateM(self ,ramp_rate,vector_array): #Kelvin per minute
           self.ramprate= ramp_rate 
           
           p = mp.Process(target=runProcess, args=(self.orm,vector_array,ramp_rate,))

           return p
     def setSweeps(self, sweep_parameters):
        """Sets the parameters for all sweeps.

        This fills up a dictionary with all the possible steps in
        a sweep. If a step number is not found in the sweep_parameters
        dictionary, then it will create the sweep step with all
        parameters set to 0.

        Args:
            sweep_parameters: A dictionary whose keys are the step
                numbers (keys: 1-16). The value of each key is a
                dictionary whose keys are the parameters in the
                sweep table (see _setSweepStep).
        """
        steps = range(1,17)
        parameters_keys = sweep_parameters.keys()
        null_parameter = {  'set_point' : 0,
                            'sweep_time': 0,
                            'hold_time' : 0  }

        for step in steps:
            if step in parameters_keys:
                self._setSweepStep(step, sweep_parameters[step])
            else:
                self._setSweepStep(step, null_parameter)

     def _setSweepStep(self, sweep_step, sweep_table):
          """Sets the parameters for a sweep step.

          This sets the step pointer (x) to the proper step.
          Then this sets the step parameters (y1, y2, y3) to
          the values dictated by the sweep_table. Finally, this
          resets the x and y pointers to 0.

          Args:
               sweep_step: The sweep step to be modified (values: 1-16)
               sweep_table: A dictionary of parameters describing the
                    sweep. Keys: set_point, sweep_time, hold_time.
          """
          step_setting = '$x{}'.format(sweep_step)
          self.orm.write(step_setting)

          setpoint_setting = '$s{}'.format(
                              sweep_table['set_point'])
          sweeptime_setting = '$s{}'.format(
                              sweep_table['sweep_time'])
          holdtime_setting = '$s{}'.format(
                              sweep_table['hold_time'])

          self.orm.write('$y1')
          self.orm.write(setpoint_setting)

          self.orm.write('$y2')
          self.orm.write(sweeptime_setting)

          self.orm.write('$y3')
          self.orm.write(holdtime_setting)
          #self.orm.write(f'$S{sweep_step}')

          self._resetSweepTablePointers()

     def _resetSweepTablePointers(self):
          """Resets the table pointers to x=0 and y=0 to prevent
               accidental sweep table changes.
          """
          self.orm.write('$x0')
          self.orm.write('$y0')
     def setHeater_Auto(istrue):
          pass
     def set_PID(self,P,I,D):
          self.orm.write(f'$P{P}')
          self.orm.write(f'$I{I}')
          self.orm.write(f'$D{D}')
     def set_SetPointLimit(self):
          pass
     def check_CoolingMaxRate(self ,end_point, start_point):
          pass
     def set_setHeaterLimit(self):
          pass
     def StoreToDefault(self):
          pass
     def setCalibrationTemperature(self):
          pass
     def get_Temperature(self,sensor):
          data = self.orm.query(f'R {sensor}')
          return data[1:]
     def get_setPoint(self):
          return self.orm.query('R 0')                        
     def get_Error(self):
          return self.orm.query('R 4')
     def setTemperature(self,temp):
          self.write(f'$T{temp}')
     def get_RampRate(self):
          
          return self.ramprate
     def get_PID(self):
          return self.orm.query('R 8'),self.orm.query('R 9'),self.orm.query('R 10')
     def get_setPointLimit(self):
          pass
     def updatePID_table(self,row,p,i,d):
          pass
     def getCalibrationTemp(self):
          pass
def runProcess(orm,Vector_array,ramprate):
     f= 310
     for x in  range(20):
          orm.write(f'T {f}')
          time.sleep(ramprate)
          f=f+1

     

class CSV_Writer:
     def __init__(self,number_of_coulmn_in_numpy_array,header_numpy_array):
          pass
     def update(self,values_numpy_array):
          pass
     def close(self):
          pass    




        
     





     
      