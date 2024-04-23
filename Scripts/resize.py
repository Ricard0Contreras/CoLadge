import cv2 as cv
import hashlib
import os
import sys


def calSha1(filename):
       h = hashlib.sha1()
       with open(filename,'rb') as file:
           chunk = 0
           while chunk != b'':
               chunk = file.read(1024)
               h.update(chunk)

       return h.hexdigest()


def imgRemux(imgSize, path):
    img = cv.imread(path)
    height, width = img.shape[:2]

    if height < width:
        width = height
    elif width < height:
        height = width
    cropped = img[0:width, 0:height]  # Crop Image to make into 1:1 Ratio

    resized = cv.resize(cropped, (imgSize, imgSize), interpolation=cv.INTER_CUBIC)  # Resize picture
    cv.imwrite('Database' + os.sep + 'pictureCache' + os.sep + calSha1(path) + '.cache.png', resized)  # Save resized image to file
