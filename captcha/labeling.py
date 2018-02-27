import cv2
import os

keymap = dict(zip(range(48,58),range(0,10)))
print(keymap)

if not os.path.exists('./pics/'):
    print('please run gather.py first!')
    exit(1)

cv2.namedWindow("TEST")
l = os.listdir('./pics/')
l2 = [i for i in l if i.endswith('.jpg')]
for i in l2:
    img = cv2.imread(os.path.join('./pics/',i))
    cv2.imshow("TEST", img)
    key = int(cv2.waitKey(0))
    if key == 27:
        break
    if key in keymap:
        print (keymap[key])
        print (i)
        if not os.path.exists('./collect/' + str(keymap[key]) ):
            os.makedirs('./collect/' + str(keymap[key]))
        os.rename(os.path.join('./pics/',i),'./collect/' + str(keymap[key]) + '/' + str(i))
