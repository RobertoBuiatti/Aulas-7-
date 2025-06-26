import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import glob
import os

def preprocessar_imagem(gray):
    """
    Pré-processamento otimizado para diferentes tipos de objeto.
    """
    print("🔧 Pré-processamento otimizado...")
    
    # Aplicar CLAHE primeiro para melhorar contraste
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Filtro bilateral mais suave para preservar bordas
    bilateral = cv2.bilateralFilter(enhanced, 15, 80, 80)
    
    # Filtro mediano pequeno para remover ruído pontual
    median = cv2.medianBlur(bilateral, 3)
    
    return median

def deteccao_multi_threshold(img_processed):
    """
    Múltiplas técnicas de binarização para capturar diferentes objetos.
    """
    print("📊 Aplicando múltiplos thresholds...")
    
    # 1. Otsu - para objetos com contraste claro
    _, binary_otsu = cv2.threshold(img_processed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 2. Adaptativo Gaussiano com parâmetros mais sensíveis
    binary_adaptive1 = cv2.adaptiveThreshold(img_processed, 255, 
                                           cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                           cv2.THRESH_BINARY, 21, 5)
    
    # 3. Adaptativo com bloco menor para objetos pequenos
    binary_adaptive2 = cv2.adaptiveThreshold(img_processed, 255, 
                                           cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                           cv2.THRESH_BINARY, 11, 3)
    
    # 4. Triangle threshold
    _, binary_triangle = cv2.threshold(img_processed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
    
    # 5. Threshold manual baseado na distribuição
    hist = cv2.calcHist([img_processed], [0], None, [256], [0, 256])
    threshold_manual = np.argmax(hist) - 20  # Pico principal menos offset
    threshold_manual = max(50, min(200, threshold_manual))  # Limitar entre 50-200
    _, binary_manual = cv2.threshold(img_processed, threshold_manual, 255, cv2.THRESH_BINARY)
    
    # Combinar resultados usando operação OR para capturar mais objetos
    combined1 = cv2.bitwise_or(binary_adaptive1, binary_adaptive2)
    combined2 = cv2.bitwise_or(binary_otsu, binary_triangle)
    combined3 = cv2.bitwise_or(combined1, binary_manual)
    final_binary = cv2.bitwise_or(combined2, combined3)
    
    # Auto-inversão baseada na densidade de pixels brancos
    white_ratio = np.sum(final_binary == 255) / final_binary.size
    if white_ratio > 0.6:  # Se mais de 60% é branco, inverter
        final_binary = cv2.bitwise_not(final_binary)
        print("   🔄 Imagem invertida automaticamente")
    
    print(f"   📈 Densidade de objetos: {(1-white_ratio)*100:.1f}%")
    
    return final_binary

def limpeza_morfologica_suave(binary):
    """
    Limpeza morfológica mais conservadora para preservar objetos pequenos.
    """
    print("🧹 Limpeza morfológica suave...")
    
    # Kernels menores para não perder objetos pequenos
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    kernel_medium = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    
    # Sequência de operações mais conservadora
    
    # 1. Abertura muito suave para remover apenas ruído pequeno
    morph = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_small, iterations=1)
    
    # 2. Fechamento suave para preencher pequenos buracos
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel_medium, iterations=1)
    
    # 3. Dilatação mínima para conectar partes próximas
    morph = cv2.dilate(morph, kernel_small, iterations=1)
    
    return morph

