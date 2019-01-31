# slouží ke sbírání obrázků
# uchovává fotky dílů, které jsou přiměřeně uprostřed

# počítá se s tím, že díly jsou stejného typu

import sys
sys.path.insert(0, '/home/pryb/fastai')

# This file contains all the main external libs we'll use
from fastai.imports import *

from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *

from fastailib import *

import io
import socket
import struct
from PIL import Image
import numpy

PATH_TO_MODEL="/home/pryb/data/brick/"
MODEL='224_brick_all'



def getListenningSocket():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8201))
    server_socket.listen(0)

    return server_socket

def readOpenCvImageFromClient(): # TODO redundantní funkce
    # Read the length of the image as a 32-bit unsigned int. If the
    # length is zero, quit the loop
    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]

    # Construct a stream to hold the image data and read the image
    # data from the connection
    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))
    # Rewind the stream, open it as an image with PIL and do some
    # processing on it
    image_stream.seek(0)

    return Image.open(image_stream)


(learn, val_tfms) = initNeuralNetwork(PATH_TO_MODEL, MODEL)

server_socket = getListenningSocket()

try:
    while True:
        # Accept a single connection and make a file-like object out of it
        socket = server_socket.accept()[0]
        connection = socket.makefile('rb')
        img = readOpenCvImageFromClient()
        
        (classification, predictions) = classifyImage(learn, val_tfms, img) 
        if 0 < classification:
          # na obrázku něco je, zjistíme, jestli je to uprostřed
          imgCropped = cropOpencvImage (img)
          (classificationCropped, predictionsCropped) = classifyImage (learn, val_tfms, imgCropped)
          if 0 < classificationCropped:
            # ano, je to uprostřed. Uložíme obrázek.
            imgCropped.save('grabbed/g_%f.jpg' % (classificationIndex, time.time()), "JPEG")
  
        # od pusheru se nevyžaduje žádná akce, jenom sbíráme obrázky 
        conn2=socket.makefile('wb')
        conn2.write(struct.pack('<L', 0))
        conn2.flush()

        connection.close()
        conn2.close()

finally:
    server_socket.close()
