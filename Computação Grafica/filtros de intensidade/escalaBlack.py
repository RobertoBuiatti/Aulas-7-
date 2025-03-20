from PIL import Image
import math


img = Image.open('cat.jpg')

matriz = img.load()

largura, altura = img.size
print(largura,altura)

print(matriz[0,0])


for i in range(largura):
        for j in range(altura):
            media = (matriz[i,j][0])+ (matriz[i,j][1])+ (matriz[i,j][2])/3
            media = 0 if int(media) <= 128 else 255
            pixel = (media, media, media)
            matriz[i,j] = pixel

img.save('Cat_Black.jpg')
matriz = img.load()

largura, altura = img.size
print(largura,altura)

print(matriz[0,0])