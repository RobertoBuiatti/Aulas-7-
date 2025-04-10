from PIL import Image, ImageFilter, ImageChops, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import random


def equalizar_histograma(imagem_pil):
    imagem = np.array(imagem_pil)
    histograma, bins = np.histogram(imagem.flatten(), bins=256, range=[0, 256])
    cdf = histograma.cumsum()
    cdf_normalizada = cdf * 255 / cdf[-1]
    imagem_equalizada = np.interp(imagem.flatten(), bins[:-1], cdf_normalizada)
    return Image.fromarray(imagem_equalizada.reshape(imagem.shape).astype('uint8'))


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


def deteccao_bordas(img, save_path, image_name):
    # Masks for Sobel operator
    mask_x = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    mask_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

    # Sobel kernels
    kernel_sobel_x = ImageFilter.Kernel((3, 3), mask_x, 1)
    kernel_sobel_y = ImageFilter.Kernel((3, 3), mask_y, 1)

    # Apply Sobel filters
    sobel_x = img.filter(kernel_sobel_x)
    sobel_y = img.filter(kernel_sobel_y)
    
    # Combine Sobel results using ImageChops
    sobel_f = ImageChops.add(sobel_x, sobel_y)
    
    # Ensuring the pixel values stay in the valid range (0-255)
    sobel_f = ImageEnhance.Brightness(sobel_f).enhance(2.0)  # Adjust brightness to improve visibility
    sobel_f = sobel_f.convert("L")

    # Save Sobel results with unique names
    sobel_x.save(f'{save_path}/{image_name}_sobel_x.jpg')
    sobel_y.save(f'{save_path}/{image_name}_sobel_y.jpg')
    sobel_f.save(f'{save_path}/{image_name}_sobel_f.jpg')

    # Masks for Laplacian operator
    mask_la1 = [0, 1, 0, 1, -4, 1, 0, 1, 0]
    mask_la2 = [1, 1, 1, 1, -8, 1, 1, 1, 1]

    # Apply Laplacian filters
    laplaciano1 = img.filter(ImageFilter.Kernel((3, 3), mask_la1, 1))
    laplaciano2 = img.filter(ImageFilter.Kernel((3, 3), mask_la2, 1))

    # Save Laplacian results with unique names
    laplaciano1.save(f'{save_path}/{image_name}_laplaciano1.jpg')
    laplaciano2.save(f'{save_path}/{image_name}_laplaciano2.jpg')

    # Masks for Prewitt operator
    mask_x_pre = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
    mask_y_pre = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

    # Prewitt kernels
    kernel_prewitt_x = ImageFilter.Kernel((3, 3), mask_x_pre, 1)
    kernel_prewitt_y = ImageFilter.Kernel((3, 3), mask_y_pre, 1)

    # Apply Prewitt filters
    prewitt_x = img.filter(kernel_prewitt_x)
    prewitt_y = img.filter(kernel_prewitt_y)
    
    # Combine Prewitt results using ImageChops
    prewitt_f = ImageChops.add(prewitt_x, prewitt_y)
    
    # Ensuring the pixel values stay in the valid range (0-255)
    prewitt_f = ImageEnhance.Brightness(prewitt_f).enhance(2.0)  # Adjust brightness to improve visibility
    prewitt_f = prewitt_f.convert("L")

    # Save Prewitt results with unique names
    prewitt_x.save(f'{save_path}/{image_name}_prewitt_x.jpg')
    prewitt_y.save(f'{save_path}/{image_name}_prewitt_y.jpg')
    prewitt_f.save(f'{save_path}/{image_name}_prewitt_f.jpg')


imagem = Image.open('Aulas-7-\Computação Grafica\histograma\cat.jpg').convert('L')
imagem1 = Image.open('Aulas-7-\Computação Grafica\histograma\\abandeira.jpg').convert('L')
imagem_eq = equalizar_histograma(imagem)
imagem_eq1 = aplicar_ruido(imagem, 0.05)
imagem_eq1 = equalizar_histograma(imagem_eq)
deteccao_bordas(imagem_eq1, '.', 'cat_eq1')

imagem_eq2 = equalizar_histograma(imagem1)
imagem_eq3 = aplicar_ruido(imagem1, 0.05)
imagem_eq3 = equalizar_histograma(imagem_eq2)
deteccao_bordas(imagem_eq2, '.', 'bandeira_eq2')

# Save the equalized images
imagem_eq.save('cat_eq.jpg')
imagem_eq1.save('cat_eq1.jpg')

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 6))

# Original image
axs[0, 0].imshow(imagem, cmap='gray')
axs[0, 0].set_title('Original')
axs[0, 0].axis('off')

# Original histogram
axs[0, 1].hist(np.array(imagem).flatten(), bins=256, range=(0, 256), color='gray')
axs[0, 1].set_title('Histograma Original')

# Equalized image
axs[1, 0].imshow(imagem_eq, cmap='gray')
axs[1, 0].set_title('Imagem Equalizada')
axs[1, 0].axis('off')

# Equalized histogram
axs[1, 1].hist(np.array(imagem_eq).flatten(), bins=256, range=(0, 256), color='gray')
axs[1, 1].set_title('Histograma Equalizado')

plt.tight_layout()
plt.show()
