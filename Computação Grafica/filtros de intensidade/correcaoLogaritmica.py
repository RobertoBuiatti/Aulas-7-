from PIL import Image
import math


img = Image.open('cat.jpg')

matriz = img.load()

largura, altura = img.size
print(largura,altura)

print(matriz[0,0])

def logaritmica (pixel):
    c = 255/math.log(256)
    return int(c*math.log(1+pixel))
fator = 1.5
for i in range(largura):
    for j in range(altura):
        pixel = logaritmica(matriz[i,j][0]), logaritmica(matriz[i,j][1]), logaritmica(matriz[i,j][2])
        matriz[i,j] = pixel

img.save('Cat_log.jpg')
matriz = img.load()

largura, altura = img.size
print(largura,altura)

print(matriz[0,0])