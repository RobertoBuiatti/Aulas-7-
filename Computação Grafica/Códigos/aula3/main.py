from PIL import Image, ImageFilter

##Traço
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/dog.jpg')

# #Criar o kernel
# size = (3,3)
# mask = (-1,-1, -1, -1, 8, -1, -1, -1, -1)
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)

# #Aplicar o kernel
# img2 = img.filter(kernel)
# img2.save('cachorrofiltro.jpg')



# #Blur
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/dog.jpg')

# size = (3,3)
# mask = (-1,-1, -1, -1, 8, -1, -1, -1, -1)
# mask = (1,1,1,1,1,1,1,1,1)
# mask = tuple(x/9 for x in mask)
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)

# img2 = img.filter(kernel)
# img2.save('cachorroblur.jpg')



# #Sharpen
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/cachorroblur.jpg')

# size = (3,3)
# mask = (-1,-1, -1, -1, 8, -1, -1, -1, -1) #Detecção de Bordas
# mask = (1,1,1,1,1,1,1,1,1)
# mask = tuple(x/9 for x in mask) #Blur
# mask = (0,-1, 0, -1, 5, -1, 0, -1, 0) #Sharpen
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)

# img2 = img.filter(kernel)
# img2.save('cachorrosharpen.jpg')

# Com Ruido
import  numpy as np
import random

def aplicar_ruido(img, prob):
    output = np.array(img)
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            rnd = random.random()
            if rnd < prob:
                output[i][j] = 0 #preto
            elif rnd > 1 - prob:
                output[i][j] = 255 #branco
    return Image.fromarray(output)

img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/dog.jpg')
img2 = aplicar_ruido(img, 0.05)
img2.save('cachorroruido.jpg')

#Filtro de Mediana
img3 = img2.filter(ImageFilter.MedianFilter(size=3))
img3.save('cachorroruidomediana.jpg')

#Sharpen
img4 = img3.filter(ImageFilter.SHARPEN)
img4.save('cachorroruidomedianasharpen.jpg')