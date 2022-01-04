'''
 * Program to do things
 * USB tty -> /dev/tty.usbmodem14102
'''

import serial
import json
import time

'''
 * variables for script
'''

SERIALPORT      = "COM5"
BAUDRATE        = 115200

ser = serial.Serial()

# -------------------- Functions -------------------- #
'''
 * init serial mode
'''
def initUART():        
    ser.port = SERIALPORT
    ser.baudrate = BAUDRATE
    ser.bytesize = serial.EIGHTBITS         # number of bits per bytes
    ser.parity = serial.PARITY_NONE         # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE      # number of stop bits
    ser.timeout = None                      # block read
    ser.xonxoff = False                     # disable software flow control
    ser.rtscts = False                      # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False                      # disable hardware (DSR/DTR) flow control
    
    try:
        ser.open()
        print("Starting Up Serial Monitor")
    except serial.SerialException as e:
        print(f"Serial {SERIALPORT} port not available")
        exit()

'''
 * send message to microcontroller with serial
'''
def sendUARTMessage(msg):
    ser.write(msg)
    print(f"Message <{msg.decode()}> sent to micro-controller")

'''
 * receive message from serial
'''
def readUARTMessage():
    msg = ser.readline()
    packet = msg.decode()
    return packet

'''
 * main program logic follows:
'''
if __name__ == '__main__':
    initUART()
    elem = ""
    msgReceived = ""

    print ('Press Ctrl-C to quit.')

    try:
        print(f"Server started")
        
        while ser.isOpen() : 
            if (ser.inWaiting() > 0): # if incoming bytes are waiting
                while elem != "\n":
                    elem = ser.read(1)
                    msgReceived += elem
                print(msgReceived)
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        exit()