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
import shutil


dataclasses = "" # plní se při inicializaci neuronsítě

OUTDIR = "../outdir"
def prepareOutDirs ():
    if os.path.exists(OUTDIR):
        shutil.rmtree (OUTDIR)
    os.makedirs(OUTDIR)
   
    unknown = "%s/%s" % (OUTDIR, "unknown") 
    if not os.path.exists(unknown):
        os.makedirs(unknown)

    for subdir in dataclasses:
        directory = "%s/%s" % (OUTDIR, subdir)
        if not os.path.exists(directory):
            os.makedirs(directory)

def initNeuralNetwork(pathToModel, model):
    PATH = "/home/pryb/data/brick/"
    sz=224

    arch=resnet34
    data = ImageClassifierData.from_paths(pathToModel, tfms=tfms_from_model(arch, sz))
    learn = ConvLearner.pretrained(arch, data, precompute=False) # TODO prověřit to precompute
    learn.load(model)
    print('start')
    trn_tfms, val_tfms = tfms_from_model(resnet34, sz, aug_tfms = transforms_side_on, max_zoom = 1.1)

    # FIXME tohle patří jenom do vyhodnocovacího serveru
    global dataclasses
    dataclasses = data.classes
    prepareOutDirs ()

    return learn, val_tfms

def classifyImage(learn, val_tfms, img):
    
    im= val_tfms(img.astype(np.float32)/255)

    # predictions are log scale - 0 would be 100% sure
    predictions = learn.predict_array(im[None])
    
    classificationIndex = np.argmax(np.exp(predictions))

    print(classificationIndex)

    return classificationIndex, predictions

def classifyAndSaveImage(learn, val_tfms, img):
    imgCv = imageToOpenCv (img)
 
    ( classificationIndex, predictions ) = classifyImage (learn, val_tfms, imgCv)
    
    if -0.1 > predictions[0,classificationIndex]:
        # uncertain
        print(predictions)
        img.save('%s/unknown/%d_%f.jpg' % (OUTDIR, classificationIndex, time.time()), "JPEG")
        classificationIndex = 0
    else:
        if classificationIndex > 0:
            img.save('%s/%s/%d_%f.jpg' % (OUTDIR, dataclasses[classificationIndex], classificationIndex, time.time()), "JPEG")

    return classificationIndex

def cropOpenCvImage (img):
    width, height = img.shape[:2]
    
    wt = width//3
    ht = height//3
    
    imgCropped = img[wt:wt*2, ht:ht*2]
    return imgCropped

def cropImage (img):
    width, height = img.size
    wt = width//3
    ht = height//3
    box = (wt, ht, wt*2, ht*2)
    area = img.crop(box)
    return area

def readImageFromClient(socket): 
    connection = socket.makefile('rb')

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

    img = Image.open(image_stream)

    connection.close ()
 
    return img

def imageToOpenCv (img):
    # prevedeme na openCV
    imageCV = numpy.array(img.convert('RGB'))
    #imageCV = imageCV[:, :, ::-1].copy()
    return imageCV

def getListenningSocket():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8201))
    server_socket.listen(0)

    return server_socket

def sendClassification (socket, classification):
        conn2=socket.makefile('wb')
        conn2.write(struct.pack('<L', classification))
        conn2.flush()
        conn2.close()

def isImageCentered(learn, val_tfms, img):
    # vyřízneme střed
    imgCropped = cropOpenCvImage(img)
    #cv2.imwrite('/home/pryb/data_cleanup/01.png', imgCropped)     
    #cv2.imwrite('/home/pryb/data_cleanup/01a.png', img)     
    # klasifikujeme střed
    (classificationCropped, predictionsCropped) = classifyImage (learn, val_tfms, imgCropped)
        
    if (classificationCropped == 0) and ( -0.1 < predictionsCropped[0,classificationCropped]):
        return False
    return True
    
