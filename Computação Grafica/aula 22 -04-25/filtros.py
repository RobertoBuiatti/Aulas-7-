from PIL import Image, ImageFilter, ImageOps

def filtro_negativo(img):
    return ImageOps.invert(img.convert('RGB'))

def filtro_gray(img):
    return img.convert('L')

def filtro_contorno(img):
    return img.filter(ImageFilter.CONTOUR)