import os
import  numpy as np
from imutils import paths
import argparse
from tensorflow.keras.models import Model
import cv2
from tensorflow.keras.models import load_model
def prepare():
    testdata = []
    image = cv2.imread('test4.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    testdata.append(image);
    testdata = np.array(testdata) / 255.0
    return testdata

model=load_model('covidv2.h5')
prediction=model.predict([prepare()], verbose=0)

print(prediction)
if(prediction[0][0]>prediction[0][1]):
    print("covid")
else:
    print("not-covid")