import cv2 
import numpy as np 
import matplotlib.pyplot as plt

def sigmoid(x):
	return 1/(1+np.exp(-x))

img = cv2.imread("test_img.jpeg")
bw_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#bw_img = np.array(bw_img)
width,height = 256,256
dsize = (width, height)
bw_img = bw_img/255
#test = cv2.resize(img,dsize
#print(bw_img.shape)
#print(bw_img[0])
#cv2.imshow("original img",img)
#cv2.imwrite("bw_img.jpeg",bw_img)
#cv2.waitKey(0)
#cv2.imshow("bw img",bw_img)
print(bw_img.size)
for i in range(bw_img.size):
	inb = bw_img[i]
	#print(inb.shape)
	if inb >0.5:
		bw_img[i][j] = 1
	else:
		bw_img[i][j] = 0
plt.imshow(bw_img)
plt.show()
import os 
size = os.get_terminal_size()
print(" the size is: ",size)
fil = open("test.txt","w+")
test = "x"*size[0]
r =""
for i in range(size[1]):
	r += test + "\n"

fil.write(r)
