#!/usr/bin/env python
import requests
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

def downpic(filename):
    r = requests.get('http://yjs.ustc.edu.cn/checkcode.asp')
    img_array = np.asarray(bytearray(r.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    final = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
    cells = np.hsplit(final, 4)
    if not os.path.exists('./pics/'):
        os.makedirs('./pics/')
    for i in range(4):
        cv2.imwrite('./pics/'+str(filename+i)+'.jpg', cells[i])

def run():
    start = 0
    end = 1000
    while(start < end):
        downpic(start)
        print (start)
        start += 4

if __name__ == '__main__':
    run()
