# coding=UTF-8
import io 
import socket
import sys
import time
import struct
from optparse import OptionParser
from picamera import PiCamera
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np
from nxtPusher import *

from Queue import PriorityQueue
from threading import Thread

pushQueue = PriorityQueue()

HOST = '72.52.111.156'   # Symbolic name meaning all available interfaces
PORT = 8001 # Arbitrary non-privileged port

CLASSIFICATION_NONE = 0

WINDOW_SIZE = 0.03

MOTOR_A_DELAY = 1.2
MOTOR_B_DELAY = 2.7
MOTOR_C_DELAY = 4.4

MOTOR_ROTATION=36*5/3

def queueProcessor(queue):
    brick, motorControl = nxt_init()
    try:
        while stillRunning:
            pushEvent = queue.get()
            time.sleep(.01)
            queue.task_done()
            
            timeToNext = pushEvent[0] - time.time()
            if timeToNext > WINDOW_SIZE:
                queue.put(pushEvent)
                continue

            if timeToNext > 0:
                nxt_push(motorControl, pushEvent[1])
    finally:
        print('Trying to stop MotorControl')
        brick.stop_program()

def getCamera():
    camera = PiCamera(resolution=(480, 480), framerate=30)
    # Set ISO to the desired value
    camera.iso = 100
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = 10000
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'auto'
    camera.awb_gains = g
    camera.zoom = (0.43, 0.43, 0.29, 0.29)

    return camera

# zapneme blinkt naplno
def blinktOn():
    set_brightness(1)
    clear()
    set_pixel(0, 255, 255, 255)
    set_pixel(1, 255, 255, 255)
    set_pixel(2, 255, 255, 255)
    set_pixel(3, 255, 255, 255)
    set_pixel(4, 255, 255, 255)
    set_pixel(5, 255, 255, 255)
    set_pixel(6, 255, 255, 255)
    set_pixel(7, 255, 255, 255)
    show()

# pošle obrázek ve streamu na server
def sendImage( connection, stream ):
    # Write the length of the capture to the stream and flush to
    # ensure it actually gets sent
    connection.write(struct.pack('<L', stream.tell()))
    connection.flush()

    # Rewind the stream and send the image data over the wire
    stream.seek(0)
    connection.write(stream.read())
    
    # Reset the stream for the next capture
    stream.seek(0)
    stream.truncate()

def getConnection():
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket = socket.socket()
    client_socket.connect(('localhost', 8201))

    # Make a file-like object out of the connection
    connection_write = client_socket.makefile('wb')
    connection_read  = client_socket.makefile('rb')

    return connection_read, connection_write
   
def putToQueue (queue, time, classification):
    if CLASSIFICATION_NONE == classification:
        return;

    if 1 == classification:
        event = (time + MOTOR_A_DELAY, classification)
    if 2 == classification:
        event = (time + MOTOR_A_DELAY, classification)
    if 3 == classification:
        event = (time + MOTOR_B_DELAY, classification)
    if 4 == classification:
        event = (time + MOTOR_B_DELAY, classification)
    if 5 == classification:
        event = (time + MOTOR_C_DELAY, classification)
    if 6 == classification:
        event = (time + MOTOR_C_DELAY, classification)
    if 7 == classification:
        event = (time + MOTOR_C_DELAY, 5)
    if 8 == classification:
        event = (time + MOTOR_C_DELAY, 6)
    if 9 == classification:
        event = (time + MOTOR_C_DELAY, 6)
    pushQueue.put(event)

# zpracujem příkazovou řádku
parser = OptionParser()
parser.add_option("--dry-run", action="store_true", dest="dryRun") # nepokusi se spustit NXT
(options, args) = parser.parse_args()

# nastavíme semafor pro běh
stillRunning = True

# zapneme svetlo
blinktOn()

# spustíme kameru
camera = getCamera()

# spustíme frontu zpracování, pokud to není dry run
if not options.dryRun:
    worker = Thread(target=queueProcessor, args=(pushQueue,))
    worker.setDaemon(True)
    worker.start()

try:
    # Construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        imageTime = time.time()
        #print(time.time())
        # navážeme spojení s neurotikem
        (connection_read, connection) = getConnection()

        sendImage(connection, stream)
        
        classification = struct.unpack('<L', connection_read.read(struct.calcsize('<L')))[0]
        
        putToQueue(pushQueue, imageTime, classification)

        connection.close()
        connection_read.close()

        #print(time.time())
        #print(classification)
        #print("")

except KeyboardInterrupt:
    stillRunning = False
    time.sleep(1)
    client_socket.close()

