'''
 * Program to do things
 * USB tty -> /dev/tty.usbmodem14102
'''

from os import read
import serial
import json
import paho.mqtt.client as mqtt
import time
import re

'''
 * variables for script
'''

SERIALPORT      = "/dev/ttyACM0"
#SERIALPORT      = "COM3"
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
def on_message(client, userdata, msg):
    arr = formatData(msg.payload.decode().split("\n")[:-1]) # Data received looks like : "{data1}\n{data2}...\n", so the received data is splitted on the "\n" char and the last entry is removed
    for msgToSend in arr :
        queueMessage.append(msgToSend)

'''
 * adds idFire key to json objects
'''
def formatData(arr):
    for i in range (len(arr)) :
        arr[i] += "|||" + str(calculateChecksum(arr[i])) # Add a checksum at the end of every message
    return arr

'''
 * calculate checksum for a given message
'''
def calculateChecksum(message):
        nleft = len(message)
        sum = 0
        pos = 0
        while nleft > 1:
            sum = ord(message[pos]) * 256 + (ord(message[pos + 1]) + sum)
            pos = pos + 2
            nleft = nleft - 2
        if nleft == 1:
            sum = sum + ord(message[pos]) * 256

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum += (sum >> 16)
        sum = (~sum & 0xFFFF)

        return sum

'''
 * send message to microcontroller with serial
'''
def sendUARTMessage(msg):
    ser.write(msg.encode())
    print(f"Message <{msg}> sent to micro-controller")

'''
 * receive message from serial
'''
def readUARTMessage():
    msg = ser.readline() # The data needs to end with "\n", we should setup a timeout to take care of potential issues
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
            for msg in queueMessage : # Makes sure every message is sent one by one, and if something went wrong will resend the data. No timeouts made as of now
                sendUARTMessage(msg) # Send msg and start a while loop as per to wait an ACK from the microbit
                status = "NACK"
                start = time.time() # Start a timer to resend the data every 2 second if nothing is happening
                while status == "NACK" :
                    if (time.time() - start) > 2 :
                        sendUARTMessage(msg)
                        start = time.time()
                    elif (ser.inWaiting() > 0): # If incoming bytes are waiting
                        data = readUARTMessage()
                        if data != None :
                            if re.search("^ACK", data) :
                                queueMessage.remove(msg)
                                print(f"Message <{msg}> removed from the queue")
                                status = "ACK"
                        else :
                            sendUARTMessage(msg)
                            start = time.time()
    except (KeyboardInterrupt, SystemExit):
        client.disconnect()
        ser.close()
        exit()