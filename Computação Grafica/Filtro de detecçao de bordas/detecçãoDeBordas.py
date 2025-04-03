from PIL import Image, ImageFilter, ImageChops
import math

#colorida
img = Image.open(r'C:\Users\08401822602\Desktop\7-periodo\Aulas-7-\Computação Grafica\Filtro de detecçao de bordas\bandeira.jpg')
save_path = r'C:\Users\08401822602\Desktop\7-periodo\Aulas-7-\Computação Grafica\Filtro de detecçao de bordas'


mask_x = [-1,0,1,-2,0,2,-1,0,1]
mask_y = [-1,-2,-1,0,0,0,1,2,1]
kernel_sobel_x = ImageFilter.Kernel((3,3), mask_x, 1)
kernel_sobel_y = ImageFilter.Kernel((3,3), mask_y, 1)

#aplicar os filtros
sobel_x = img.filter(kernel_sobel_x)
sobel_y = img.filter(kernel_sobel_y)
sobel_f = ImageChops.add(sobel_x, sobel_y)

sobel_x.save(f'{save_path}\\sobel_x.jpg')
sobel_y.save(f'{save_path}\\sobel_y.jpg')
sobel_f.save(f'{save_path}\\sobel_f.jpg')

#laplaciano

mask_la1 = [0,1,0,1,-4,1,0,1,0]
mask_la2 = [1,1,1,1,-8,1,1,1,1]
laplaciano1 = img.filter(ImageFilter.Kernel((3,3), mask_la1,1))
laplaciano2 = img.filter(ImageFilter.Kernel((3,3), mask_la2,1))

laplaciano1.save(f'{save_path}\\laplaciano1.jpg')
laplaciano2.save(f'{save_path}\\laplaciano2.jpg')

#prewitt
mask_x = [-1,0,1,-1,0,1,-1,0,1]
mask_y = [-1,-2,-1,0,0,0,1,2,1]

kernel_prewitt_x = ImageFilter.Kernel((3,3), mask_x,1)
kernel_prewitt_y = ImageFilter.Kernel((3,3), mask_y,1)
prewitt_x = img.filter(kernel_prewitt_x)
prewitt_y = img.filter(kernel_prewitt_y)
prewitt_f = ImageChops.add(prewitt_x, prewitt_y)
prewitt_x.save(f'{save_path}\\prewitt_x.jpg')
prewitt_y.save(f'{save_path}\\prewitt_y.jpg')
prewitt_f.save(f'{save_path}\\prewitt_f.jpg')





#escala de cinza
img = Image.open(r'C:\Users\08401822602\Desktop\7-periodo\Aulas-7-\Computação Grafica\Filtro de detecçao de bordas\bandeira.jpg').convert('L')
save_path = r'C:\Users\08401822602\Desktop\7-periodo\Aulas-7-\Computação Grafica\Filtro de detecçao de bordas'


mask_x = [-1,0,1,-2,0,2,-1,0,1]
mask_y = [-1,-2,-1,0,0,0,1,2,1]
kernel_sobel_x = ImageFilter.Kernel((3,3), mask_x, 1)
kernel_sobel_y = ImageFilter.Kernel((3,3), mask_y, 1)

#aplicar os filtros
sobel_x = img.filter(kernel_sobel_x)
sobel_y = img.filter(kernel_sobel_y)
sobel_f = ImageChops.add(sobel_x, sobel_y)

sobel_x.save(f'{save_path}\\sobel_x_Cinza.jpg')
sobel_y.save(f'{save_path}\\sobel_y_Cinza.jpg')
sobel_f.save(f'{save_path}\\sobel_f_Cinza.jpg')

#laplaciano

mask_la1 = [0,1,0,1,-4,1,0,1,0]
mask_la2 = [1,1,1,1,-8,1,1,1,1]
laplaciano1 = img.filter(ImageFilter.Kernel((3,3), mask_la1,1))
laplaciano2 = img.filter(ImageFilter.Kernel((3,3), mask_la2,1))

laplaciano1.save(f'{save_path}\\laplaciano1_Cinza.jpg')
laplaciano2.save(f'{save_path}\\laplaciano2_Cinza.jpg')

#prewitt
mask_x = [-1,0,1,-1,0,1,-1,0,1]
mask_y = [-1,-2,-1,0,0,0,1,2,1]

kernel_prewitt_x = ImageFilter.Kernel((3,3), mask_x,1)
kernel_prewitt_y = ImageFilter.Kernel((3,3), mask_y,1)
prewitt_x = img.filter(kernel_prewitt_x)
prewitt_y = img.filter(kernel_prewitt_y)
prewitt_f = ImageChops.add(prewitt_x, prewitt_y)
prewitt_x.save(f'{save_path}\\prewitt_x_Cinza.jpg')
prewitt_y.save(f'{save_path}\\prewitt_y_Cinza.jpg')
prewitt_f.save(f'{save_path}\\prewitt_f_Cinza.jpg')