def detectar_objetos_watershed_melhorado(morph_img, original_shape):
    """
    Watershed melhorado para separar objetos grudados.
    """
    print("🌊 Aplicando watershed melhorado...")
    
    # Transformada de distância
    dist_transform = cv2.distanceTransform(morph_img, cv2.DIST_L2, 5)
    
    # Threshold adaptativo baseado na distribuição de distâncias
    dist_flat = dist_transform[dist_transform > 0]
    if len(dist_flat) > 0:
        threshold_dist = np.percentile(dist_flat, 70)  # 70º percentil
        threshold_dist = max(threshold_dist, 0.3 * dist_transform.max())
    else:
        threshold_dist = 0.3 * dist_transform.max()
    
    _, sure_fg = cv2.threshold(dist_transform, threshold_dist, 255, 0)
    
    # Área de fundo (background)
    kernel = np.ones((3,3), np.uint8)
    sure_bg = cv2.dilate(morph_img, kernel, iterations=2)
    
    # Área incerta
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Componentes conectados
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    
    # Aplicar watershed
    img_colored = cv2.cvtColor(morph_img, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(img_colored, markers)
    
    # Criar máscara final
    result = np.zeros_like(morph_img)
    result[markers > 1] = 255
    
    num_objects = len(np.unique(markers)) - 2  # -2 para remover background e unknown
    print(f"   🎯 Watershed detectou {num_objects} regiões")
    
    return result

def filtros_contorno_relaxados(contours, img_shape, area_minima=50):
    """
    Filtros mais relaxados para não perder objetos válidos.
    """
    print("🔍 Aplicando filtros relaxados...")
    
    contornos_validos = []
    img_area = img_shape[0] * img_shape[1]
    
    # Calcular área média dos contornos para threshold dinâmico
    areas = [cv2.contourArea(cnt) for cnt in contours if cv2.contourArea(cnt) > 10]
    if areas:
        area_media = np.median(areas)
        area_minima_dinamica = max(area_minima, area_media * 0.1)  # 10% da mediana
    else:
        area_minima_dinamica = area_minima
    
    print(f"   📏 Área mínima dinâmica: {area_minima_dinamica:.0f} pixels")
    
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        
        # Filtro básico de área
        if area < area_minima_dinamica:
            continue
        if area > img_area * 0.7:  # Não pode ser mais que 70% da imagem
            continue
        
        # Filtros mais permissivos
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
        
        # Bounding box
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h if h > 0 else 0
        
        # Extent
        rect_area = w * h
        extent = float(area) / rect_area if rect_area > 0 else 0
        
        # Critérios muito relaxados
        if (area > area_minima_dinamica and 
            0.05 < aspect_ratio < 20.0 and  # Muito permissivo para aspect ratio
            extent > 0.1):  # Extent mínimo muito baixo
            
            contornos_validos.append(cnt)
            print(f"   ✅ Objeto {len(contornos_validos)}: área={area:.0f}, "
                  f"aspect={aspect_ratio:.2f}, extent={extent:.2f}")
    
    return contornos_validos

def detectar_objetos_complementar(img_original, binary_main):
    """
    Detecção complementar usando diferentes abordagens.
    """
    print("🔄 Detecção complementar...")
    
    gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    
    # Abordagem 1: Detecção de bordas
    edges = cv2.Canny(gray, 50, 150)
    edges_dilated = cv2.dilate(edges, np.ones((2,2), np.uint8), iterations=1)
    
    # Abordagem 2: Threshold inverso
    binary_inv = cv2.bitwise_not(binary_main)
    
    # Combinar abordagens
    combined = cv2.bitwise_or(binary_main, edges_dilated)
    
    return combined

def contar_objetos_otimizado(caminho_imagem, area_minima=50, debug=False):
    """
    Função principal otimizada para contagem de objetos.
    """
    print(f"\n📸 Processando: {caminho_imagem}")
    
    # Carregar imagem
    img_original = cv2.imread(caminho_imagem)
    if img_original is None:
        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")
    
    print(f"   📏 Dimensões: {img_original.shape[1]}x{img_original.shape[0]} pixels")
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    
    # Pré-processamento
    img_processed = preprocessar_imagem(gray)
    
    # Detecção multi-threshold
    binary_main = deteccao_multi_threshold(img_processed)
    
    # Limpeza morfológica suave
    morph_clean = limpeza_morfologica_suave(binary_main)
    
    # Aplicar watershed
    watershed_result = detectar_objetos_watershed_melhorado(morph_clean, img_original.shape[:2])
    
    # Detecção complementar
    binary_combined = detectar_objetos_complementar(img_original, watershed_result)
    
    # Encontrar contornos
    print("🔍 Encontrando contornos...")
    contours, _ = cv2.findContours(binary_combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"   📊 Contornos encontrados: {len(contours)}")
    
    # Filtrar contornos com critérios relaxados
    contornos_validos = filtros_contorno_relaxados(contours, img_original.shape[:2], area_minima)
    
    # Criar visualização
    img_resultado = img_original.copy()
    
    # Cores para diferentes objetos
    cores = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), 
             (255, 0, 255), (0, 255, 255), (128, 255, 0), (255, 128, 0)]
    
    for i, cnt in enumerate(contornos_validos):
        cor = cores[i % len(cores)]
        
        # Desenhar contorno mais grosso
        cv2.drawContours(img_resultado, [cnt], -1, cor, 3)
        
        # Calcular centro
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Círculo com número maior
            cv2.circle(img_resultado, (cx, cy), 15, (0, 0, 0), -1)
            cv2.circle(img_resultado, (cx, cy), 15, (255, 255, 255), 3)
            cv2.putText(img_resultado, str(i+1), (cx-8, cy+5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    contagem_final = len(contornos_validos)
    
    # Adicionar texto com resultado
    cv2.rectangle(img_resultado, (10, 10), (160, 35), (0, 0, 0), -1)
    cv2.putText(img_resultado, f"OBJETOS DETECTADOS: {contagem_final}", 
            (15, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
    
    print(f"\n🎯 RESULTADO FINAL: {contagem_final} objetos detectados")
    
    if debug:
        # Mostrar etapas intermediárias
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 3, 1)
        plt.imshow(cv2.cvtColor(img_original, cv2.COLOR_BGR2RGB))
        plt.title('Original')
        plt.axis('off')
        
        plt.subplot(2, 3, 2)
        plt.imshow(img_processed, cmap='gray')
        plt.title('Pré-processado')
        plt.axis('off')
        
        plt.subplot(2, 3, 3)
        plt.imshow(binary_main, cmap='gray')
        plt.title('Binarizado')
        plt.axis('off')
        
        plt.subplot(2, 3, 4)
        plt.imshow(morph_clean, cmap='gray')
        plt.title('Morfologia')
        plt.axis('off')
        
        plt.subplot(2, 3, 5)
        plt.imshow(binary_combined, cmap='gray')
        plt.title('Final Combinado')
        plt.axis('off')
        
        plt.subplot(2, 3, 6)
        plt.imshow(cv2.cvtColor(img_resultado, cv2.COLOR_BGR2RGB))
        plt.title(f'Resultado: {contagem_final} objetos')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    return img_resultado, contagem_final, binary_combined

def main():
    """Execução principal"""
    print("🚀 CONTADOR DE OBJETOS OTIMIZADO")
    print("=" * 50)
    
    # Lista de imagens para processar
    imagens = glob.glob('images/*.png') + glob.glob('images/*.jpg') + glob.glob('images/*.jpeg')

    # Pasta de saída
    pasta_saida = 'output'
    os.makedirs(pasta_saida, exist_ok=True)
    
    for caminho in imagens:
        print(f"\n{'='*60}")
        print(f"🔍 PROCESSANDO: {caminho}")
        print(f"{'='*60}")
        
        try:
            # Processar imagem
            img_resultado, contagem, mask_final = contar_objetos_otimizado(
                caminho, area_minima=30, debug=False
            )
            
            # Nome base da imagem (sem caminho e sem extensão)
            nome_base = os.path.splitext(os.path.basename(caminho))[0]
            
            # Caminhos de saída
            caminho_resultado = os.path.join(pasta_saida, f'resultado_otimizado_{nome_base}.png')
            caminho_mascara = os.path.join(pasta_saida, f'mask_{nome_base}.png')
            
            # Salvar resultados
            cv2.imwrite(caminho_resultado, img_resultado)
            cv2.imwrite(caminho_mascara, mask_final)
            
            print(f"💾 Resultado salvo em: {caminho_resultado}")
            print(f"💾 Máscara salva em: {caminho_mascara}")
            print(f"📊 CONTAGEM FINAL: {contagem} objetos")
            
            # Mostrar resultados
            cv2.imshow(f"Resultado Otimizado - {nome_base}", img_resultado)
            cv2.imshow(f"Máscara Final - {nome_base}", mask_final)
            cv2.imshow(f"Original - {nome_base}", cv2.imread(caminho))
            
            print(f"👆 Pressione qualquer tecla para continuar...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✨ Processamento concluído!")

if __name__ == "__main__":
    main()