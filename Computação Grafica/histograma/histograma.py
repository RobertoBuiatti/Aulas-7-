from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def equalizar_histograma(imagem_pil):
    imagem = np.array(imagem_pil)
    histograma, bins = np.histogram(imagem.flatten(), bins=256, range=[0, 256])
    cdf = histograma.cumsum()
    cdf_normalizada = cdf * 255 / cdf[-1]
    imagem_equalizada = np.interp(imagem.flatten(), bins[:-1], cdf_normalizada)
    return Image.fromarray(imagem_equalizada.reshape(imagem.shape).astype('uint8'))


imagem = Image.open('Aulas-7-\Computação Grafica\histograma\cat.jpg').convert('L')
imagem_eq = equalizar_histograma(imagem)

imagem_eq.save('cat_eq.jpg')

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
