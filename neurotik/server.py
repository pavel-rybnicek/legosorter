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

RESULTS = "/home/pryb/results/"

def initNeuralNetwork():
    PATH = "/home/pryb/data/brick/"
    sz=224

    arch=resnet34
    data = ImageClassifierData.from_paths(PATH, tfms=tfms_from_model(arch, sz))
    learn = ConvLearner.pretrained(arch, data, precompute=False)
    learn.load('224_brick_last')
    print('start')
    trn_tfms, val_tfms = tfms_from_model(resnet34, sz, aug_tfms = transforms_side_on, max_zoom = 1.1)
    return learn, val_tfms, data.classes

def initDirs(classes):
    shutil.rmtree(RESULTS, ignore_errors=True)
    os.mkdir(RESULTS) 
    os.mkdir('%s%s' % (RESULTS, "unknown")) 
    for x in range(0, len(classes) - 1):
        os.mkdir('%s%s' % (RESULTS, classes[x])) 

def getListenningSocket():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8201))
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

def classifyImage(classes, learn, val_tfms, image):
    #image.save("out.jpg", "JPEG")
    
    # prevedeme na openCV
    imageCV = numpy.array(image.convert('RGB'))
    imageCV = imageCV[:, :, ::-1].copy()

    im= val_tfms(imageCV.astype(np.float32)/255)
    #im= val_tfms(open_image('out.jpg'))
    # netreba, uz bylo nastaveno. TODO navic by melo byt true learn.precompute=False
    pred1 = learn.predict_array(im[None])
    prob = np.argmax(np.exp(pred1))
    # predictions are log scale - 0 would be 100% sure
    if -0.1 > pred1[0,prob]:
        print(pred1)
        image.save('%sunknown/%d_%f.jpg' % (RESULTS, prob, time.time()), "JPEG")
        prob = 0
    else:
        if prob > 0:
            image.save('%s%s/%d_%f.jpg' % (RESULTS, classes[prob], prob, time.time()), "JPEG")

    return prob


(learn, val_tfms, classes) = initNeuralNetwork()

initDirs(classes)

server_socket = getListenningSocket()

try:
    while True:
        # Accept a single connection and make a file-like object out of it
        socket = server_socket.accept()[0]
        connection = socket.makefile('rb')
        img = readImageFromClient()
        
        classification = classifyImage(classes, learn, val_tfms, img) 
        print(classification)
       
        conn2=socket.makefile('wb')
        conn2.write(struct.pack('<L', classification))
        conn2.flush()

        connection.close()
        conn2.close()

finally:
    server_socket.close()
