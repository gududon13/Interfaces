import pyvisa as pv
import time
import csv
import bhavtoshlab_11 as bl

def setTemp(elf,Temp):
    return elf.write(f'SETP1, {Temp}\r')


def getTemp(elf):
    return elf.query("KRDG? 0\r")
def setRamp(elf,output=1,ramp_value=1):
    return elf.write(f'RAMP {output},1,{ramp_value}\r')
def convertor(x):
    L = ['0','1','2','3','4','5','6','7','8','9','.','E','+']
    String = ''
    for i in x:
        if i in L:
            String += i
    return String
def close(elf):
    elf.close()

RESOURCE_LISTS = pv.ResourceManager().list_resources()
print(RESOURCE_LISTS)

Lockincu = bl.SR830LockIn_interface(3)
Lockincv = bl.SR830LockIn_interface(5)
R = 5283

# Set up GPIB connection to instrument
rm = pv.ResourceManager()
Address = input('Address of GPIB')
SR336 = rm.open_resource('GPIB0::'+Address +'::INSTR')
print(SR336.query('*IDN?'))

current_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
csv_filename = f"FOUR PROBE {current_time}.csv"
csv_file = open(csv_filename, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'Temp','Vx','Vy','Vr','theta','Ix','Iy','Ir','Itheta','R'])

InitialTime = time.time()
VariableTime = 0
Temperature = getTemp(SR336)
Assure = input('Proceed?')
setTemp(SR336,296)
upPointer=0
downPointer=0

up_array=[380,380,380,380,380,380,380,380,380,380,380,380,380,380,380,380,380,380,380,380]
down_array=[296,296,296,296,296,296,296,296,296,296,296,296,296,296,296,296,296,296,296,296]

Converge = []

for i in range(len(up_array)):
    Converge.append(down_array[i])
    Converge.append(up_array[i])

SetTempFlag = True
Direction = 1 #cooling is 1, 2 is heating
FluctuationFlag = True

Pointer = 0

for i in range(15):
     Lockincv.getSnap()
for i in range(15):
      Lockincu.getSnap()

try:
    while True:#VariableTime < 36000:
        
        # responselockinVx = convertor(Lockincv.getVoltageX())
        # responselockinVy = convertor(Lockincv.getVoltageY())
        # responselockinVr = convertor(Lockincv.getVoltageR())
        # responselockintheta = convertor(Lockincv.getPhase())
        vxyrt=Lockincv.getSnap()
        vx, vy, vr, vtheta = map(float, vxyrt.split(','))

        # responselockinIx = float(convertor(Lockincu.getVoltageX()))
        # responselockinIy = float(convertor(Lockincu.getVoltageY()))
        # responselockinIr = float(convertor(Lockincu.getVoltageR()))
        # responselockinItheta = convertor(Lockincu.getPhase())
        ixyrt=Lockincu.getSnap()
        ix, iy, ir, itheta = map(float, ixyrt.split(','))
       # resistance= float(responselockinVr)/(responselockinIr/R)

        VariableTime = time.time()-InitialTime
        Temperature = convertor(getTemp(SR336))
        csv_writer.writerow([VariableTime,  Temperature ,(float(vx)),(float(vy)),(float(vr)),(float(vtheta)) ,(float(ix)),(float(iy)),(float(ir)),(float(itheta)), ((vr*5288/ir))])
       # csv_writer.writerow([VariableTime,  Temperature ,vxyrt ,ixyrt, ((21))])


        if eval(Temperature) < 380 and eval(Temperature) > 296:
            FluctuationFlag = True
        else:
            FluctuationFlag = False

        if Direction == 1 and eval(Temperature) < Converge[Pointer] + 1 and SetTempFlag and FluctuationFlag:
            Pointer += 1
            SetTempFlag = False
            Direction = 2
            setTemp(SR336,Converge[Pointer])

        elif Direction == 2 and eval(Temperature) > Converge[Pointer] - 1 and SetTempFlag and FluctuationFlag:
            Pointer += 1
            SetTempFlag = False
            Direction = 1
            setTemp(SR336,Converge[Pointer])
        else:
            pass
        
        if not SetTempFlag:
            if Direction == 2 and eval(Temperature) > Converge[Pointer - 1] + 2:
                SetTempFlag =True
            elif Direction == 1 and eval(Temperature) < Converge[Pointer - 1] - 2:
                SetTempFlag =True
            else:
                pass
        
        Lockincu.autoSensetivity((ir))
        Lockincv.autoSensetivity((vr))
       


except KeyboardInterrupt:
    print("\nLoop stopped by user.")


finally:
    # Close CSV file and instrument connection
    csv_file.close()
    print("CSV file closed and instrument connection closed.")
    Lockincu.orm.write('SENS26\r')
    Lockincv.orm.write('SENS26\r')
    Lockincu.close()
    Lockincv.close()
    close(SR336)
    





