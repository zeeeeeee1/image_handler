import glob
import sys
import re
import os.path
import shutil
import cv2

def put_converted_img(img, filename):
    converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    converted_img = cv2.rotate(converted_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite("./img/converted_" + filename, converted_img)

if __name__ == "__main__":
    imgpaths = glob.glob("./img/*")
    for imgpath in imgpaths:
        img = cv2.imread(imgpath)
        print(img.shape)
        ext = os.path.splitext(imgpath)[1]
        filename = os.path.basename(imgpath)
        put_converted_img(img, filename)



