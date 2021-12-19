'''
 * Program to do things
 * USB tty -> /dev/tty.usbmodem14102
'''

import serial
import json
import paho.mqtt.client as mqtt
import time

'''
 * variables for script
'''

FILENAME        = "values.txt"
LAST_VALUE      = "deadbeef"
SERIALPORT      = "COM4"
BAUDRATE        = 115200

ser = serial.Serial()
client = mqtt.Client("", True)
queueMessage = []

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
 * init mqtt
'''
def initMQTT():
    client.connect("127.0.0.1", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()

'''
 * function on connect for mqtt broker
'''
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/detectors")

'''
 * function on message for mqtt broker
'''
def on_message(client, userdata, msg): # MANQUE LA LOGIQUE DE VERIF DES MESSAGES POUR RENVOYER ET TOUT
    #queueMessage.append(msg.payload)
    print(msg.payload)
    sendUARTMessage(msg.payload)
    '''
    for i in range (5):
        msgRcvd = readUARTMessage()
        if (msgRcvd == "MESSAGE_SUCCESS"):
            queueMessage.pop(0)
            return 1
        else:
            time.sleep(0.5)
    print("TIMEOUT for msg : <{queueMessage[0]}>")
    queueMessage.pop(0)
    '''

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
    ser.flush()
    packet = msg.decode()
    return packet

'''
 * main program logic follows:
'''
if __name__ == '__main__':
    initUART()
    initMQTT()

    print ('Press Ctrl-C to quit.')

    try:
        print(f"Server started")
        
        while ser.isOpen() : 
            if (ser.inWaiting() > 0): # if incoming bytes are waiting
                print(readUARTMessage())
    except (KeyboardInterrupt, SystemExit):
        client.disconnect()
        ser.close()
        exit()