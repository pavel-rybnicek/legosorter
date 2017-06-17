'''
    Simple socket server using threads
'''

import io 
import socket
import sys
import time
import struct
from thread import *
from picamera import PiCamera
import numpy as np
 
HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 8001 # Arbitrary non-privileged port

MIN_BRT = 160
MAX_BRT = 170
 
camera = PiCamera(resolution=(640, 480), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = 10000#camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'auto'
camera.awb_gains = g
camera.brightness = 55
camera.contrast = 55

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
#    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    
    my_stream = io.BytesIO()
    #infinite loop so that function do not terminate and thread do not end.
    i = 0
    while True:
         
        #Receiving from client
        print '1 ',time.time()
        data = conn.recv(1024)

        # zkorigujeme jas
        if i > 40:
            adjustBrightness()
            i = 0
        
        camera.capture(my_stream, 'jpeg', use_video_port = True)
       
        filesocket = conn.makefile('wb') 
        
        delka = my_stream.tell()
        filesocket.write(struct.pack('>l', delka))
        filesocket.flush()

        # Rewind the stream and send the image data over the wire
        my_stream.seek(0)
        filesocket.write(my_stream.read())
        filesocket.flush()
        
        # Reset the stream for the next capture
        my_stream.seek(0)
        my_stream.truncate()

        i = i + 1
        
 
    #came out of loop
    conn.close()
 
# srovnani jasu na konstantni uroven
def setBrightness():
    while getBrightness() < MIN_BRT:
        camera.brightness = camera.brightness + 1
    
    while getBrightness() > MAX_BRT:
        camera.brightness = camera.brightness - 1

# srovnani jasu na konstantni uroven
def adjustBrightness():
    currentBrt = getBrightness()
    
    if currentBrt < MIN_BRT:
        camera.brightness = camera.brightness + 1
    elif currentBrt > MAX_BRT:
        camera.brightness = camera.brightness - 1

# zjisti aktualni jas bile plochy
def getBrightness():
    output = np.empty((640 * 480 * 3,), dtype=np.uint8)
    camera.capture(output, 'rgb')
    output = output.reshape((640, 480, 3))
    output = output[70:570, :110, :] 
    currentBrt = np.average(output)
    print currentBrt
    return currentBrt

# nastavime inicialni jas
setBrightness()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
