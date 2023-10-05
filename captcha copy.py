from PIL import Image
import operator

im = Image.open("stuff/captcha.gif")
im = im.convert("P")
his = im.histogram()

values = {}

for i in range(256):
    values[i] = his[i]

for j, k in sorted(values.items(), key=operator.itemgetter(1), reverse=True)[:10]:
    print(j, k)


im2 = Image.new("P", im.size, 255)

im = im.convert("P")

temp = {}

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        temp[pix] = pix
        if pix == 225:  # these are the numbers to get_
            im2.putpixel((y, x), 0)

im2.save("stuff/output.gif")

# new code starts here_

inletter = False
foundletter = False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):  # slice across_
    for x in range(im2.size[1]):  # slice down_
        pix = im2.getpixel((y, x))
        if pix != 255:
            inletter = True

    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))

    inletter = False

print(letters)
