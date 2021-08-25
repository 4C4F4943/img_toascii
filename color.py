import numpy as np
from numpy.core.fromnumeric import reshape
from numpy.core.records import array
from numpy.lib.function_base import average
import requests
import time
import matplotlib.pyplot as plt
from PIL import Image,ImageEnhance
from PIL import ImageCms
import io

def convert_to_srgb(img):
    '''Convert PIL image to sRGB color space (if possible)'''
    icc = img.info.get('icc_profile', '')
    if icc:
        io_handle = io.BytesIO(icc)     # virtual file
        src_profile = ImageCms.ImageCmsProfile(io_handle)
        dst_profile = ImageCms.createProfile('sRGB')
        img = ImageCms.profileToProfile(img, src_profile, dst_profile)
    return img
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

def extract(lst,idx):
    return [item[idx] for item in lst]

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)
import random
print(colored(random.randint(0,255),random.randint(0,255),random.randint(0,255),"ouhhhh colorsss"))
def img_ascii(file_name, cols=100,res_file="out.txt",more_gray=True,inverse=False,scale=0.43):
  #global gscale1, gscale2, args
  gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
  gscale2 = '@%#*+=-:. '
  gscale = ""
  # how many grayscale options
  opt = 0
  if inverse:
    gscale1 = gscale1[::-1]
    gscale2 = gscale2[::-1]

  
  if more_gray:
    gscale = gscale1
    gopt = 69
  else:
    gscale = gscale2
    gopt = 9

  try:
    requests.get(file_name)
    image = Image.open(requests.get(file_name, stream=True).raw)#.convert('L')
    #image.load()
    image = image.convert("RGB")

    #background = Image.new("RGB", image.size, (255, 255, 255))
    #background.paste(image, mask = image.split()[3])

    print(image.size[0])
  except:
    image = Image.open(file_name)#.convert('L')
    image = image.convert("RGB")

  #enhancor = ImageEnhance.Contrast(image)
  W, H = image.size[0], image.size[1]
  if cols == "max": 
    cols = W
  gray_img = image.convert('L')
  #sharpness
  enhancor = ImageEnhance.Sharpness(gray_img)
  sharper = enhancor.enhance(3)

  #contrast
  av = avg(gray_img)
  enhancor2 = ImageEnhance.Contrast(sharper)
  more_vibrant = enhancor2.enhance((3-round((av*3)/255)))
  av = avg(gray_img)

  #brightness
  enhancor3 = ImageEnhance.Brightness(more_vibrant)
  gray_img = enhancor3.enhance((11-round((av*11)/255))/5)
  #print("input image dims: %d x %d" % (W, H))
  w = W/cols
  h = w/scale
  rows = int(H/h)
  #print("cols: %d, rows: %d" % (cols, rows))
  #print("tile dims: %d x %d" % (w, h))
  
  if cols > W or rows > H:
    print("image too small for cols, the max is: ",W)
    cols = W

     
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
      g_img = gray_img.crop((x1, y1, x2, y2))
      a = int(avg(g_img))
      gsval = gscale[int((a*gopt)/255)]
      img = np.array(img)
      #print(img)
      red = int(np.average(extract(img[0][:],0)))
      green = int(np.average(extract(img[0][:],1)))
      blue = int(np.average(extract(img[0][:],2)))
      #print(red,green,blue)
      #exit()
      res[j] += colored(red,green,blue,"@")
      #res[j] += gsval

          
  
  f = open(res_file,"w")
  for row in res: 
    print(row)
    f.write(row+ '\n')
  f.close()
  return res
times = []
avgs = []
url = "https://i.pinimg.com/564x/71/94/58/71945842e6985f179772c11a65bfb3c9.jpg"
#url = "idk.jpeg"
img_ascii(url,cols=120,res_file="testing6.txt",more_gray=False,inverse=True,scale=0.43)
"""
for i in range(100):
  start = time.time()
  img_ascii("dark_img.jpeg",cols=200,res_file="testing6.txt",more_gray=False,inverse=True,scale=0.43)
  stop = time.time()-start
  times.append(stop)
  if i % 10 == 0 and i != 0:
    
    print("iteration: %.3i, current avg %.5f"%(i,sum(times[i-10:i])/10),end="\r")
    for j in range(10):
      avgs.append(sum(times[i-10:i])/10)
print(" on average it took: ",sum(times)/len(times)," seconds")
plt.plot(times)
plt.plot(avgs)
plt.show()"""
