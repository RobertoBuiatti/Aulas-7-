from PIL import Image
import math


img = Image.open('cat.jpg')

matriz = img.load()

largura, altura = img.size
print(largura,altura)

print(matriz[0,0])

def gama (pixel, gama):
    return int(pow((pixel/255), gama)*255)

fator = 1.5
for i in range(largura):
    for j in range(altura):
        pixel = gama(matriz[i,j][0], fator), gama(matriz[i,j][1], fator), gama(matriz[i,j][2], fator)
        matriz[i,j] = pixel

img.save('cat_Gama.jpg')
matriz = img.load()

largura, altura = img.size
print(largura,altura)

print(matriz[0,0])