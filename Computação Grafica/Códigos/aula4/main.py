from PIL import Image, ImageFilter, ImageChops

imagem = Image.open('C:/Users/10695691600/Documents/7-Periodo/Computação Gráfica/Códigos/aula4/dog.jpg').convert('L')

#Sobel
mask_x = [-1,0,1,-2,0,2,-1,0,0]
mask_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
kernel_sobel_x = ImageFilter.Kernel((3, 3), mask_x, 1)
kernel_sobel_y = ImageFilter.Kernel((3, 3), mask_y, 1)
sobel_x = imagem.filter(kernel_sobel_x)
sobel_y = imagem.filter(kernel_sobel_y)
sobel_f = ImageChops.add(sobel_x, sobel_y)
sobel_x.save("sobel_x.jpg")
sobel_y.save("sobel_y.jpg")
sobel_f.save("sobel_f.jpg")

#Laplaciano
mask_la1 = [0, 1, 0, 1, -4, 1, 0, 1, 0]
mask_la2 = [1, 1, 1, 1, -8, 1, 1, 1, 1]
laplaciano1 = imagem.filter(ImageFilter.Kernel((3, 3), mask_la1, 1))
laplaciano1.save('laplaciano1.jpg')
laplaciano2 = imagem.filter(ImageFilter.Kernel((3, 3), mask_la2, 1))
laplaciano2.save('laplaciano2.jpg')

#Prewitt
mask_x = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
mask_y = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
kernel_prewitt_x = ImageFilter.Kernel((3, 3), mask_x, 1)
kernel_prewitt_y = ImageFilter.Kernel((3, 3), mask_y, 1)
prewitt_X = imagem.filter(kernel_prewitt_x)
prewitt_Y = imagem.filter(kernel_prewitt_y)
prewitt_f = ImageChops.add(prewitt_X, prewitt_Y)
prewitt_X.save("prewitt_x.jpg")
prewitt_Y.save("prewitt_y.jpg")
prewitt_f.save("prewitt_f.jpg")