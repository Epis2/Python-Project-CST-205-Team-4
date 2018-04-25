from PIL import Image

img = 'rosa_red.jpg'
def decrease_red(image,red_percentage):
    decrease = (100 - red_percentage)/100
    im = Image.open(image)
    new_list = map(lambda a : (int(a[0]*decrease), a[1], a[2]), im.getdata())
    im.putdata(list(new_list))
    im.show()



def negative(image):
    im = Image.open(image)
    neg_list = [(255-p[0], 255-p[1], 255-p[2]) for p in im.getdata()]
    im.putdata(list(neg_list))
    im.show()

def greyscale(image):
    im = Image.open(image)
    neg_list = [((p[0]+p[1]+p[2])//3,)*3 for p in im.getdata()]
    im.putdata(list(neg_list))
    im.show()



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
    im.show()

def thumbnail(image):
    im = Image.open(image)
    im.thumbnail(((im.width)//2,im.height//2), Image.ANTIALIAS)
    im.show()

thumbnail(img)
