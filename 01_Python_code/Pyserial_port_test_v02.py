import serial
import serial.tools.list_ports as lp

import serial.tools.list_ports_osx as lpo

# from serial.tools import list_ports_osx

# x = type(lp.comports())
x = lp.main()

print(x)

# for port, desc, hwid in sorted(lpo.comports()):
#     print("{}: {} [{}]".format(port, desc, hwid))

portName = "/dev/cu.usbserial-DA00XTF4"
baudRate = 115200
byteSize = serial.EIGHTBITS
paritY = serial.PARITY_NONE
stopbitS = serial.STOPBITS_ONE
xonxofF = True

dPort = serial.Serial()
