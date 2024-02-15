import cv2 as cv
import hashlib
import os
import sys


def calSha1(filePath):
    if len(path) < 2:
        sys.exit('Usage: %s filename' % filePath)

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: File "%s" was not found!' % filePath)

    with open(filePath, 'rb') as f:
        sha1 = hashlib.sha1()

        while True:
            chunk = f.read(16 * 1024)
            if not chunk:
                break
            sha1.update(chunk)

        return str(sha1.hexdigest())


def imgRemux(imgSize, path):
    img = cv.imread(path)
    height, width = img.shape[:2]

    if height < width:
        width = height
        print("Widder")

    elif width < height:
        height = width
        print("Taller")

    cropped = img[0:width, 0:height] #Crop Image to make into 1:1 Ratio

    resized = cv.resize(cropped,(finalImgSize, finalImgSize),interpolation = cv.INTER_CUBIC) #Resize picture 
    cv.imwrite( calSha1(path) + '.png',resized) #Save resized image to file
