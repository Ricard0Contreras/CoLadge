from PIL import Image 
import cv2 as cv

#init Canva 
#canvaImg = cv.imread('result.png')
#canvaHeightY , canvaWidthX = canvaImg.shape[:2]
#canvaImg = Image.open('result.png')

#init Canva must be called as is for all functions below to work

def makeCanva(x, y, sizePics):
    canvaX = sizePics * x
    canvaY = sizePics * y
    canvaImg = Image.new('RGB', (canvaX, canvaY)) 
    canvaImg.save('result.png')

def putPic(canvaImg, picPath, sizePics, x, y):
    posX = x * sizePics
    posY = y * sizePics
    cords = (posX, posY)
    img2 = Image.open(picPath)
    canvaImg.paste(img2, cords)
