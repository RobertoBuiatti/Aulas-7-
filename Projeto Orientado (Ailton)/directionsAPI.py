import requests
import json
import os
from typing import List, Dict, Tuple
from datetime import datetime
import time
import networkx as nx
from geopy.distance import geodesic
from geopy.geocoders import Nominatim, Photon
import random

# Constantes
ITUIUTABA_LAT = -18.9706
ITUIUTABA_LON = -49.4640

# Endereços predefinidos em Ituiutaba
PONTO_INICIAL = "Rodoviária, 100 - Ituiutaba, MG"
COORDENADAS_CONHECIDAS = {
    PONTO_INICIAL: (ITUIUTABA_LAT - 0.0076, ITUIUTABA_LON + 0.0019)  # Coordenadas da rodoviária
}

class RotaOtimizada:
    """
    Classe para gerenciar cálculos de rotas otimizadas usando OpenRouteService
    """
    def __init__(self, api_key: str = None, cache_file: str = 'coordenadas_cache.txt',
                 api_timeout: int = 20):
        """
        Inicializa a classe de otimização de rotas
        
        Args:
            api_key: Chave da API OpenRouteService (opcional)
            cache_file: Arquivo para cache de coordenadas (opcional)
            api_timeout: Tempo limite para requisições em segundos
        """
        self.api_key = api_key or '5b3ce3597851110001cf6248e4f2b94a65164a3eb706b7dd40f6a544'
        self.base_url = 'https://api.openrouteservice.org/v2/directions/driving-car'
        self.cache_file = cache_file
        self.cache = self._carregar_cache()
        self.grafo = nx.Graph()
        self.timeout = api_timeout
        
        # Inicializa geocodificadores
        self.nominatim = Nominatim(
            user_agent="otimizador_rotas_v1",
            timeout=self.timeout
        )
        self.photon = Photon(
            user_agent="otimizador_rotas_v1",
            timeout=self.timeout
        )

    def _carregar_cache(self) -> Dict:
        """Carrega o cache de coordenadas do arquivo"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _salvar_cache(self):
        """Salva o cache de coordenadas no arquivo"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def _criar_chave_cache(self, origem: Tuple[float, float], destino: Tuple[float, float]) -> str:
        """
        Cria uma chave única para o cache baseada nas coordenadas
        
        Args:
            origem: Tuple (latitude, longitude) do ponto de origem
            destino: Tuple (latitude, longitude) do ponto de destino
        """
        # Ordena os pontos para garantir consistência independente da ordem
        pontos = sorted([f"{origem[0]},{origem[1]}", f"{destino[0]},{destino[1]}"])
        return f"{pontos[0]}-{pontos[1]}"

    def _gerar_coordenada_sintetica(self, endereco: str) -> Tuple[float, float]:
        """
        Gera uma coordenada sintética para um endereço quando a geocodificação falha
        
        Args:
            endereco: Endereço para gerar coordenada
            
        Returns:
            Tuple com (latitude, longitude) gerada
        """
        # Extrai número da rua/avenida
        partes = endereco.split(",")[0].split()
        try:
            num_rua = int(''.join(filter(str.isdigit, partes[1])))
            lat_offset = (num_rua % 30) * 0.0003
            lon_offset = (num_rua % 20) * 0.0005
        except (IndexError, ValueError):
            lat_offset = random.uniform(-0.008, 0.008)
            lon_offset = random.uniform(-0.008, 0.008)
        
        # Adiciona aleatoriedade mantendo padrão de grade
        lat_offset += random.uniform(-0.0005, 0.0005)
        lon_offset += random.uniform(-0.0005, 0.0005)
        
        # Se for avenida, desloca em direção diferente
        if "Avenida" in endereco:
            return ITUIUTABA_LAT + lat_offset, ITUIUTABA_LON - lon_offset
        else:
            return ITUIUTABA_LAT - lat_offset, ITUIUTABA_LON + lon_offset

    def geocodificar_endereco(self, endereco: str, max_tentativas: int = 3) -> Tuple[float, float]:
        """
        Geocodifica um endereço usando múltiplos serviços
        
        Args:
            endereco: Endereço a ser geocodificado
            max_tentativas: Número máximo de tentativas
            
        Returns:
            Tuple com (latitude, longitude)
        """
        for tentativa in range(max_tentativas):
            # Pausa entre tentativas
            if tentativa > 0:
                time.sleep(1 + tentativa)
            
            # Ajusta formato do endereço baseado na tentativa
            if tentativa == 0:
                endereco_busca = f"{endereco}, Ituiutaba, MG"
            elif tentativa == 1:
                partes = endereco.split(" - ")
                endereco_busca = f"{partes[0]}, Ituiutaba, Minas Gerais, Brasil"
            else:
                if "Rua" in endereco or "Avenida" in endereco:
                    via = endereco.split(",")[0]
                    endereco_busca = f"{via}, Centro, Ituiutaba, MG"
                else:
                    endereco_busca = "Centro, Ituiutaba, MG"
            
            print(f"🔍 Tentativa {tentativa + 1} - Buscando: {endereco_busca}")
            
            # Tenta com Nominatim
            try:
                location = self.nominatim.geocode(
                    endereco_busca,
                    exactly_one=True,
                    country_codes="BR",
                    language="pt-BR",
                    timeout=self.timeout,
                    bounded=True,
                    viewbox=((ITUIUTABA_LON - 0.2, ITUIUTABA_LAT - 0.2),
                            (ITUIUTABA_LON + 0.2, ITUIUTABA_LAT + 0.2))
                )
                
                if location:
                    return location.latitude, location.longitude
                    
            except Exception as e:
                print(f"⚠️ Nominatim falhou: {str(e)}")
            
            # Tenta com Photon
            try:
                location = self.photon.geocode(
                    endereco_busca,
                    exactly_one=True,
                    language="pt"
                )
                
                if location:
                    return location.latitude, location.longitude
                    
            except Exception as e:
                print(f"⚠️ Photon falhou: {str(e)}")
        
        # Se todas tentativas falharem, gera coordenada sintética
        print(f"⚠️ Geocodificação falhou. Usando coordenada sintética para: {endereco}")
        return self._gerar_coordenada_sintetica(endereco)

    def calcular_rota(self, origem: Tuple[float, float], destino: Tuple[float, float]) -> Dict:
        """
        Calcula a rota otimizada entre dois pontos
        
        Args:
            origem: Tuple com (latitude, longitude) do ponto de origem
            destino: Tuple com (latitude, longitude) do ponto de destino
            
        Returns:
            Dict com informações da rota incluindo distância, duração e geometria
        """
        chave_cache = self._criar_chave_cache(origem, destino)
        
        # Verifica cache
        if chave_cache in self.cache:
            print("Usando dados do cache")
            return self.cache[chave_cache]

        # Prepara parâmetros da requisição
        coords = f"{origem[1]},{origem[0]}|{destino[1]},{destino[0]}"
        
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        params = {
            'coordinates': coords,
            'profile': 'driving-car',
            'format': 'geojson'
        }

        try:
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            dados_rota = response.json()
            
            # Processa os dados da rota
            rota_processada = {
                'distancia': dados_rota['features'][0]['properties']['segments'][0]['distance'],
                'duracao': dados_rota['features'][0]['properties']['segments'][0]['duration'],
                'geometria': dados_rota['features'][0]['geometry']['coordinates']
            }
            
            # Salva no cache
            self.cache[chave_cache] = rota_processada
            self._salvar_cache()
            
            return rota_processada

        except requests.exceptions.RequestException as e:
            print(f"Erro ao calcular rota: {e}")
            return None

    def calcular_rota_multiplos_pontos(self, pontos: List[Tuple[float, float]]) -> List[Dict]:
        """
        Calcula rotas otimizadas passando por múltiplos pontos
        
        Args:
            pontos: Lista de tuplas (latitude, longitude)
            
        Returns:
            Lista de dicionários com informações das rotas entre os pontos
        """
        if len(pontos) < 2:
            raise ValueError("São necessários pelo menos 2 pontos para calcular uma rota")

        rotas = []
        for i in range(len(pontos) - 1):
            rota = self.calcular_rota(pontos[i], pontos[i + 1])
            if rota:
                rotas.append(rota)
            # Respeita limite de requisições
            time.sleep(1)

        return rotas

    def calcular_estatisticas_rota(self, rotas: List[Dict]) -> Dict:
        """
        Calcula estatísticas gerais das rotas
        
        Args:
            rotas: Lista de dicionários com informações das rotas
            
        Returns:
            Dicionário com estatísticas gerais
        """
        distancia_total = sum(rota['distancia'] for rota in rotas)
        duracao_total = sum(rota['duracao'] for rota in rotas)
        
        return {
            'distancia_total_km': round(distancia_total / 1000, 2),
            'duracao_total_horas': round(duracao_total / 3600, 2),
            'numero_trechos': len(rotas)
        }

