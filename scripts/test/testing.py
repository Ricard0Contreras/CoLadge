from scripts import localDatabase, resize, colorExtraction, canva
from PIL import Image 
import cv2 as cv
import os
import re

#plot point in 3d to represent gradient and color
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# path of cached of all pictures

def makeCollage(picList, xPics, yPics):
   cachePath = 'database' + os.sep + 'pictureCache' + os.sep
   #total amount of pictures
   picN = 16

   # max X value of canvas
   canvaXMax = xPics
   # max Y value of canvas
   canvaYMax = yPics

   # size (Pixels) of cached source pics
   sizePics = 1000


   #canva.makeCanva(canvaXMax, canvaYMax, sizePics) # make the canva (X, Y, Size of squares)
   #canvaImg = cv.imread('result.png') # opening canva, name hardcoded on scripts/canva.py 
   #canvaHeight , canvaWidth = canvaImg.shape[:2] # width and height of canva
   #canvaImg = Image.open('result.png') # opening canva to start loop of operations 

   # 3d plot making
   print('Show Vals')
   localDatabase.showValues()

   fig = plt.figure()
   ax = plt.figure().add_subplot(projection='3d')
   xDat = np.array([])
   yDat = np.array([])
   zDat = np.array([])
   #cordsDat = np.array([[]])
   cordDat = []

   for image in picList:
      procImg = image # pic that will processed

      picHash = str(resize.calSha1(procImg)) # process the hash of pic

      if localDatabase.keyInDB(picHash): # search the DB for the hash of the pic, if it is there then add to canva

         #y = int(x/4) #the way Y is calculated makes it jump to the next line when such is filed
         #if (x>3):
         #   x -= 4 * y

         print(str(procImg) + ' is already in cache & db \n')# + 'putting '+ str(procImg) + ' on', x, ' ', y)

         picColors = localDatabase.returnColors(picHash) # Stores the colors of that pic in a list, in total 5

         print(picColors)
         
         xDat = np.append(xDat, int(picColors[0]))
         yDat = np.append(yDat, int(picColors[1]))
         zDat = np.append(zDat, int(picColors[2]))
         #cordsDat = np.append(cordsDat, list(tempList))
         cordDat.append(picColors)


         #canva.putPic(canvaImg, cachePath+picHash+'.png', sizePics, x, y) # puts the pic on the canva based on X and Y


      else: # else cache pic and add to canva 
         resize.imgRemux(sizePics, procImg)
         localDatabase.addValue(picHash, colorExtraction.getColor(cachePath + picHash + '.png')) # calculates the colors and add all the data to the db

         #y = int(x/4)
         #if (x>3):
         #   x -= 4 * y
         print('added ' + str(procImg) + ' to cache & db \n') # + 'putting '+ str(procImg) + ' on', x, ' ', y)

         #canva.putPic(canvaImg, cachePath+picHash+'.png', sizePics, x, y)

   colors = []
   for n in range(len(xDat)):
      colors.append('#%02x%02x%02x' % (int(xDat[n]),int(yDat[n]),int(zDat[n])))


   cordDat = np.asarray(cordDat)

   print()
   print('Values of X/R ',xDat)
   print('Values of Y/G ',yDat)
   print('Values of Z/B ',zDat)
   print()
   print('2D array', cordDat)
   print('Colors array', colors)


   counter = 1
   ax.scatter3D(xDat, yDat, zDat, c = colors)
   ax.set_xlabel('R')
   ax.set_ylabel('G')
   ax.set_zlabel('B')
   for (x2, y2, z2) in zip(xDat, yDat, zDat):
      ax.text(x2, y2, z2, f'({counter})')
      counter += 1
         
   plt.show()
#canvaImg.save('result.png') # saves final picture result, must be ONLY ran once 
