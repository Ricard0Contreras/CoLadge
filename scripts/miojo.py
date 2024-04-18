from scripts import localDatabase, resize, colorExtraction, canva
from math import sqrt
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from scipy.optimize import fsolve
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



def find_point_on_line(ex1, ex2, d): # Calculates the point of such distances 
    ex1 = np.array(ex1)
    ex2 = np.array(ex2)
    def func(t):
        # Calculate the point on the line at parameter t
        point = ex1 + t * (ex2 - ex1)
        # Return the difference between the Euclidean distance from ex1 to the point and d
        return np.linalg.norm(point - ex1) - d
    # Use scipy's fsolve function to solve for t
    t = fsolve(func, 0)
    # Calculate the coordinates of the point on the line at parameter t
    point = ex1 + t * (ex2 - ex1)
    return point


def find_best_distances(arr1, arr2):
    # Reshape the arrays into 2D (n,3) arrays
    arr1_reshaped = arr1.reshape(-1, 3)
    arr2_reshaped = arr2.reshape(-1, 3)

    # Compute the distance matrix
    distance_matrix = cdist(arr1_reshaped, arr2_reshaped)

    # Use the Hungarian algorithm to find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(distance_matrix)

    # Return the corresponding pairs and the total distance
    pairs = list(zip(row_ind, col_ind))
    #total_distance = distance_matrix[row_ind, col_ind].sum()

    return pairs # total_distance


def find_distance(p1,p2): # finds the distance between two points
   val = 0
   for n in range(len(p1)):
      val += (p1[n] - p2[n])**2
   return sqrt(val)


def find_closest_non_zero(array, index, direction):
    if direction == "up":
        for i in range(index, -1, -1):
            if array[i] != 0:
                return array[i]
    elif direction == "down":
        for i in range(index, len(array)):
            if array[i] != 0:
                return array[i]
    elif direction == "left":
        for i in range(index, -1, -1):
            if array[i] != 0:
                return array[i]
    elif direction == "right":
        for i in range(index, len(array)):
            if array[i] != 0:
                return array[i]
    return 0


