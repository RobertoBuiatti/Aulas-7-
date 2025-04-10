from PIL import Image, ImageFilter

# #Nitidez
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/pratica/dog.jpg')
# size = (3,3)
# mask = (1, 0 -1, 0, 0, 0, -1, 0, 1) #Detecção de Bordas
# mask = (1,1,1,1,1,1,1,1,1)
# mask = tuple(x/9 for x in mask) #Blur
# mask = (0,-1, 0, -1, 5, -1, 0, -1, 0) #Sharpen
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)
# #Aplicar o kernel
# img2 = img.filter(kernel)
# img2.save('dog1.jpg')

# #Traço
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/pratica/dog.jpg')
# #Criar o kernel
# size = (3,3)
# mask = (0,1,0,1,-4,1,0,1,0) #Detecção de Bordas
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)
# #Aplicar o kernel
# img2 = img.filter(kernel)
# img2.save('dog2.jpg')

# #Traço
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/pratica/dog.jpg')
# #Criar o kernel
# size = (3,3)
# mask = (-1,-1,-1,-1,8,-1,-1,-1,-1) #Detecção de Bordas
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)
# #Aplicar o kernel
# img2 = img.filter(kernel)
# img2.save('dog3.jpg')

# #Nitidez
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/pratica/dog.jpg')
# size = (3,3)
# mask = (0,-1,0,-1,5,-1,0,-1,0) #Detecção de Bordas
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)
# img2 = img.filter(kernel)
# img2.save('dog4.jpg')

# #Nitidez
# img = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/aula3/pratica/dog.jpg')
# size = (3,3)
# mask = (1, 0 -1, 0, 0, 0, -1, 0, 1) #Detecção de Bordas
# mask = (1,1,1,1,1,1,1,1,1)
# mask = tuple(x/9 for x in mask) #Blur
# mask = (0,-1, 0, -1, 5, -1, 0, -1, 0) #Sharpen
# scale = 1
# offset = 0
# kernel = ImageFilter.Kernel(size, mask, scale, offset)
# #Aplicar o kernel
# img2 = img.filter(kernel)
# img2.save('dog1.jpg')