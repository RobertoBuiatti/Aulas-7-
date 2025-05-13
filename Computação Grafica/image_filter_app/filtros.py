from PIL import Image, ImageFilter, ImageChops
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Configurar backend não-interativo antes de importar pyplot
import matplotlib.pyplot as plt
import io
import base64
from typing import Tuple, Optional, Union
import warnings
warnings.filterwarnings('ignore')  # Ignorar warnings do matplotlib

# Tipos personalizados para melhor legibilidade
ImageType = Union[Image.Image, np.ndarray]

# Configurações globais
MAX_IMAGE_SIZE = (1920, 1080)  # Tamanho máximo permitido
COMPRESSION_QUALITY = 85  # Qualidade da compressão JPEG
DEFAULT_GAMMA = 1.0  # Valor padrão para correção gamma
THRESHOLD_DEFAULT = 128  # Valor padrão para limiarização (P&B)

def validar_e_preparar_imagem(imagem: Image.Image) -> Image.Image:
    """
    Valida e prepara a imagem para processamento.
    Redimensiona se necessário e converte para RGB.
    """
    if imagem.size[0] * imagem.size[1] > MAX_IMAGE_SIZE[0] * MAX_IMAGE_SIZE[1]:
        imagem.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
    
    # Garantir que a imagem está em RGB
    if imagem.mode != 'RGB':
        imagem = imagem.convert('RGB')
    
    return imagem

def processar_em_lotes(imagem: Image.Image,
                      funcao_pixel: callable,
                      tamanho_lote: int = 1000) -> Image.Image:
    """
    Processa a imagem em lotes para melhor performance.
    """
    img_array = np.array(imagem)
    altura, largura = img_array.shape[:2]
    
    for i in range(0, altura, tamanho_lote):
        lote = img_array[i:i + tamanho_lote]
        img_array[i:i + tamanho_lote] = funcao_pixel(lote)
    
    return Image.fromarray(img_array)

def converter_para_cinza(imagem: Image.Image) -> Image.Image:
    """Converte a imagem para escala de cinza."""
    imagem = validar_e_preparar_imagem(imagem)
    return imagem.convert('L').convert('RGB')

def aplicar_preto_e_branco(imagem: Image.Image, threshold: int = THRESHOLD_DEFAULT) -> Image.Image:
    """
    Aplica limiarização na imagem para converter para preto e branco.
    
    Args:
        imagem: Imagem de entrada
        threshold: Valor de limiar (0-255)
    """
    imagem = validar_e_preparar_imagem(imagem)
    imagem_cinza = imagem.convert('L')
    return imagem_cinza.point(lambda x: 0 if x < threshold else 255, '1').convert('RGB')

def aplicar_correcao_gamma(imagem: Image.Image, gamma: float = DEFAULT_GAMMA) -> Image.Image:
    """
    Aplica correção gamma na imagem.
    
    Args:
        imagem: Imagem de entrada
        gamma: Valor do fator gamma (padrão = 1.0)
    """
    imagem = validar_e_preparar_imagem(imagem)
    
    def ajustar_gamma(canal: np.ndarray) -> np.ndarray:
        return np.clip(255 * (canal / 255) ** gamma, 0, 255).astype(np.uint8)
    
    # Converter para array numpy para processamento mais eficiente
    img_array = np.array(imagem)
    
    # Aplicar correção gamma em cada canal
    resultado = np.dstack([ajustar_gamma(img_array[:,:,i]) for i in range(3)])
    
    return Image.fromarray(resultado)

def aplicar_negativo(imagem: Image.Image) -> Image.Image:
    """Aplica o filtro negativo na imagem usando processamento em lote."""
    imagem = validar_e_preparar_imagem(imagem)
    
    def negativo_lote(lote):
        return 255 - lote
    
    return processar_em_lotes(imagem, negativo_lote)

def aplicar_mediana(imagem: Image.Image, tamanho: int = 3) -> Image.Image:
    """Aplica o filtro da mediana na imagem."""
    imagem = validar_e_preparar_imagem(imagem)
    return imagem.filter(ImageFilter.MedianFilter(size=tamanho))

def aplicar_gaussiano(imagem: Image.Image, tamanho: int = 3) -> Image.Image:
    """Aplica o filtro gaussiano na imagem."""
    imagem = validar_e_preparar_imagem(imagem)
    
    # Otimização: Usar filtro gaussiano nativo do PIL para melhor performance
    return imagem.filter(ImageFilter.GaussianBlur(radius=tamanho/2))

