import serial, time

# initialization and open the port

# possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

dPort = serial.Serial()
dPort.port = "/dev/cu.usbserial-DA00XTF4"
# ser.port = "/dev/ttyS2"
dPort.baudrate = 115200
dPort.bytesize = serial.EIGHTBITS  # number of bits per bytes
dPort.parity = serial.PARITY_NONE  # set parity check: no parity
dPort.stopbits = serial.STOPBITS_ONE  # number of stop bits
# ser.timeout = None          #block read
dPort.timeout = 1            #non-block read
# ser.timeout = 2              #timeout block read
dPort.xonxoff = serial.XON  # disable software flow control
dPort.rtscts = False  # disable hardware (RTS/CTS) flow control
dPort.dsrdtr = False  # disable hardware (DSR/DTR) flow control
dPort.writeTimeout = 2     #timeout for write


try:
    dPort.open()
except Exception as e:
    print("error open serial port: " + str(e))
    exit()

if dPort.isOpen():

    try:
        # dPort.flushInput() #flush input buffer, discarding all its contents
        # dPort.flushOutput()#flush output buffer, aborting current output
        # and discard all that is in buffer

        # write data
        dPort.write(bytes('$ex=1', 'ascii'))
        print("write data: $ex=1")

        # time.sleep(0.5)  # give the serial port sometime to receive the data

        numOfLines = 0

        while numOfLines <= 5:
            response = dPort.readlines()
            print("read data: " + str(response))
            numOfLines = numOfLines + 1

        dPort.close()
    except Exception as e1:
        print("error communicating...: " + str(e1))

else:
    print("cannot open serial port ")
