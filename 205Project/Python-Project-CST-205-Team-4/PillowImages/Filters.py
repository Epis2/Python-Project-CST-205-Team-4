from PIL import Image
from flask import Flask, render_template
from PIL import ImageFilter
import numpy as np
import skimage
import matplotlib.pyplot as plt
from skimage import io, filters
import cv2
import sys
app = Flask(__name__)


@app.route('/')

def index():
    return render_template('Modify.html')



#image I used for tests
#img = 'rosa_red.jpg'

def colorswitch(x):
    return {
        'autumn' : cv2.COLORMAP_AUTUMN,
        'bone' : cv2.COLORMAP_BONE,
        'jet' : cv2.COLORMAP_JET,
        'winter' : cv2.COLORMAP_WINTER,
        'rainbow' : cv2.COLORMAP_RAINBOW,
        'ocean' : cv2.COLORMAP_OCEAN,
        'summer' : cv2.COLORMAP_SUMMER,
        'spring' : cv2.COLORMAP_SPRING,
        'cool' : cv2.COLORMAP_COOL,
        'hsv' : cv2.COLORMAP_HSV,
        'pink' : cv2.COLORMAP_PINK,
        'hot' : cv2.COLORMAP_HOT,
    }[x]

def colormaps(image,colormap):
    image_gray = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    image_remap = cv2.applyColorMap(image_gray, colorswitch(colormap))
    cv2.imshow(colormap  + " " + image , image_remap)
    cv2.waitKey()

def fontswitch(x):
    return {
        'simplex' : cv2.FONT_HERSHEY_SIMPLEX,
        'plain' : cv2.FONT_HERSHEY_PLAIN,
        'duplex' : cv2.FONT_HERSHEY_DUPLEX,
        'complex' : cv2.FONT_HERSHEY_COMPLEX,
        'triplex' : cv2.FONT_HERSHEY_TRIPLEX,
        'small' : cv2.FONT_HERSHEY_COMPLEX_SMALL,
        'script_simplex' : cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        'script_complex' : cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    }[x]

def writeText(image,text, x,y, thickness, font = cv2.FONT_HERSHEY_SIMPLEX):
    imagetext = cv2.putText(image, text, (x,y),font,4, (245,245,245),thickness)
    cv2.imshow("image",imagetext)
    cv2.waitKey()

'''
x,y = coordinates of the bottom left of the string
thickness = thickness of the text (its an int starting at 1)
writeText(cv2.imread(img),'TESTING', 50, 300, 3)
writeText(cv2.imread(img),'TESTING', 50, 300, 3, fontswitch('plain'))
'''


def decrease_red(image,red_percentage):
    decrease = (100 - red_percentage)/100
    im = Image.open(image)
    new_list = map(lambda a : (int(a[0]*decrease), a[1], a[2]), im.getdata())
    im.putdata(list(new_list))
    plt.imshow(im)
    plt.show()



def negative(image):
    im = Image.open(image)
    neg_list = [(255-p[0], 255-p[1], 255-p[2]) for p in im.getdata()]
    im.putdata(list(neg_list))
    plt.imshow(im)
    plt.show()

