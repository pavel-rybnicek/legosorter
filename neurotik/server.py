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
import _thread

PATH_TO_MODEL="/home/pryb/data/color/"
MODEL='224_color'

def processRequest (socket):
    img = readImageFromClient(socket)
       
    classification = classifyAndSaveImage(learn, val_tfms, img) 
    print(classification)
    sendClassification (socket, classification)
    socket.close()

(learn, val_tfms) = initNeuralNetwork(PATH_TO_MODEL, MODEL)

server_socket = getListenningSocket()

try:
    while True:
        # Accept a single connection and make a file-like object out of it
        socket = server_socket.accept()[0]

        _thread.start_new_thread(processRequest, (socket, ))
       
finally:
    server_socket.close()