def aplicar_sobel(imagem: Image.Image, direcao: str = 'ambos') -> Image.Image:
    """
    Aplica o filtro Sobel na imagem.
    
    Args:
        imagem: Imagem de entrada
        direcao: 'x', 'y' ou 'ambos' para direção do gradiente
    """
    imagem = validar_e_preparar_imagem(imagem)
    
    # Converter para escala de cinza
    imagem = imagem.convert('L')
    
    # Definir kernels Sobel
    kernel_x = ImageFilter.Kernel((3,3), [-1,0,1,-2,0,2,-1,0,1], 1)
    kernel_y = ImageFilter.Kernel((3,3), [-1,-2,-1,0,0,0,1,2,1], 1)
    
    if direcao == 'x':
        resultado = imagem.filter(kernel_x)
    elif direcao == 'y':
        resultado = imagem.filter(kernel_y)
    else:
        sobel_x = imagem.filter(kernel_x)
        sobel_y = imagem.filter(kernel_y)
        resultado = ImageChops.add(sobel_x, sobel_y)
    
    return resultado.convert('RGB')

def aplicar_prewitt(imagem: Image.Image, direcao: str = 'ambos') -> Image.Image:
    """
    Aplica o filtro Prewitt na imagem.
    
    Args:
        imagem: Imagem de entrada
        direcao: 'x', 'y' ou 'ambos' para direção do gradiente
    """
    imagem = validar_e_preparar_imagem(imagem)
    
    # Converter para escala de cinza
    imagem = imagem.convert('L')
    
    # Definir kernels Prewitt
    kernel_x = ImageFilter.Kernel((3,3), [-1,0,1,-1,0,1,-1,0,1], 1)
    kernel_y = ImageFilter.Kernel((3,3), [-1,-1,-1,0,0,0,1,1,1], 1)
    
    if direcao == 'x':
        resultado = imagem.filter(kernel_x)
    elif direcao == 'y':
        resultado = imagem.filter(kernel_y)
    else:
        prewitt_x = imagem.filter(kernel_x)
        prewitt_y = imagem.filter(kernel_y)
        resultado = ImageChops.add(prewitt_x, prewitt_y)
    
    return resultado.convert('RGB')

def aplicar_laplaciano(imagem: Image.Image, tipo: int = 1, realce: bool = False) -> Image.Image:
    """
    Aplica o filtro Laplaciano na imagem.
    
    Args:
        imagem: Imagem de entrada
        tipo: 1 para kernel básico, 2 para kernel estendido
        realce: Se True, realça as bordas na imagem original
    """
    imagem = validar_e_preparar_imagem(imagem)
    
    # Converter para escala de cinza
    imagem = imagem.convert('L')
    
    # Definir kernels Laplaciano
    if tipo == 1:
        kernel = ImageFilter.Kernel((3,3), [0,1,0,1,-4,1,0,1,0], 1)
    else:
        kernel = ImageFilter.Kernel((3,3), [1,1,1,1,-8,1,1,1,1], 1)
    
    # Aplicar filtro
    resultado = imagem.filter(kernel)
    
    if realce:
        # Realçar bordas na imagem original usando ImageChops
        resultado = ImageChops.subtract(imagem, resultado)
    
    return resultado.convert('RGB')

def gerar_histograma(imagem: Image.Image) -> str:
    """Gera o histograma da imagem e retorna como imagem base64."""
    try:
        # Converter para array numpy de forma otimizada
        img_array = np.asarray(imagem)
        
        # Calcular histogramas usando numpy
        if len(img_array.shape) == 3:
            hist_data = [
                np.histogram(img_array[:,:,i].ravel(), bins=256, range=(0,256))[0]
                for i in range(3)
            ]
        else:
            hist_data = [np.histogram(img_array.ravel(), bins=256, range=(0,256))[0]]
        
        # Criar nova figura (thread-safe)
        fig = plt.figure(figsize=(6,4), dpi=100)
        
        # Plotar histogramas
        if len(img_array.shape) == 3:
            cores = ('r', 'g', 'b')
            for hist, cor in zip(hist_data, cores):
                plt.plot(range(256), hist, color=cor, alpha=0.5)
        else:
            plt.plot(range(256), hist_data[0], color='gray', alpha=0.5)
        
        plt.title('Histograma')
        plt.xlabel('Intensidade de Pixel')
        plt.ylabel('Quantidade de Pixels')
        
        # Gerar imagem em memória de forma segura
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png', bbox_inches='tight',
                   pad_inches=0, backend='Agg')
        plt.close('all')  # Fechar todas as figuras
        img_stream.seek(0)
        
        return base64.b64encode(img_stream.getvalue()).decode()
        
    except Exception as e:
        plt.close('all')  # Garantir que todas as figuras são fechadas em caso de erro
        raise e