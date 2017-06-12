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
 
HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 8001 # Arbitrary non-privileged port
 
camera = PiCamera(resolution=(640, 480), framerate=30)
# Set ISO to the desired value
camera.iso = 800
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = 10000#camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'auto'
camera.awb_gains = g

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
    while True:
         
        #Receiving from client
        print '1 ',time.time()
        data = conn.recv(1024)
        print '2 ',time.time()
        
        camera.capture(my_stream, 'jpeg', use_video_port = True)
        print '3 ',time.time()
       
        filesocket = conn.makefile('wb') 
        print '4 ',time.time()
        delka = my_stream.tell()
        print '5 ',time.time()
        filesocket.write(struct.pack('>l', delka))
        filesocket.flush()
        print '6 ',time.time()

        # Rewind the stream and send the image data over the wire
        my_stream.seek(0)
        filesocket.write(my_stream.read())
        filesocket.flush()
        print '7 ',time.time()
        # Reset the stream for the next capture
        my_stream.seek(0)
        my_stream.truncate()
        print '8 ',time.time()
 
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
