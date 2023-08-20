import copy
import os
import cv2
import cv2 as cv
import numpy as np
import argparse
from enum import Enum

parser = argparse.ArgumentParser(
    prog="BackgroundColorConverter",
    description="Change the background color of the given image",
)
parser.add_argument( "filename" )
parser.add_argument( '-o', "--outdir",
                     required = True )
parser.add_argument( '-f', '--fromColor',
                     required = True )
parser.add_argument( '-t', "--toColor",
                     required = True )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = parser.parse_args()
    filename: str  = args.filename
    outdir: str    = args.outdir
    fromColorStr: str = args.fromColor
    toColorStr: str   = args.toColor

    Color = Enum( "ToColor", ["RED", "BLUE", "WHITE"] )
    if fromColorStr.casefold() == "red".casefold() or fromColorStr.casefold() == 'r'.casefold():
        fromColor = Color.RED
    elif fromColorStr.casefold() == "blue".casefold() or fromColorStr.casefold() == 'b'.casefold():
        fromColor = Color.BLUE
    elif fromColorStr.casefold() == "white".casefold() or fromColorStr.casefold() == 'w'.casefold():
        fromColor = Color.WHITE
    else:
        assert False, "Unsupported fromColor. Valid values include b/blue, r/red, w/white or uppercase counterpart."

    if toColorStr.casefold() == "red".casefold() or toColorStr.casefold() == 'r'.casefold():
        toRGBIndex = ( 255, 0, 0 )
    elif toColorStr.casefold() == "blue".casefold() or toColorStr.casefold() == 'b'.casefold():
        toRGBIndex = ( 0, 0, 255 )
    elif toColorStr.casefold() == "white".casefold() or toColorStr.casefold() == 'w'.casefold():
        toRGBIndex = ( 255, 255, 255 )
    else:
        assert False, "Unsupported toColor. Valid values include b/blue, r/red, w/white or uppercase counterpart."

    cwd = os.getcwd()
    filepath = filename if os.path.isabs( filename ) else cwd + '/' + filename
    outputpath = outdir if os.path.isabs( outdir ) else cwd + '/' + outdir
    img = cv.imread( filepath, cv.IMREAD_COLOR )
    assert img is not None, "file not exist"
    originImg = copy.deepcopy( img )
    rows, cols, chs = img.shape
    img = cv.cvtColor( src=img, code=cv.COLOR_BGR2HSV )

    if fromColor == Color.RED:
        lowerBound1 = np.array( [0, 70, 50] )
        upperBound1 = np.array( [10, 255, 255] )
        lowerBound2 = np.array( [170, 70, 50] )
        upperBound2 = np.array( [180, 255, 255] )
    elif fromColor == Color.BLUE:
        lowerBound1 = np.array( [90, 70, 50] )
        upperBound1 = np.array( [128, 255, 255] )
        lowerBound2 = None
        upperBound2 = None
    else:  # WHITE
        lowerBound1 = np.array( [0, 0, 231] )
        upperBound1 = np.array( [180, 18, 255] )
        lowerBound2 = None
        upperBound2 = None

    mask1 = cv.inRange( img, lowerb=lowerBound1, upperb=upperBound1 )
    mask2 = cv.inRange( img, lowerb=lowerBound2, upperb=upperBound2 ) if lowerBound2 is not None else None
    mask = cv.bitwise_or(src1=mask1, src2=mask2) if mask2 else mask1

    # myKernelSize = ( 3, 3 ) if img.size < 640 * 480 else ( 12, 12 )
    erode = cv2.erode( mask, kernel=cv.getStructuringElement( shape=cv.MORPH_ERODE, ksize=myKernelSize, iterations=1 ) )
    # erode = cv2.erode( src=mask, kernel=None, iterations= 1 )
    # erode = cv2.dilate(mask, kernel=cv.getStructuringElement(shape=cv.MORPH_ERODE, ksize=myKernelSize))
    # dilation = cv2.dilate( src=mask, kernel=None, iterations=1 )

    for i in range( rows ):
        for j in range( cols ):
            if erode[i][j] == 255:
                originImg[i][j] = toRGBIndex

    # cv.imshow( "mask", mask )
    # cv.imshow( "erode", erode )
    # cv.imshow( "dilate", dilation )
    # cv.imshow( "after", originImg )
    # cv.waitKey(0)

    cv.imwrite( outputpath + '/' + "after.jpg", originImg )
    print( f"Written image to {outputpath}, image's name is after.jpg" )
