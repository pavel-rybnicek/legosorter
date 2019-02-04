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

PATH_TO_MODEL="/home/pryb/data/color/"
MODEL='224_color'



(learn, val_tfms) = initNeuralNetwork(PATH_TO_MODEL, MODEL)

server_socket = getListenningSocket()

try:
    while True:
        # Accept a single connection and make a file-like object out of it
        socket = server_socket.accept()[0]
        img = readImageFromClient(socket)
        
        imgCv = imageToOpenCv (img)
 
        # budeme se zabývat pouze vycentrovanými obrázky
        if isImageCentered (learn, val_tfms, imgCv):
          
          (classificationIndex, predictions) = classifyImage(learn, val_tfms, imgCv) 
          if 0 < classificationIndex:
            # na obrázku něco je, bere to
            img.save('grabbed/g_%f.jpg' % (time.time()), "JPEG")
    
        # od pusheru se nevyžaduje žádná akce, jenom sbíráme obrázky 
        sendClassification (socket, 0)

finally:
    server_socket.close()
