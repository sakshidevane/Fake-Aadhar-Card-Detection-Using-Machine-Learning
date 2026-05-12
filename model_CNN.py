
import numpy as np

import os

from PIL import Image
from numpy import *


# input image dimensions
img_rows, img_cols = 100, 100

# number of channels
img_channels = 3

#%%
#  data

path1 = 'D:/Rushikesh khatke/Rushikesh25-26/25c9404 -FAKE adhar card detection CNN/100% code/new 100% code/Real Aadhar card'    #path of folder of images    
path2 = 'D:/Rushikesh khatke/Rushikesh25-26/25c9404 -FAKE adhar card detection CNN/100% code/new 100% code/training set/1'  #path of folder to save images    

listing = os.listdir(path1)
num_samples=size(listing)
print(num_samples)

for file in listing:
    im = Image.open(path1 + '\\' + file)  
    img = im.resize((img_rows,img_cols))
    gray = img.convert(mode='RGB')
                #need to do some more processing here          
    gray.save(path2 +'\\' +  file, "JPEG")

imlist = os.listdir(path2)

im1 = array(Image.open('input_data_resized/' + imlist[0])) # open one image to get size
m,n = im1.shape[0:2] # get the size of the images
imnbr = len(imlist) # get the number of images


