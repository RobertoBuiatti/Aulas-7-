from PIL import Image
import math

#Abrir a imagem
img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula2/panda.jpg')

#Carregar a imagem
matriz = img.load()

#Pegar o tamanho da imagem
largura, altura = img.size
print(largura, altura)

#Formato da matriz (tupla)
matriz[0,0]

# #Percorrer a imagem pixel a pixel e Filtro Negativo
# for i in range(largura):
#     for j in range(altura):
#         pixel = (255 - matriz[i,j][0], 255 - matriz[i,j][1], 255 - matriz[i,j][2])
#         matriz[i,j] = pixel

# #Salvar a imagem
# img.save('panda_negativo.jpg')

# #Coreção de gamma
# def gama(pixel, gama):
#     return int(pow((pixel/255), gama) * 255)

# #Percorrer a imagem pixel a pixel e Filtro Gamma
# fator = 0.5
# for i in range(largura):
#     for j in range(altura):
#         pixel = (gama(matriz[i,j][0], fator), gama(matriz[i,j][1], fator), gama(matriz[i,j][2], fator))
#         matriz[i,j] = pixel

# #Salvar a imagem
# img.save('panda_gamma.jpg')

# #Filtro Logaritmo
# def log(pixel):
#     c = 255 / math.log(256)
#     return int(c * math.log(1 + pixel))

# #Percorrer a imagem pixel a pixel e Filtro Logaritmo
# for i in range(largura):
#     for j in range(altura):
#         pixel = (log(matriz[i,j][0]), log(matriz[i,j][1]), log(matriz[i,j][2]))
#         matriz[i,j] = pixel
        
# #Salvar a imagem
# img.save('panda_log.jpg')

#Colorida para cinza
#Percorrer a imagem pixel a pixel e Filtro Cinza
for i in range(largura):
    for j in range(altura):
        media = (matriz[i,j][0] + matriz[i,j][1] + matriz[i,j][2]) / 3
        media = int(media)
        pixel = (media, media, media)
        matriz[i,j] = pixel

#Salvar a imagem   
img.save('panda_cinza.jpg')

#Colorida para cinza
#Percorrer a imagem pixel a pixel e Filtro Cinza
for i in range(largura):
    for j in range(altura):
        media = (matriz[i,j][0] + matriz[i,j][1] + matriz[i,j][2]) / 3
        media = 0 if int(media) < 128 else 255
        media = int(media)
        pixel = (media, media, media)
        matriz[i,j] = pixel

#Salvar a imagem   
img.save('panda_pretoBranco.jpg')
