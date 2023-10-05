import pytesseract
import os
from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path

def solve_captcha(path):

    """
    Convert a captcha image into a text, 
    using PyTesseract Python-wrapper for Tesseract
    Arguments:
        path (str):
            path to the image to be processed
    Return:
        'textualized' image
    """
    image = Image.open(path).convert('RGB')
    image = ImageOps.autocontrast(image)

    dirPath = "stuff"
    Path(dirPath).mkdir(parents=True, exist_ok=True)
    filename = "stuff/{}.png".format(os.getpid())
    image.save(filename)

    text = pytesseract.image_to_string(Image.open(filename))
    return text


if __name__ == '__main__':
    path = "stuff/captcha.gif"
    print('-- Resolving')
    captcha_text = solve_captcha(path)
    print('-- Result: {}'.format(captcha_text))