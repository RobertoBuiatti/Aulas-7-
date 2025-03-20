from PIL import Image
import math

img = Image.open('cat.jpg')

matriz = img.load()

largura, altura = img.size
print(largura,altura)


print(matriz[0,0])

for i in range(largura):
    for j in range(altura):
        pixel = ((255 - matriz[i,j][0]), (255 - matriz[i,j][1]), (255 - matriz[i,j][2]))
        matriz[i,j] = pixel

img.save('cat_negativo.jpg')