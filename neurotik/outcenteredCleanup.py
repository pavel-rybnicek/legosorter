# roztřídí obrázky na centrované a necentrované
# prochází rekurzivně do podadresářů
# slouží k vyčištění nasbíraných obrázků

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
WORKDIR="/home/pryb/data_cleanup/"
INPUTDIR="%ssource/" % WORKDIR
OUTPUTDIR_OUTCENTERED="%soutcentered/" % WORKDIR
OUTPUTDIR_OUTCENTERED_CROPPED="%soutcentered_crop/" % WORKDIR

(learn, val_tfms) = initNeuralNetwork(PATH_TO_MODEL, MODEL)

for root, dirs, files in os.walk(INPUTDIR):
    for name in files:
        # přečteme obrázek
        image_name = os.path.join(root, name)
        img = Image.open(image_name)
        imgOpenCv = imageToOpenCv(img)

        # uděláme si kopii ořezu pro uložení na disk
        imgCropped = cropImage (img)
        print (image_name) 
        # když není centrovaný, vyřadíme 
        if not(isImageCentered (learn, val_tfms, imgOpenCv)):
            # nic tam neni a jsme si fakt jistý
            os.rename(image_name, ("%s%s" % (OUTPUTDIR_OUTCENTERED, name)) )
            imgCropped.save("%s%s" % (OUTPUTDIR_OUTCENTERED_CROPPED, name), 'jpeg')
            print ("neberu")
        else:
            print ("beru")
            
