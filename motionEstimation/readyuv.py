import numpy as np
import cv2

block = 16 #size of block 16x16

def yuvRead(vid, width, height, nFrame):
    f = open(vid, "rb")
    stream = f.read()
    length = int(width*height*1.5)
    y = np.zeros((nFrame, height, width), dtype='uint8')
    u = np.zeros((nFrame, int(height/2), int(width/2)), dtype='uint8')
    v = np.zeros((nFrame, int(height/2), int(width/2)), dtype='uint8')
    for i in range(nFrame):
        frame = stream[(i*length):((i+1)*length)]
        dataYRaw = np.frombuffer(frame[0:width*height], dtype = 'uint8')
        y[i] = np.reshape(dataYRaw, (height,width))
        dataURaw = np.frombuffer(frame[width*height:int(1.25*height*width)], dtype = 'uint8')
        u[i] = np.reshape(dataURaw, (int(0.5*height), int(0.5*width)))
        dataVRaw = np.frombuffer(frame[int(1.25*width*height):int(1.5*height*width)], dtype = 'uint8')
        v[i] = np.reshape(dataVRaw, (int(0.5*height), int(0.5*width)))
    return y,u,v
def zeroPadding(img, nPad): #nPad: number of extend part
    global block
    height = len(img)
    width = len(img[0])
    size = (height+nPad*2,width+nPad*2)
    imgPad = np.zeros(size, dtype='uint8')
    imgPad[nPad:height+nPad,nPad:width+nPad] = img
    return imgPad

def findMinDiff(searchArea, img):
    global block
    minDiff = 16*16*255
    #print(searchArea.shape)
    minDiffMatrix = img
    for x in range(0,(len(searchArea)-16)):
        for y in range(0,(len(searchArea[0])-16)):
            diffMatrix = searchArea[x:(x+16), y:(y+16)]
            #print(diffMatrix.shape, img.shape)
            diff = abs(np.sum(diffMatrix-img))
            if diff < minDiff:
                minDiff =diff
                minDiffMatrix = diffMatrix
                mvx = x
                mvy = y
    
    mv = np.array([x,y])
    return minDiffMatrix, mv

def motionEstimation(preFrame, curFrame):
    global block
    predictFram = np.zeros(curFrame.shape, dtype='uint8')
    height = len(curFrame)
    width = len(curFrame[0])
    preFrame = zeroPadding(preFrame, 16)
    mv = np.zeros((int(height/block),int(width/block),2))
    for x in range(0,height,block):
        for y in range(0,width,block):    # each block of current Frame
            searchArea = preFrame[(x+16-16):(x+16+block+16), (y+16-16):(y+16+block+16)]
            img = curFrame[x:(x+16), y:(y+16)]
            minDiffMatrix, mv[int(x/block), int(y/block)] = findMinDiff(searchArea, img)
            predictFram[x:(x+16), y:(y+16)] = minDiffMatrix
            # cv2.imshow('f1', minDiffMatrix)
            # cv2.waitKey()
            # cv2.imshow('f2', img)
            # cv2.waitKey()
    return predictFram, mv  
            
def decode(preFrame, deltaFrame, mv):
    global block
    height = len(deltaFrame)
    width = len(deltaFrame[0])
    preFrame = zeroPadding(preFrame, 16)
    mv = np.zeros((int(height/block),int(width/block),2))
    for x in range(0,height,block):
        for y in range(0,width,block):    # each block of preframe
  
vid = "sampleQCIF.yuv"
width = 176
height = 144
nFrame = 500
y, u, v =  yuvRead(vid, width, height, nFrame)
# for i in range(nFrame):
#     if i % 75 == 0:
#         cv2.imshow('imhy', y[i])
#         cv2.waitKey()
#         cv2.imshow('imh', u[i])
#         cv2.waitKey()
#         cv2.imshow('imh', v[i])
#         cv2.waitKey()
predictFram, mv = motionEstimation(y[1], y[50])
deltaFrame = (predictFram - y[2])
gray = cv2.threshold(deltaFrame, 100, 255, cv2.THRESH_BINARY_INV)[1]
dst = cv2.Laplacian(deltaFrame, cv2.CV_16S, ksize=3)
# cv2.imshow('f1', y[1])
# cv2.waitKey()
# cv2.imshow('f2', predictFram)
# cv2.waitKey()
cv2.imshow('df', dst)
cv2.waitKey()
# np.savetxt('test.txt', pad,  fmt='%i', delimiter=', ', ) 
