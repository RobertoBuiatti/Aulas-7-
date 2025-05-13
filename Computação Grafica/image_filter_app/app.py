from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
import os
from datetime import datetime, timedelta
from filtros import *
import logging
import shutil
from werkzeug.utils import secure_filename
import threading
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = os.path.join('static', 'uploads')
PROCESSED_FOLDER = os.path.join('static', 'processed')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
FILE_RETENTION_HOURS = 24  # Tempo de retenção dos arquivos

# Configurar limites de requisição
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def criar_diretorios():
    """Cria os diretórios necessários se não existirem."""
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(PROCESSED_FOLDER, exist_ok=True)
        logger.info("Diretórios criados/verificados com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar diretórios: {str(e)}")
        raise

def limpar_arquivos_antigos():
    """Remove arquivos mais antigos que FILE_RETENTION_HOURS."""
    while True:
        try:
            tempo_limite = datetime.now() - timedelta(hours=FILE_RETENTION_HOURS)
            
            for pasta in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
                for arquivo in os.listdir(pasta):
                    caminho_arquivo = os.path.join(pasta, arquivo)
                    tempo_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
                    
                    if tempo_modificacao < tempo_limite:
                        os.remove(caminho_arquivo)
                        logger.info(f"Arquivo removido: {arquivo}")
                        
        except Exception as e:
            logger.error(f"Erro na limpeza de arquivos: {str(e)}")
            
        time.sleep(3600)  # Espera 1 hora antes da próxima verificação

# Iniciar thread de limpeza
threading.Thread(target=limpar_arquivos_antigos, daemon=True).start()

# Criar diretórios na inicialização
criar_diretorios()

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida e nome seguro."""
    if not '.' in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    filename_base = secure_filename(filename.rsplit('.', 1)[0].lower())
    
    return ext in ALLOWED_EXTENSIONS and len(filename_base) > 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar_imagem():
    """Processa a imagem aplicando o filtro selecionado."""
    try:
        # Validar arquivo
        if 'imagem' not in request.files:
            return jsonify({'erro': 'Nenhuma imagem enviada'}), 400
        
        arquivo = request.files['imagem']
        if arquivo.filename == '':
            return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(arquivo.filename):
            return jsonify({'erro': 'Nome de arquivo ou tipo não permitido'}), 400
        
        # Verificar tamanho do arquivo
        arquivo.seek(0, os.SEEK_END)
        tamanho = arquivo.tell()
        arquivo.seek(0)
        
        if tamanho > MAX_FILE_SIZE:
            return jsonify({'erro': 'Arquivo muito grande (máximo 10MB)'}), 400

        # Gerar nomes únicos seguros para os arquivos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_base = secure_filename(arquivo.filename.rsplit('.', 1)[0])
        nome_original = f'original_{nome_base}_{timestamp}.jpg'
        nome_processado = f'processado_{nome_base}_{timestamp}.jpg'
        
        # Salvar imagem original
        caminho_original = os.path.join(UPLOAD_FOLDER, nome_original)
        try:
            arquivo.save(caminho_original)
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {str(e)}")
            return jsonify({'erro': 'Erro ao salvar arquivo'}), 500
        
        # Abrir e validar imagem com PIL
        try:
            imagem = Image.open(caminho_original)
        except Exception as e:
            os.remove(caminho_original)
            logger.error(f"Erro ao abrir imagem: {str(e)}")
            return jsonify({'erro': 'Arquivo não é uma imagem válida'}), 400
        
        # Obter e validar parâmetros
        try:
            filtro = request.form.get('filtro', 'negativo')
            tamanho_kernel = min(max(int(request.form.get('tamanho_kernel', 3)), 3), 7)
            direcao = request.form.get('direcao', 'ambos')
            tipo_laplaciano = min(max(int(request.form.get('tipo_laplaciano', 1)), 1), 2)
            gamma = float(request.form.get('gamma', DEFAULT_GAMMA))
            threshold = min(max(int(request.form.get('threshold', THRESHOLD_DEFAULT)), 0), 255)
            realce_bordas = request.form.get('realce_bordas', 'false').lower() == 'true'
            pre_processamento = request.form.get('pre_processamento', 'false').lower() == 'true'
            
            # Aplicar pré-processamento em escala de cinza se solicitado
            if pre_processamento and filtro in ['sobel', 'prewitt', 'laplaciano']:
                imagem = converter_para_cinza(imagem)
            
            # Aplicar filtro selecionado
            if filtro == 'negativo':
                imagem_processada = aplicar_negativo(imagem)
            elif filtro == 'mediana':
                imagem_processada = aplicar_mediana(imagem, tamanho_kernel)
            elif filtro == 'gaussiano':
                imagem_processada = aplicar_gaussiano(imagem, tamanho_kernel)
            elif filtro == 'sobel':
                imagem_processada = aplicar_sobel(imagem, direcao)
            elif filtro == 'prewitt':
                imagem_processada = aplicar_prewitt(imagem, direcao)
            elif filtro == 'laplaciano':
                imagem_processada = aplicar_laplaciano(imagem, tipo_laplaciano, realce_bordas)
            elif filtro == 'cinza':
                imagem_processada = converter_para_cinza(imagem)
            elif filtro == 'preto_branco':
                imagem_processada = aplicar_preto_e_branco(imagem, threshold)
            elif filtro == 'gamma':
                imagem_processada = aplicar_correcao_gamma(imagem, gamma)
            else:
                raise ValueError('Filtro não reconhecido')
            
            # Salvar imagem processada
            caminho_processado = os.path.join(PROCESSED_FOLDER, nome_processado)
            imagem_processada.save(caminho_processado, quality=95, optimize=True)
            
            # Gerar histogramas
            histograma_original = gerar_histograma(imagem)
            histograma_processado = gerar_histograma(imagem_processada)
            
            # Liberar memória
            imagem.close()
            imagem_processada.close()
            
            return jsonify({
                'imagem_original': os.path.join('static', 'uploads', nome_original),
                'imagem_processada': os.path.join('static', 'processed', nome_processado),
                'histograma_original': histograma_original,
                'histograma_processado': histograma_processado
            })
            
        except Exception as e:
            # Limpar arquivos em caso de erro
            os.remove(caminho_original)
            logger.error(f"Erro no processamento: {str(e)}")
            return jsonify({'erro': 'Erro ao processar imagem'}), 500
            
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/download/<path:filename>')
def download(filename):
    """Endpoint para download da imagem processada."""
    try:
        filename = secure_filename(filename)
        if not os.path.exists(os.path.join(PROCESSED_FOLDER, filename)):
            return jsonify({'erro': 'Arquivo não encontrado'}), 404
            
        return send_file(
            os.path.join(PROCESSED_FOLDER, filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Erro no download: {str(e)}")
        return jsonify({'erro': 'Erro ao baixar arquivo'}), 500

if __name__ == '__main__':
    # Configurar host e porta
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)