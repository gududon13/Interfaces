import numpy as np
import matplotlib.pyplot as plt
import pyvisa as pv

RESOURCE_LISTS = pv.ResourceManager().list_resources()

class SR830LockIn_interface:
    
    def __init__(self,adress=0):
        self.ad=RESOURCE_LISTS[adress]
        self.orm= pv.ResourceManager().open_resource(self.ad,write_termination = '\n',read_termination='\n')
        
    def setInputVoltage(self,voltage):
        if(voltage <= 0.6):
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
    def autoSensetivity(self):
        pass
    def autoTimeConstant(self):
        pass
    def autophase(self):
        pass
    def setPhase(self,phase):
        command= str('PHAS'+str(phase))
        print(command)
        self.orm.write(command)
    def getPhase(self):
        return self.orm.query('OUTP?4')

    