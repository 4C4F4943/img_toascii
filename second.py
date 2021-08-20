import numpy as np
from numpy.core.fromnumeric import reshape
from numpy.core.records import array
from numpy.lib.function_base import average
import requests
import time
import matplotlib.pyplot as plt
from PIL import Image,ImageEnhance
#from numpy.lib.type_check import imag


gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

#avg2
"""
def avg1(img):
	img = np.array(img)
	return np.average(img.reshape(img.shape[0],img.shape[1]))
"""
#avg1
def avg(img):
	img = np.array(img)
	w,h = img.shape
	return np.average(img.reshape(w,h))




def img_ascii(file_name, cols=100,res_file="out.txt",moreLevels=True,inverse=False,scale=0.43):
  #global gscale1, gscale2, args
  gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
  gscale2 = '@%#*+=-:. '
  gscale = ""
  # how many grayscale options
  opt = 0
  if inverse:
    gscale1 = gscale1[::-1]
    gscale2 = gscale2[::-1]

  if moreLevels:
    gscale = gscale1
    gopt = 69
  else:
    gscale = gscale2
    gopt = 9

  try:
    requests.get(file_name)
    image = Image.open(requests.get(file_name, stream=True).raw).convert('L')
  except:
    image = Image.open(file_name).convert('L')
  #enhancor = ImageEnhance.Contrast(image)
  W, H = image.size[0], image.size[1]
  if cols == "max": 
    cols = W

  #sharpness
  enhancor = ImageEnhance.Sharpness(image)
  sharper = enhancor.enhance(3)

  #contrast
  av = avg(image)
  enhancor2 = ImageEnhance.Contrast(sharper)
  more_vibrant = enhancor2.enhance((3-round((av*3)/255)))
  av = avg(image)

  #brightness
  enhancor3 = ImageEnhance.Brightness(more_vibrant)
  image = enhancor3.enhance((11-round((av*11)/255))/5)
  #print("input image dims: %d x %d" % (W, H))
  w = W/cols
  h = w/scale
  rows = int(H/h)
  #print("cols: %d, rows: %d" % (cols, rows))
  #print("tile dims: %d x %d" % (w, h))

  if cols > W or rows > H:
    print("image too small for cols")
    exit(0)
  res = []

  for j in range(rows):
    y1 = int(j*h)
    y2 = int((j+1)*h)
    res.append("")

    if j == rows-1: 
      y2 = H

    for i in range(cols):
      x1 = int(i*w)
      x2 = int((i+1)*w)
      if i == cols-1: 
        x2 = W

      img = image.crop((x1, y1, x2, y2)) 
      a = int(avg(img))
      gsval = gscale[int((a*gopt)/255)]
      res[j] += gsval
          
  
  f = open(res_file,"w")
  for row in res: 
    f.write(row+ '\n')
  f.close()
  return res
times = []
avgs = []

for i in range(100):
  start = time.time()
  img_ascii("dark_img.jpeg",cols=200,res_file="testing6.txt",moreLevels=False,inverse=True,scale=0.43)
  stop = time.time()-start
  times.append(stop)
  if i % 10 == 0 and i != 0:
    
    print("iteration: %.3i, current avg %.5f"%(i,sum(times[i-10:i])/10),end="\r")
    for j in range(10):
      avgs.append(sum(times[i-10:i])/10)
print(" on average it took: ",sum(times)/len(times)," seconds")
plt.plot(times)
plt.plot(avgs)
plt.show()