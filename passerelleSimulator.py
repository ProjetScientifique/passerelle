'''
 * Program to do things
 * USB tty -> /dev/tty.usbmodem14102
'''

import serial
import json

'''
 * variables for script
'''

FILENAME        = "values.txt"
LAST_VALUE      = "deadbeef"
SERIALPORT      = "/dev/tty.usbmodem14102"
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
    except serial.SerialException:
        print(f"Serial {SERIALPORT} port not available")
        exit()

'''
 * send message to microcontroller with serial
'''
def sendUARTMessage(msg):
    ser.write(msg)
    print(f"Message <{msg.decode()}> sent to micro-controller")

'''
* get values of triggered detectors from db
'''
def getTriggeredDetectors():
    return json.dumps(
        {
            "Detectors": [
                {
                    "latitude_capteur": 0,
                    "longitude_capteur": 0,
                    "nom_capteur": None,
                    "id_capteur":0
                },
                {
                    "latitude_capteur": 0,
                    "longitude_capteur": 0,
                    "nom_capteur": None,
                    "id_capteur":1
                },
                {
                    "latitude_capteur": 0,
                    "longitude_capteur": 0,
                    "nom_capteur": None,
                    "id_capteur":2
                },
                {
                    "latitude_capteur": 0,
                    "longitude_capteur": 0,
                    "nom_capteur": None,
                    "id_capteur":3
                }
            ]
    })

'''
 * main program logic follows:
'''
if __name__ == '__main__':
    #initUART()

    print ('Press Ctrl-C to quit.')

    try:
        print(f"Server started")
        # TODO
        print(getTriggeredDetectors())
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        # f.close()
        ser.close()
        exit()