import numpy as np
import matplotlib.pyplot as plt
import pyvisa as pv
KILO = 1000
RESOURCE_LISTS = pv.ResourceManager().list_resources()

class SR830LockIn_interface:
    
    def __init__(self,adress=0):
        self.ad=RESOURCE_LISTS[adress]
        self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\n',read_termination='\n')
        
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
         return self.orm.query('OUTP?3')
    def getVoltageX(self,unit = 'v'):
         return self.orm.query('OUTP?1')
    def autoSensetivity(self):
        vr = float(self.getVoltageR())
        if (vr)>= 0.2 and (vr)< 0.5 :
            self.orm.write('SENS25')
        elif(vr)>= 0.1 and (vr) < 0.2:
             self.orm.write('SENS24')
        elif(vr)>= 0.02 and (vr) < 0.05:
             self.orm.write('SENS23')
        elif(vr)>= 0.01 and (vr) < 0.02:
             self.orm.write('SENS22')
        elif(vr)>= 0.005 and (vr) < 0.01:
             self.orm.write('SENS21')
        elif(vr)>= 0.002 and (vr) < 0.005:
             self.orm.write('SENS19')
        elif(vr)>= 0.001 and (vr) < 0.002:
            self.orm.write('SENS19')
        elif(vr)>= 0.0002 and (vr) < 0.001:
             self.orm.write('SENS17')
        elif(vr)>= 0 and (vr) < 0.0001:
             self.orm.write('SENS15')
        else:
             self.orm.write('SENS26')
            

        
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
            self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\n',read_termination='\n')
       def setHighTemp(self,Temp):
            self.orm.write('')
class SIGLENT_FUNCTION_GENERATOR:
      CHANNEL1 = "CH1:"
      CHANNEL2 = "CH2:"
      # WRITE COMMAND ONLY WORK IN DOUBLE QUOTATION
      def __init__(self,adress=0):
        self.ad=RESOURCE_LISTS[adress]
        self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\n',read_termination='\n')
     
      def getVoltage(self,channel):
           return self.orm.query(channel+str("VOLTage?"))
      def getFrequency(self,channel):
           return self.orm.query(channel+str("VOLTage?"))
      
     
     
      