def greyscale(image):
    im = Image.open(image)
    neg_list = [((p[0]+p[1]+p[2])//3,)*3 for p in im.getdata()]
    im.putdata(list(neg_list))
    plt.imshow(im)
    plt.show()



def sepia(image):
    im = Image.open(image)
    r,g,b = 0,0,0
    for x in range(im.width):
        for y in range(im.height):
            if (im.getpixel((x,y))[0] < 63):
                r,g,b = int(im.getpixel((x,y))[0] * 1.1), im.getpixel((x,y))[1], int(im.getpixel((x,y))[2] * 0.9)
            elif (im.getpixel((x,y))[0] > 62 and im.getpixel((x,y))[0] < 192):
                r,g,b = int(im.getpixel((x,y))[0] * 1.15), im.getpixel((x,y))[1], int(im.getpixel((x,y))[2] * 0.85)
            else:
                r = int(im.getpixel((x,y))[0] * 1.08)
                if r > 255:
                    r = 255
                g,b = im.getpixel((x,y))[1], int(im.getpixel((x,y))[2] * 0.5)
            im.putpixel((x,y),(r, g, b))
    plt.imshow(im)
    plt.show()

def thumbnail(image):
    im = Image.open(image)
    im.thumbnail(((im.width)//2,im.height//2), Image.ANTIALIAS)
    plt.imshow(im)
    plt.show()

def crop(image,left,upper,right,lower):
    im = Image.open(image)
    print(im.width)
    print(im.height)
    #cropbox = (80,50,400,300)
    cropbox = (left,upper,right,lower)
    im = im.crop(cropbox)
    print(im.width)
    print(im.height)
    plt.imshow(im)
    plt.show()

def medianFilter(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.MedianFilter)
    plt.imshow(im)
    plt.show()



def channel_adjust(channel, values):
    orig_size = channel.shape
    flat_channel = channel.flatten()
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)
    return adjusted.reshape(orig_size)

def split_image_into_channels(image):
    red_channel = image[:, :, 0]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 2]
    return red_channel, green_channel, blue_channel

def merge_channels(red_channel, green_channel, blue_channel):
    return np.stack([red_channel, green_channel, blue_channel], axis=2)

def gotham(image):
    original_image = skimage.img_as_float(io.imread(image))
    r = original_image[:, :, 0]
    b = original_image[:, :, 2]
    r_boost_lower = channel_adjust(r, [
        0, 0.05, 0.1, 0.2, 0.3,
        0.5, 0.7, 0.8, 0.9,
        0.95, 1.0])
    b_more = np.clip(b + 0.03, 0, 1.0)
    merged = np.stack([r_boost_lower, original_image[:, :, 1], b_more], axis=2)
    blurred = filters.gaussian(merged, sigma=10, multichannel=True)
    final = np.clip(merged * 1.3 - blurred * 0.3, 0, 1.0)
    b = final[:, :, 2]
    b_adjusted = channel_adjust(b, [
        0, 0.047, 0.118, 0.251, 0.318,
        0.392, 0.42, 0.439, 0.475,
        0.561, 0.58, 0.627, 0.671,
        0.733, 0.847, 0.925, 1])
    final[:, :, 2] = b_adjusted
    r, g, b = split_image_into_channels(final)
    im = merge_channels(r, g, b)
    im2 = Image.open(image).convert('L')
    plt.imshow(im)
    plt.show()


#######
# This filter make the borders of the image.

im2 = Image.open("cute.jpg").convert('L')
def edge(type):

    if type == 'Prewitt':
        factor =6

        x =[-1, 0, 1, -1, 0, 1, -1 , 0, 1]
        y =[-1, -1, -1, 0, 0, 0, 1, 1, 1]

        x1 =[1, 0, -1, 2, 0, -2, 1, 0, -1]
        y1 =[1, 2, 1, 0, 0, 0, -1, -2, -1]

    elif type == 'Sobel':
        factor =8
        x =[-1, 0, 1, -2, 0, 2, -1, 0, 1]
        y =[-1, -2, -1, 0, 0, 0, 1, 2, 1]

        x1 =[1, 0, -1, 2, 0, -2, 1, 0, -1]
        y1 =[1, 2, 1, 0, 0, 0, -1, -2, -1]

    else:
        sys.exit(0)


    data_x = im2.filter(ImageFilter.Kernel((3,3), x, factor)).getdata()
    data_y = im2.filter(ImageFilter.Kernel((3,3), y, factor)).getdata()


    data =[]
    # In this specifict for loop I created a new variable and assigned to the data_x and data_y
    # because it isn't allow me to used the original one
    dx = data_x
    dy = data_y

    for ix in range(len(data_x)):
        data.append(round(((dx[ix] ** 2) + (dy[ix] ** 2)) ** 0.5))

    datos_x = im2.filter(ImageFilter.Kernel((3,3), x1, factor)).getdata()
    datos_y = im2.filter(ImageFilter.Kernel((3,3), y1, factor)).getdata()


    data1 =[]

    for jx in range(len(data_x)):
        data1.append(round(((datos_x[jx] ** 2) + (datos_y[jx] ** 2)) ** 0.5))


    data3 =[]

    for nx in range(len(data_x)):
        data3.append(data[nx] + data1[nx])
    return data3

data3 = edge('Prewitt')

new_im = Image.new('L', im2.size)
new_im.putdata(data3)

new_im.save('edge.jpg')
im2.close()
new_im.close()