# Exemplo de uso
    def otimizar_rota(self, pontos: List[Tuple[float, float]], algoritmo: str = 'a_star', 
                     limite_branch_bound: int = 10) -> Dict:
        """
        Otimiza a rota entre múltiplos pontos usando o algoritmo especificado
        
        Args:
            pontos: Lista de tuplas (latitude, longitude)
            algoritmo: Nome do algoritmo ('a_star', 'dijkstra', 'vizinho_proximo')
            
        Returns:
            Dicionário com informações da rota otimizada
        """
        if len(pontos) < 2:
            raise ValueError("São necessários pelo menos 2 pontos para otimizar uma rota")

        # Cria grafo com todos os pontos
        self.grafo.clear()
        for i, p1 in enumerate(pontos):
            for j, p2 in enumerate(pontos[i+1:], i+1):
                dist = self.calcular_distancia_real(p1, p2)
                self.grafo.add_edge(i, j, weight=dist)

        # Escolhe o algoritmo de otimização
        if algoritmo == 'branch_bound' and len(pontos) <= limite_branch_bound:
            ordem = self._otimizar_branch_bound(pontos)
        elif algoritmo == 'a_star':
            ordem = self._otimizar_a_star(pontos)
        elif algoritmo == 'dijkstra':
            ordem = self._otimizar_dijkstra(pontos)
        else:
            ordem = self._otimizar_vizinho_proximo(pontos)

        # Calcula a rota otimizada
        rotas_otimizadas = []
        for i in range(len(ordem)-1):
            origem = pontos[ordem[i]]
            destino = pontos[ordem[i+1]]
            rota = self.calcular_rota(origem, destino)
            if rota:
                rotas_otimizadas.append(rota)

        return {
            'ordem': ordem,
            'rotas': rotas_otimizadas,
            'estatisticas': self.calcular_estatisticas_rota(rotas_otimizadas)
        }

    def _otimizar_a_star(self, pontos: List[Tuple[float, float]]) -> List[int]:
        """Otimiza rota usando algoritmo A*"""
        inicio = 0
        nao_visitados = set(range(1, len(pontos)))
        caminho = [inicio]
        
        while nao_visitados:
            atual = caminho[-1]
            proximo = min(nao_visitados, 
                         key=lambda x: nx.astar_path_length(self.grafo, atual, x))
            caminho.append(proximo)
            nao_visitados.remove(proximo)
        
        return caminho

    def _otimizar_dijkstra(self, pontos: List[Tuple[float, float]]) -> List[int]:
        """Otimiza rota usando algoritmo de Dijkstra"""
        inicio = 0
        nao_visitados = set(range(1, len(pontos)))
        caminho = [inicio]
        
        while nao_visitados:
            atual = caminho[-1]
            proximo = min(nao_visitados,
                         key=lambda x: nx.dijkstra_path_length(self.grafo, atual, x))
            caminho.append(proximo)
            nao_visitados.remove(proximo)
        
        return caminho

    def _otimizar_vizinho_proximo(self, pontos: List[Tuple[float, float]]) -> List[int]:
        """Otimiza rota usando algoritmo do vizinho mais próximo"""
        inicio = 0
        nao_visitados = set(range(1, len(pontos)))
        caminho = [inicio]
        
        while nao_visitados:
            atual = caminho[-1]
            proximo = min(nao_visitados,
                         key=lambda x: self.grafo[atual][x]['weight'])
            caminho.append(proximo)
            nao_visitados.remove(proximo)
        
        return caminho

    def calcular_distancia_real(self, origem: Tuple[float, float], 
                              destino: Tuple[float, float]) -> float:
        """Calcula a distância real entre dois pontos usando a API ou cache"""
        rota = self.calcular_rota(origem, destino)
        return rota['distancia'] if rota else geodesic(origem, destino).meters

    def carregar_enderecos_cache(self, arquivo_cache: str) -> Dict[str, Tuple[float, float]]:
        """
        Carrega endereços do arquivo de cache existente
        
        Args:
            arquivo_cache: Caminho para o arquivo de cache
            
        Returns:
            Dicionário com endereços e suas coordenadas
        """
        enderecos = {}
        if os.path.exists(arquivo_cache):
            with open(arquivo_cache, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        try:
                            endereco, lat, lon = linha.split('|')
                            enderecos[endereco] = (float(lat), float(lon))
                        except ValueError:
                            print(f"⚠️ Erro ao processar linha do cache: {linha}")
        return enderecos

    def formatar_resultado(self, resultado: Dict, enderecos: Dict[str, Tuple[float, float]] = None) -> str:
        """
        Formata o resultado da otimização em texto amigável
        
        Args:
            resultado: Dicionário com resultado da otimização
            enderecos: Dicionário opcional com mapeamento de coordenadas para endereços
            
        Returns:
            String formatada com o resultado
        """
        saida = []
        saida.append("\n=== 📍 Rota Otimizada ===\n")
        
        # Adiciona pontos na ordem
        for i, idx in enumerate(resultado['ordem']):
            if enderecos:
                # Encontra endereço correspondente às coordenadas
                coord = resultado['rotas'][0]['geometria'][0] if i == 0 else resultado['rotas'][i-1]['geometria'][-1]
                endereco = None
                for end, (lat, lon) in enderecos.items():
                    if abs(lat - coord[1]) < 0.0001 and abs(lon - coord[0]) < 0.0001:
                        endereco = end
                        break
                
                if endereco:
                    saida.append(f"{i+1}. {endereco}")
                else:
                    saida.append(f"{i+1}. Ponto {idx+1}")
            else:
                saida.append(f"{i+1}. Ponto {idx+1}")
        
        # Adiciona estatísticas
        stats = resultado['estatisticas']
        saida.append("\n=== 📊 Estatísticas ===")
        saida.append(f"Distância total: {stats['distancia_total_km']:.2f} km")
        saida.append(f"Duração estimada: {stats['duracao_total_horas']:.2f} horas")
        saida.append(f"Número de trechos: {stats['numero_trechos']}")
        
        return "\n".join(saida)

    def tratar_erro_api(self, erro: requests.exceptions.RequestException) -> str:
        """
        Trata erros da API e retorna mensagem amigável
        
        Args:
            erro: Exceção da requisição
            
        Returns:
            Mensagem de erro formatada
        """
        if isinstance(erro, requests.exceptions.HTTPError):
            if erro.response.status_code == 429:
                return "Limite de requisições atingido. Tente novamente em alguns minutos."
            elif erro.response.status_code == 401:
                return "Erro de autenticação. Verifique sua chave da API."
            else:
                return f"Erro HTTP {erro.response.status_code}: {erro.response.text}"
        elif isinstance(erro, requests.exceptions.ConnectionError):
            return "Erro de conexão. Verifique sua internet."
        elif isinstance(erro, requests.exceptions.Timeout):
            return "Tempo esgotado. Servidor demorou muito para responder."
        else:
            return f"Erro inesperado: {str(erro)}"

    def _otimizar_branch_bound(self, pontos: List[Tuple[float, float]]) -> List[int]:
        """
        Otimiza rota usando algoritmo Branch and Bound
        
        Args:
            pontos: Lista de coordenadas (latitude, longitude)
            
        Returns:
            Lista com ordem dos pontos otimizada
        """
        print("\n🌳 Calculando rota por Branch and Bound...")
        inicio = time.time()
        
        n = len(pontos)
        melhor_custo = float('inf')
        melhor_rota = None
        nos_visitados = 0
        
        def calcular_limite_inferior(rota_atual: List[int], nao_visitados: set) -> float:
            """Calcula limite inferior para poda"""
            if not nao_visitados:
                return 0
                
            # Estimativa otimista: menor aresta conectando cada vértice não visitado
            estimativa = 0
            vertices = list(range(n))
            for v in nao_visitados:
                menor_aresta = min(self.grafo[v][outro]['weight'] 
                                 for outro in vertices if outro != v and 
                                 self.grafo.has_edge(v, outro))
                estimativa += menor_aresta / 2
            
            return estimativa

        def branch_and_bound_rec(custo_atual: float, rota_atual: List[int], 
                               visitados: set):
            """Função recursiva do branch and bound"""
            nonlocal melhor_custo, melhor_rota, nos_visitados
            nos_visitados += 1
            
            if len(visitados) == n:
                if custo_atual < melhor_custo:
                    melhor_custo = custo_atual
                    melhor_rota = rota_atual[:]
                return
                
            # Calcula limite inferior
            nao_visitados = set(range(n)) - visitados
            limite = custo_atual + calcular_limite_inferior(rota_atual, nao_visitados)
            
            if limite >= melhor_custo:
                return  # Poda o ramo
                
            atual = rota_atual[-1]
            for proximo in range(n):
                if proximo not in visitados and self.grafo.has_edge(atual, proximo):
                    novo_custo = custo_atual + self.grafo[atual][proximo]['weight']
                    if novo_custo < melhor_custo:
                        branch_and_bound_rec(novo_custo, rota_atual + [proximo], 
                                          visitados | {proximo})

        # Inicia a recursão
        branch_and_bound_rec(0, [0], {0})
        
        print(f"⏱️ Tempo de execução: {time.time() - inicio:.2f} segundos")
        print(f"🔍 Nós visitados: {nos_visitados}")
        
        return melhor_rota

    def comparar_algoritmos(self, pontos: List[Tuple[float, float]], 
                          enderecos: Dict[str, Tuple[float, float]] = None) -> str:
        """
        Compara resultados de diferentes algoritmos
        
        Args:
            pontos: Lista de coordenadas (latitude, longitude)
            enderecos: Dicionário opcional com mapeamento de endereços
        
        Returns:
            String formatada com comparação
        """
        algoritmos = ['a_star', 'dijkstra', 'vizinho_proximo']
        if len(pontos) <= 10:
            algoritmos.append('branch_bound')
        
        resultados = []
        for alg in algoritmos:
            inicio = time.time()
            resultado = self.otimizar_rota(pontos, alg)
            tempo = time.time() - inicio
            
            resultados.append({
                'algoritmo': alg,
                'distancia': resultado['estatisticas']['distancia_total_km'],
                'duracao': resultado['estatisticas']['duracao_total_horas'],
                'tempo_exec': tempo,
                'ordem': resultado['ordem']
            })
        
        # Organiza resultados
        saida = ["\n=== 🔄 Comparação de Algoritmos ===\n"]
        for res in resultados:
            saida.append(f"Algoritmo: {res['algoritmo'].upper()}")
            saida.append(f"- Distância: {res['distancia']:.2f} km")
            saida.append(f"- Duração: {res['duracao']:.2f} horas")
            saida.append(f"- Tempo de execução: {res['tempo_exec']:.2f} segundos")
            if enderecos:
                ordem = [list(enderecos.keys())[i] for i in res['ordem']]
                saida.append("- Ordem dos pontos:")
                for i, end in enumerate(ordem, 1):
                    saida.append(f"  {i}. {end}")
            saida.append("")
        
        # Identifica melhor resultado
        melhor = min(resultados, key=lambda x: x['distancia'])
        saida.append(f"🏆 Melhor resultado: {melhor['algoritmo'].upper()}")
        saida.append(f"- Distância: {melhor['distancia']:.2f} km")
        saida.append(f"- Economia vs pior caso: {((max(r['distancia'] for r in resultados) - melhor['distancia'])/melhor['distancia']*100):.1f}%")
        
        return "\n".join(saida)

if __name__ == '__main__':
    # Cria instância da classe
    rota_api = RotaOtimizada()
    
    # Exemplo com endereços em Ituiutaba
    enderecos = [
        "Rua 20, 1000 - Centro, Ituiutaba, MG",
        "Avenida 17, 1234 - Centro, Ituiutaba, MG",
        "Rua 24, 789 - Centro, Ituiutaba, MG",
        "Avenida 31, 456 - Centro, Ituiutaba, MG"
    ]
    
    # Exemplo com endereços em Ituiutaba
    enderecos = [
        PONTO_INICIAL,  # Começa da rodoviária
        "Rua 20, 1000 - Centro, Ituiutaba, MG",
        "Avenida 17, 1234 - Centro, Ituiutaba, MG",
        "Rua 24, 789 - Centro, Ituiutaba, MG",
        "Avenida 31, 456 - Centro, Ituiutaba, MG"
    ]
    
    # Geocodifica endereços
    print("\n🌍 Geocodificando endereços...")
    coordenadas = []
    for endereco in enderecos:
        if endereco in COORDENADAS_CONHECIDAS:
            coord = COORDENADAS_CONHECIDAS[endereco]
            print(f"📍 {endereco} -> {coord} (coordenada conhecida)")
        else:
            coord = rota_api.geocodificar_endereco(endereco)
            print(f"📍 {endereco} -> {coord}")
        coordenadas.append(coord)
    
    # Compara diferentes algoritmos
    endereco_map = dict(zip(coordenadas, enderecos))
    print(rota_api.comparar_algoritmos(coordenadas, endereco_map))
