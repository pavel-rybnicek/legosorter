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

def initNeuralNetwork():
    PATH = "/home/pryb/data/brick/"
    sz=224

    arch=resnet34
    data = ImageClassifierData.from_paths(PATH, tfms=tfms_from_model(arch, sz))
    learn = ConvLearner.pretrained(arch, data, precompute=True)
    learn.load('224_lastlayer')
    print('start')
    filename='/home/pryb/fastai/courses/dl1/data/brick/test1/a3.jpg'
    trn_tfms, val_tfms = tfms_from_model(resnet34, sz, aug_tfms = transforms_side_on, max_zoom = 1.1)
    return learn, val_tfms

def getListenningSocket():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8200))
    server_socket.listen(0)

    return server_socket

def readImageFromClient():
    # Read the length of the image as a 32-bit unsigned int. If the
    # length is zero, quit the loop
    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
    #if not image_len:
                    #break
    # Construct a stream to hold the image data and read the image
    # data from the connection
    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))
    # Rewind the stream, open it as an image with PIL and do some
    # processing on it
    image_stream.seek(0)

    return Image.open(image_stream)

def classifyImage(learn, val_tfms, image):
    image2.save("out.jpg", "JPEG")
    im= val_tfms(open_image('out.jpg'))
    learn.precompute=False
    pred1 = learn.predict_array(im[None])
    prob = np.argmax(np.exp(pred1))

    return prob


(learn, val_tfms) = initNeuralNetwork()

server_socket = getListenningSocket()

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        image2 = readImageFromClient()
        
        #image = image2.convert('RGB')
        #open_cv_image = numpy.array(image)
        #open_cv_image = open_cv_image[:, :, ::-1].copy()
        #print('Image is %dx%d' % image.size)
        #image.verify()
        #print('Image is verified')

        classification = classifyImage(learn, val_tfms, image2) 
        print(classification)

finally:
    connection.close()
    server_socket.close()