def makeCollage(picList, xPics, yPics):
   cachePath = 'database' + os.sep + 'pictureCache' + os.sep
   #total amount of pictures
   picN = len(picList)

   # max X value of canvas
   canvaXMax = xPics
   # max Y value of canvas
   canvaYMax = yPics

   # size (Pixels) of cached source pics
   sizePics = 1000

   # List of path of cached pics
   picHashList = []

   canva.makeCanva(canvaXMax, canvaYMax, sizePics) # make the canva (X, Y, Size of squares)
   canvaImg = cv.imread('result.png') # opening canva, name hardcoded on scripts/canva.py 
   canvaHeight, canvaWidth = canvaImg.shape[:2] # width and height of canva
   canvaImg = Image.open('result.png') # opening canva to start loop of operations 

   # 3d plot making
   ax = plt.figure().add_subplot(projection='3d')
   cordDat = [] # Array of all cords of pics
   xDat = np.array([])
   yDat = np.array([])
   zDat = np.array([])

   for image in picList:
      procImg = image # pic that will processed

      picHash = str(resize.calSha1(procImg)) # process the hash of pic
      picHashList.append(picHash+'.png') # Saves path of all pics that will be used

      if localDatabase.keyInDB(picHash): # search the DB for the hash of the pic, if it is there then add to canva
         print(str(procImg) + ' is already in cache & db \n')# + 'putting '+ str(procImg) + ' on', x, ' ', y)
         picColors = localDatabase.returnColors(picHash) # Stores the colors of that pic in a list, in total 5
         print(picColors)
         cordDat.append(picColors) # adds the cords to the list

      else: # else cache pic and add to canva 
         resize.imgRemux(sizePics, procImg)
         currentColor = colorExtraction.getColor(cachePath + picHash + '.png')
         localDatabase.addValue(picHash, currentColor) # calculates the colors and add all the data to the db
         cordDat.append(currentColor) # adds the cords to the list
         print('added ' + str(procImg) + ' to cache & db \n')


   # lists holding the cordinate array of all pictures
   cordDat = np.asarray(cordDat, dtype=float)
   xDat = cordDat[:,0]
   yDat = cordDat[:,1]
   zDat = cordDat[:,2]

   colors = [] # list with hex color of each picture

   for n in range(len(xDat)):
      colors.append('#%02x%02x%02x' % (int(xDat[n]),int(yDat[n]),int(zDat[n])))

   print()
   print('2D array', cordDat)
   print('Colors array', colors)


   # 3D visualization of colors
   counter = 1
   ax.scatter3D(xDat, yDat, zDat, c = colors)
   ax.set_xlabel('R')
   ax.set_ylabel('G')
   ax.set_zlabel('B')
   for (x2, y2, z2) in zip(xDat, yDat, zDat): # Labels points with count
      ax.text(x2, y2, z2, f'({counter})')
      counter += 1

   hull = ConvexHull(cordDat.astype(int))
   hullpoints = cordDat.astype(int)[hull.vertices,:] # Calculates the two extremas
   hdist = cdist(hullpoints, hullpoints, metric='euclidean')
   bestpair = np.unravel_index(hdist.argmax(), hdist.shape)
   ex1 = hullpoints[bestpair[1]]
   ex2 = hullpoints[bestpair[0]]
   print('Two corner extremas ',ex1,ex2)
   print()

   disExtrema1 = [] # Array of all distances 
   disExtrema2 = []
   disLine = []


   for n in range(len(xDat)):
      disExtrema1.append(sqrt((xDat[n] - ex1[0])**2 + (yDat[n] - ex1[1])**2 + (zDat[n] - ex1[2])**2))
      disExtrema2.append(sqrt((xDat[n] - ex2[0])**2 + (yDat[n] - ex2[1])**2 + (zDat[n] - ex2[2])**2))
      disLine.append(abs((ex2[1]-ex1[1])*xDat[n] + (ex1[0]-ex2[0])*yDat[n] + (ex2[0]*ex1[1] - ex1[0]*ex2[1]))/
                     sqrt((ex2[0]-ex1[0])**2 + (ex2[1]-ex1[1])**2 + (ex2[2]-ex1[2])**2))


   # 2d array that holds the points of the grid of the collage
   gArr = np.array(cordDat)
   gArr[:,:] = 0
   gArr = gArr.reshape(xPics,yPics,3)

   # Setting commons on cord array
   gArr[0][0] = ex2
   gArr[xPics - 1][yPics - 1] = ex1
   #print(gArr)

   disDiagLine = max(disExtrema1) #lenght of diagonal line

   pDiadDis = disDiagLine / (max(xPics, yPics)- 1)
   k = 0
   x = 0
   y = 0
   p1 = ex2 # starts with the bigest extrema and the other extrema
   p2 = ex1

   rows, cols = yPics, xPics
   for i in range(max(rows, cols)):
      row = int(np.round(i * (rows - 1) / (max(rows, cols) - 1)))
      col = int(np.round(i * (cols - 1) / (max(rows, cols) - 1)))

      if col >= cols:
         col = cols - 1

      x = col
      y = row
      print('diags are ',x ,' ',y)
      if (gArr[x][y] - [0.0,0.0,0.0]).all() == False:
         print(x,y,'will take a value')
         k += 1
         gArr[x][y] = find_point_on_line(p1, p2, pDiadDis*k)



   print('Calc Diags')
   print(gArr)
   print()


   for i in range(gArr.shape[0]):
       for j in range(gArr.shape[1]):
           # If the point is all zeros
           if np.all(gArr[i, j] == 0):
               # Calculate X, Y, and Z based on the rules
               gArr[i, j, 0] = find_closest_non_zero(gArr[:, j, 0], i, "up") or find_closest_non_zero(gArr[:, j, 0], i, "down")
               gArr[i, j, 1] = find_closest_non_zero(gArr[:, j, 1], i, "up") or find_closest_non_zero(gArr[:, j, 1], i, "down")
               gArr[i, j, 2] = find_closest_non_zero(gArr[i, :, 2], j, "left") or find_closest_non_zero(gArr[i, :, 2], j, "right")

   print('Calculated missing values')
   print(gArr)
   print()


   cordDat = cordDat.reshape(xPics,yPics,3)

   orgIndPics = find_best_distances(gArr, cordDat)
   print(orgIndPics)
   for n in orgIndPics:
      print(n[1])

   x = 0
   y = 0

   for n in orgIndPics:
      print(x,' ',y)
      canva.putPic(canvaImg, cachePath+picHashList[n[1]], sizePics, x, y) # puts the pic on the canva based on X and Y
      x += 1
      if (x>xPics-1):
         y += 1
         x = 0

   canvaImg.save('result.png') # saves final picture result, must be ONLY ran once at end
   plt.show()
