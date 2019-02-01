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
MODEL='224_brick_last'
INPUTDIR="../data_pokus/train/"
OUTPUTDIR="../"

def ulozStredObazku
    

(learn, val_tfms) = initNeuralNetwork(PATH_TO_MODEL, MODEL)

for root, dirs, files in os.walk(PATH_IMAGES):
    for name in files:
        # přečteme obrázek
        image_name = os.path.join(root, name)
        img = open_image(image_name)

        # uděláme si kopii ořezu pro uložení na disk
        imgg = Image.open(image_name)
        width, height = image.shape[:2]
        wt = width//3
        ht = height//3
        box = (wt, ht, wt*2, ht*2)
        area = imgg.crop(box)
        
        targetdir = "centrovane"
        if isImageCentered (learn, val_tfms, img):
            # nic tam neni a jsme si fakt jistý
            targetdir = "necentrovane"
        
        os.remove(image_name, ("../%s/" % targetdir) )
        area.save("../%s_orez/%s" % (targetdir, basename), 'jpeg')
            
