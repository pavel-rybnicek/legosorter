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
MODEL='224_brick_last'



(learn, val_tfms) = initNeuralNetwork(PATH_TO_MODEL, MODEL)

server_socket = getListenningSocket()

try:
    while True:
        # Accept a single connection and make a file-like object out of it
        socket = server_socket.accept()[0]
        connection = socket.makefile('rb')
        img = readOpenCvImageFromClient()
        
        classification = classifyAndSaveImage(learn, val_tfms, img) 
        print(classification)
        sendClassification (classification)
       
        connection.close()

finally:
    server_socket.close()
