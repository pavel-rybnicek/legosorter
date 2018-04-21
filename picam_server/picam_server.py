'''
    Simple socket server using threads
'''

import io 
import socket
import sys
import time
import struct
from picamera import PiCamera
from blinkt import set_pixel, set_brightness, show, clear
import numpy as np

 
HOST = 'neurotik.praha12.czf'   # Symbolic name meaning all available interfaces
PORT = 8001 # Arbitrary non-privileged port

def getCamera():
    camera = PiCamera(resolution=(640, 480), framerate=30)
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
    camera.zoom = (0.3, 0.3, 0.5, 0.5)

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
    client_socket.connect(('neurotik.praha12.czf', 8200))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')

    return connection
    
# zapneme svetlo
blinktOn()

# spustíme kameru
camera = getCamera()

# navážeme spojení s neurotikem
connection = getConnection()

try:
    # Construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        print(time.time())
        sendImage(connection, stream)
        print(time.time())
        print("")

finally:
    connection.close()
    client_socket.close()

