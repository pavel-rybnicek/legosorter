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

import io
import socket
import struct
from PIL import Image
import numpy

def initNeuralNetwork(pathToModel, model):
    PATH = "/home/pryb/data/brick/"
    sz=224

    arch=resnet34
    data = ImageClassifierData.from_paths(pathToModel, tfms=tfms_from_model(arch, sz))
    learn = ConvLearner.pretrained(arch, data, precompute=False) # TODO prověřit to precompute
    learn.load(model)
    print('start')
    trn_tfms, val_tfms = tfms_from_model(resnet34, sz, aug_tfms = transforms_side_on, max_zoom = 1.1)
    return learn, val_tfms

def classifyImage(learn, val_tfms, image):
    #image.save("out.jpg", "JPEG")
    
    # prevedeme na openCV
    imageCV = numpy.array(image.convert('RGB'))
    imageCV = imageCV[:, :, ::-1].copy()

    im= val_tfms(imageCV.astype(np.float32)/255)

    # predictions are log scale - 0 would be 100% sure
    predictions = learn.predict_array(im[None])
    
    classificationIndex = np.argmax(np.exp(predictions))

    return classificationIndex, predictions

def classifyAndSaveImage(learn, val_tfms, image):
    ( classificationIndex, predictions ) = classifyImage (learn, val_tfms, image)
    
    if -0.1 > predictions[0,classificationIndex]:
        # uncertain
        print(predictions)
        image.save('unknown/%d_%f.jpg' % (classificationIndex, time.time()), "JPEG")
        classificationIndex = 0
    else:
        if classificationIndex > 0:
            image.save('%d/%d_%f.jpg' % (classificationIndex, classificationIndex, time.time()), "JPEG")

    return classificationIndex

def grabImage (learn, val_tfms, image):
    ( classificationIndex, predictions ) = classifyImage (learn, val_tfms, image)
    
    if -0.1 > predictions[0,classificationIndex]:
        # uncertain
        print(predictions)
        image.save('unknown/%d_%f.jpg' % (classificationIndex, time.time()), "JPEG")
        classificationIndex = 0
    else:
        if classificationIndex > 0:
            image.save('%d/%d_%f.jpg' % (classificationIndex, classificationIndex, time.time()), "JPEG")

    return classificationIndex

def cropOpencvImage (img):
    width, height = img.shape[:2]
    
    wt = width//3
    ht = height//3
    
    imgCropped = img[wt:wt*2, ht:ht*2]
    return imgCropped
