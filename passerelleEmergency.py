'''
 * Program to do things
 * USB tty -> /dev/tty.usbmodem14102
'''

import serial
import json
import time
import paho.mqtt.client as mqtt


'''
 * variables for script
'''

SERIALPORT      = "COM6"
BAUDRATE        = 115200

ser = serial.Serial()
client = mqtt.Client("", True)

# -------------------- Functions -------------------- #
'''
 * init mqtt
'''
def initMQTT():
    client.connect("127.0.0.1", 1883, 60)
    client.on_connect = on_connect
    client.loop_start()

'''
 * function on connect for mqtt broker
'''
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))


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
    #initUART()
    initMQTT()
    
    print ('Press Ctrl-C to quit.')

    client.publish("python/test", 'ar')
    client.publish("python/test", '{"test": 34}')

    try:
        print(f"Server started")
        while ser.isOpen() : 
            if (ser.inWaiting() > 0): # if incoming bytes are waiting
                print(readUARTMessage())
                client.publish("python/test", readUARTMessage())
    except (KeyboardInterrupt, SystemExit):
        client.disconnect()
        ser.close()
        exit()