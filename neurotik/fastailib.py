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

def cropOpenCvImage (img):
    width, height = img.shape[:2]
    
    wt = width//3
    ht = height//3
    
    imgCropped = img[wt:wt*2, ht:ht*2]
    return imgCropped

def readOpenCvImageFromClient(): 
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

def getListenningSocket():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8201))
    server_socket.listen(0)

    return server_socket

def sendClassification (socket, classification)
        conn2=socket.makefile('wb')
        conn2.write(struct.pack('<L', classification))
        conn2.flush()
        conn2.close()

def isImageCentered(learn, val_tfms, img)
    # vyřízneme střed
    imgCropped = cropImage(img)
        
    # klasifikujeme střed
    (classificationCropped, predictionsCropped) = classifyImage (learn, val_tfms, imgCropped)
        
    if (classificationCropped == 0) and ( -0.1 < predictionsCropped[0,classificationCroppenCropped]):
        return False
    return True
    
