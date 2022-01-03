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

SERIALPORT      = "/dev/ttyACM0"
BAUDRATE        = 115200

ser = serial.Serial()
client = mqtt.Client("", True)
queueMessage = []
idMsg = 0
idFire = 0

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
def on_message(client, userdata, msg):
    global idFire
    arr = formatData(msg.payload.decode().split("\n")[:-1])
    for msgToSend in arr :
        queueMessage.append(msgToSend)
        sendUARTMessage(msgToSend)
    idFire += 1

'''
 * adds idFire key to json objects
'''
def formatData(arr):
    global idMsg
    for i in range (len(arr)) :
        jsonElem = json.loads(arr[i])
        jsonElem["idMsg"] = idMsg
        jsonElem["idFire"] = idFire
        arr[i] = json.dumps(jsonElem)
        idMsg += 1
    return arr
'''
 * send message to microcontroller with serial
'''
def sendUARTMessage(msg):
    ser.write(msg.encode())
    print(f"Message <{msg}> sent to micro-controller")
    time.sleep(0.5)

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
    initMQTT()

    print ('Press Ctrl-C to quit.') 
    try:
        print(f"Server started")
        while ser.isOpen() : 
            if (ser.inWaiting() > 0): # if incoming bytes are waiting
                msgReceived = json.loads(readUARTMessage().replace("'", '"')) 

                for elem in queueMessage :
                    jsonElem = json.loads(elem)
                    if str(jsonElem["idMsg"]) == msgReceived["id"] :
                        if msgReceived["status"] == "ACK":
                            queueMessage.remove(elem)
                        elif msgReceived["status"] == "NACK":
                            sendUARTMessage(elem)
                        else:
                            print(msgReceived)
                
    except (KeyboardInterrupt, SystemExit):
        client.disconnect()
        ser.close()
        exit()