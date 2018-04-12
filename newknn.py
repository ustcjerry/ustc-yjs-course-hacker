# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os


class Captcha:
    def __init__(self):
        collect_dir = 'captcha/collect'
        label = []
        train_file = []
        for i in os.listdir(collect_dir):
            for y in os.listdir(collect_dir + '/' + i):
                #print i
                label.append(ord(i))
                #print y
                train_file.append(collect_dir + '/' + i + '/' + y)
        train_data = [cv2.imread(i, 0) for i in train_file]
        # print(np.array(train_data).shape)
        train = np.array(train_data).reshape(-1, 100).astype(np.float32)
        label = np.array(label).reshape(-1)
        self.knn = cv2.ml.KNearest_create()
        self.knn.train(train, cv2.ml.ROW_SAMPLE,label)

    def hack(self, img):
        test_img_array = np.asarray(bytearray(img), dtype=np.uint8)
        test_img = cv2.imdecode(test_img_array, -1)
        test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        test_final = cv2.threshold(test_gray, 100, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow("TEST", test_final)
        # cv2.waitKey(0)
        test_cells = np.array([i.reshape(-1).astype(np.float32)
                            for i in np.hsplit(test_final, 4)])
        ret, result, neighbours, dist = self.knn.findNearest(test_cells, k=1)
        result = result.reshape(-1)
        letter = []
        for i in result:
            letter.append(chr(i))
        return ''.join(letter)

    def hack_img(self, img):
        test_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        test_final = cv2.threshold(test_gray, 100, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow("TEST", test_final)
        # cv2.waitKey(0)
        test_cells = np.array([i.reshape(-1).astype(np.float32)
                            for i in np.hsplit(test_final, 4)])
        ret, result, neighbours, dist = self.knn.findNearest(test_cells, k=1)
        result = result.reshape(-1)
        letter = []
        for i in result:
            letter.append(chr(i))
        return ''.join(letter)    