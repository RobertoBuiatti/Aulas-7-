"""Algoritmos para otimização de rotas com múltiplos geocodificadores."""
from geopy.geocoders import Nominatim, Photon
from geopy.distance import geodesic
import networkx as nx
from typing import List, Tuple, Dict
import time
import random
import os
import requests
import json

# Carrega os endereços do arquivo JSON
def carregar_enderecos():
    """Carrega os endereços do arquivo JSON."""
    try:
        caminho = os.path.join('Projeto Orientado (Ailton)', 'Endereços.json')
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados['enderecos'], dados['ponto_inicial']
    except Exception as e:
        print(f"❌ Erro ao carregar endereços: {str(e)}")
        return [], ""

# Carrega os endereços e ponto inicial
ENDERECOS, PONTO_INICIAL = carregar_enderecos()

# Coordenadas aproximadas de Ituiutaba, MG
ITUIUTABA_LAT = -18.9706
ITUIUTABA_LON = -49.4640

# Coordenadas pré-definidas para locais conhecidos
COORDENADAS_CONHECIDAS = {
    "Rodoviária, 100 - Ituiutaba, MG": (-18.9782, -49.4621)  # Coordenadas aproximadas da rodoviária
}

# Configurações de geocodificação
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos entre tentativas
NOMINATIM_TIMEOUT = 30

def salvar_cache_coordenadas(coordenadas, arquivo="coordenadas_cache.txt"):
    """Salva coordenadas geocodificadas em um arquivo de cache."""
    with open(arquivo, "w", encoding="utf-8") as f:
        for endereco, (lat, lon) in coordenadas.items():
            f.write(f"{endereco}|{lat}|{lon}\n")
    print(f"💾 Cache de coordenadas salvo em {arquivo}")

def carregar_cache_coordenadas(arquivo="coordenadas_cache.txt"):
    """Carrega coordenadas geocodificadas de um arquivo de cache."""
    coordenadas = {}
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split("|")
                if len(partes) == 3:
                    endereco, lat, lon = partes
                    coordenadas[endereco] = (float(lat), float(lon))
        print(f"📂 Cache de coordenadas carregado: {len(coordenadas)} endereços")
    return coordenadas

def gerar_coordenada_sintetica(endereco):
    """Gera uma coordenada sintética para um endereço baseado em padrões de ruas."""
    # Extrai número da rua/avenida e numeração da casa
    partes = endereco.split(",")[0].split()
    try:
        # Extrai número da rua (ex: Rua 12 -> 12)
        num_rua = int(''.join(filter(str.isdigit, partes[1])))
        
        # Extrai número da casa
        num_casa = int(''.join(filter(str.isdigit, partes[2])))
        
        # Calcula deslocamentos mais precisos baseados na numeração da rua e casa
        lat_offset = (num_rua / 100) * 0.001  # Deslocamento maior para ruas mais distantes
        lon_offset = (num_casa / 1000) * 0.001  # Deslocamento proporcional ao número da casa
        
        # Ajusta direção do deslocamento baseado em padrões comuns de cidade
        if num_rua % 2 == 0:  # Ruas pares
            lat_offset = abs(lat_offset)
        else:  # Ruas ímpares
            lat_offset = -abs(lat_offset)
            
        if num_casa % 2 == 0:  # Números pares
            lon_offset = abs(lon_offset)
        else:  # Números ímpares
            lon_offset = -abs(lon_offset)
            
    except (IndexError, ValueError):
        # Fallback para caso não consiga extrair os números
        lat_offset = random.uniform(-0.005, 0.005)
        lon_offset = random.uniform(-0.005, 0.005)
    
    # Adiciona pequena variação aleatória para evitar pontos alinhados
    lat_offset += random.uniform(-0.0001, 0.0001)
    lon_offset += random.uniform(-0.0001, 0.0001)
    
    # Ajusta deslocamento baseado no tipo de via
    if "Avenida" in endereco:
        # Avenidas geralmente são maiores e mais espaçadas
        return ITUIUTABA_LAT + (lat_offset * 1.5), ITUIUTABA_LON + (lon_offset * 1.5)
    else:
        # Ruas normais
        return ITUIUTABA_LAT + lat_offset, ITUIUTABA_LON + lon_offset

def geocodificar_com_photon(endereco):
    """Geocodifica um endereço usando Photon API (baseado em OpenStreetMap)."""
    try:
        base_url = "https://photon.komoot.io/api/"
        params = {
            'q': endereco,
            'lang': 'pt',
            'limit': 1,
            # Limitar busca próximo a Ituiutaba
            'lat': ITUIUTABA_LAT,
            'lon': ITUIUTABA_LON
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data.get('features'):
            coordenadas = data['features'][0]['geometry']['coordinates']
            # Photon retorna [lon, lat], então inverte para [lat, lon]
            return coordenadas[1], coordenadas[0]
        else:
            print("⚠️ Photon API falhou")
            return None
    except Exception as e:
        print(f"⚠️ Erro no Photon: {str(e)}")
        return None

def tentar_geocodificar(endereco, max_tentativas=5):
    """Tenta geocodificar um endereço com múltiplos serviços."""
    def validar_coordenadas(lat, lon):
        """Valida se as coordenadas estão dentro de uma área razoável ao redor de Ituiutaba."""
        return -19.5 <= lat <= -18.5 and -50.0 <= lon <= -49.0

    def formatar_endereco(end):
        """Formata o endereço para melhor precisão na busca."""
        end = end.replace(" - ", ", ")
        if "Ituiutaba" not in end:
            end += ", Ituiutaba, MG"
        if "Brasil" not in end:
            end += ", Brasil"
        return end

    # Verifica se o endereço está nas coordenadas conhecidas
    if endereco in COORDENADAS_CONHECIDAS:
        coords = COORDENADAS_CONHECIDAS[endereco]
        if validar_coordenadas(coords[0], coords[1]):
            print(f"📍 Usando coordenada conhecida para: {endereco}")
            return coords
        print("⚠️ Coordenada conhecida inválida, tentando geocodificar...")
    
    # Configura o geocodificador Nominatim
    nominatim = Nominatim(
        user_agent="otimizador_roberto_v3",
        timeout=NOMINATIM_TIMEOUT
    )

    # Configura o geocodificador Photon
    photon = Photon(
        user_agent="otimizador_roberto_v3",
        timeout=NOMINATIM_TIMEOUT
    )
    
    # Formata o endereço para busca
    endereco_formatado = formatar_endereco(endereco)
    
    try:
        for tentativa in range(max_tentativas):
            print(f"🔍 Tentativa {tentativa + 1} de {max_tentativas}...")
            
            # Ajusta o formato do endereço baseado na tentativa
            if tentativa == 1:
                # Remove o número da casa
                partes = endereco_formatado.split(",")
                endereco_busca = ",".join([" ".join(partes[0].split()[0:2])] + partes[1:])
            elif tentativa == 2:
                # Usa apenas rua/avenida e cidade
                endereco_busca = f"{endereco_formatado.split(',')[0]}, Ituiutaba, MG, Brasil"
            else:
                endereco_busca = endereco_formatado

            try:
                # Tenta com Nominatim
                location = nominatim.geocode(
                    endereco_busca,
                    exactly_one=True,
                    country_codes="BR",
                    language="pt-BR",
                    timeout=NOMINATIM_TIMEOUT,
                    bounded=True,
                    viewbox=((ITUIUTABA_LON - 0.1, ITUIUTABA_LAT - 0.1),
                            (ITUIUTABA_LON + 0.1, ITUIUTABA_LAT + 0.1))
                )
                
                if location and validar_coordenadas(location.latitude, location.longitude):
                    print(f"✅ Nominatim encontrou resultado válido!")
                    return location.latitude, location.longitude

                # Se Nominatim falhar, tenta com Photon
                print("🔄 Tentando com Photon...")
                location = photon.geocode(
                    endereco_busca,
                    exactly_one=True,
                    language="pt"
                )
                
                if location and validar_coordenadas(location.latitude, location.longitude):
                    print("✅ Photon encontrou resultado válido!")
                    return location.latitude, location.longitude

                # Se geopy falhar, tenta API direta do Photon
                resultado = geocodificar_com_photon(endereco_busca)
                if resultado and validar_coordenadas(resultado[0], resultado[1]):
                    print("✅ API Photon encontrou resultado válido!")
                    return resultado

            except Exception as e:
                print(f"⚠️ Erro na tentativa {tentativa + 1}: {str(e)}")

            # Espera antes da próxima tentativa
            if tentativa < max_tentativas - 1:
                delay = RETRY_DELAY * (tentativa + 1)
                print(f"😴 Aguardando {delay} segundos antes da próxima tentativa...")
                time.sleep(delay)

    except Exception as e:
        print(f"⚠️ Erro crítico na geocodificação: {str(e)}")

    # Se todas as tentativas falharam, gera coordenada sintética
    print(f"⚠️ Todos os geocodificadores falharam. Usando coordenada sintética para: {endereco}")
    return gerar_coordenada_sintetica(endereco)

def geocodificar_enderecos():
    """Converte todos os endereços para coordenadas usando múltiplos geocodificadores."""
    print("🌍 Geocodificando endereços...")
    
    # Tenta carregar cache primeiro
    coordenadas = carregar_cache_coordenadas()
    
    # Adiciona coordenadas conhecidas ao cache
    for endereco, coord in COORDENADAS_CONHECIDAS.items():
        if endereco not in coordenadas:
            coordenadas[endereco] = coord
            print(f"📍 Adicionado endereço conhecido ao cache: {endereco}")
    
    # Verifica quais endereços ainda precisam ser geocodificados
    todos_enderecos = [PONTO_INICIAL] + ENDERECOS
    enderecos_faltantes = [e for e in todos_enderecos if e not in coordenadas]
    
    if enderecos_faltantes:
        print(f"🔍 Geocodificando {len(enderecos_faltantes)} endereços faltantes...")
        
        falhas = []
        for i, endereco in enumerate(enderecos_faltantes, 1):
            print(f"\n🏃 Processando endereço {i}/{len(enderecos_faltantes)}: {endereco}")
            
            try:
                resultado = tentar_geocodificar(endereco)
                if resultado:
                    coordenadas[endereco] = resultado
                    print(f"✅ Sucesso! Coordenadas: {resultado}")
                else:
                    print(f"⚠️ Não foi possível geocodificar: {endereco}")
                    falhas.append(endereco)
            except Exception as e:
                print(f"❌ Erro ao geocodificar {endereco}: {str(e)}")
                falhas.append(endereco)
            
            # Salva o cache mais frequentemente para não perder progresso
            if i % 3 == 0 or i == len(enderecos_faltantes):
                salvar_cache_coordenadas(coordenadas)
        
        # Relatório final
        if falhas:
            print(f"\n⚠️ {len(falhas)} endereços não puderam ser geocodificados:")
            for endereco in falhas:
                print(f"   - {endereco}")
        else:
            print("\n✅ Todos os endereços foram geocodificados com sucesso!")
            
    else:
        print("✅ Todos os endereços já estão no cache!")
            
    return coordenadas

def distancia_km(a: str, b: str, coordenadas: Dict) -> float:
    """Calcula a distância em km entre dois endereços."""
    return geodesic(coordenadas[a], coordenadas[b]).km

def gerar_grafo(enderecos: List[str], coordenadas: Dict) -> nx.Graph:
    """Gera um grafo com as distâncias entre todos os pontos."""
    G = nx.Graph()
    for i, origem in enumerate(enderecos):
        for j, destino in enumerate(enderecos[i+1:], i+1):
            dist = distancia_km(origem, destino, coordenadas)
            G.add_edge(origem, destino, weight=dist)
    return G

def vizinho_mais_proximo(inicio: str, locais: List[str], coordenadas: Dict) -> Tuple[List[str], float]:
    """Algoritmo do vizinho mais próximo."""
    print("\n🔄 Calculando rota por Vizinho Mais Próximo...")
    start_time = time.time()
    
    nao_visitados = locais[:]
    rota = [inicio]
    atual = inicio
    distancia_total = 0

    while nao_visitados:
        proximo = min(nao_visitados, key=lambda x: distancia_km(atual, x, coordenadas))
        distancia_total += distancia_km(atual, proximo, coordenadas)
        rota.append(proximo)
        nao_visitados.remove(proximo)
        atual = proximo

    print(f"⏱️ Tempo de execução: {time.time() - start_time:.2f} segundos")
    return rota, distancia_total

def dijkstra(grafo: nx.Graph, inicio: str, locais: List[str]) -> Tuple[List[str], float]:
    """
    Algoritmo otimizado de Dijkstra para encontrar o caminho mais curto que conecta um conjunto de pontos.
    
    Args:
        grafo (nx.Graph): Grafo ponderado com os pontos e arestas.
        inicio (str): O ponto de partida.
        locais (List[str]): Lista de pontos que devem ser visitados.
    
    Returns:
        Tuple[List[str], float]: Uma tupla com a lista do caminho percorrido e a distância total.
    """
    print("\n📍 Calculando rota por Dijkstra...")
    start_time = time.time()

    # Inicialização
    caminho = [inicio]
    total = 0
    nao_visitados = set(locais)
    atual = inicio

    while nao_visitados:
        try:
            # Calcula as distâncias de 'atual' para todos os outros nós usando Dijkstra
            distancias, _ = nx.single_source_dijkstra(grafo, atual, weight='weight')

            # Filtra os nós não visitados e verifica o mais próximo
            menores_distancias = {no: distancias[no] for no in nao_visitados if no in distancias}

            if not menores_distancias:
                print("⚠️ Não foi possível encontrar caminhos para todos os pontos.")
                break

            # Escolhe o próximo nó com a menor distância
            proximo = min(menores_distancias, key=menores_distancias.get)

            # Atualiza o caminho, a distância total e o nó atual
            total += menores_distancias[proximo]
            caminho.append(proximo)
            nao_visitados.remove(proximo)
            atual = proximo

        except Exception as e:
            print(f"⚠️ Erro durante o cálculo do caminho: {str(e)}")
            break

    print(f"⏱️ Tempo de execução: {time.time() - start_time:.2f} segundos")
    return caminho, total

def branch_and_bound(inicio: str, locais: List[str], coordenadas: Dict) -> Tuple[List[str], float]:
    """
    Algoritmo Branch and Bound para encontrar o caminho mais curto.
    
    Args:
        inicio (str): O ponto de partida.
        locais (List[str]): Lista de locais a serem visitados.
        coordenadas (Dict): Dicionário com as coordenadas de cada local.
    
    Returns:
        Tuple[List[str], float]: Uma tupla com a lista do caminho e a distância total.
    """
    print("\n🌳 Calculando rota por Branch and Bound...")
    start_time = time.time()

    todos_locais = set(locais)
    melhor_rota = None
    melhor_distancia = float('inf')

    def calcular_limite_inferior(rota_atual: List[str], nao_visitados: set) -> float:
        """Calcula um limite inferior para a distância total da rota."""
        if not nao_visitados:
            return 0
        
        # Soma a menor aresta saindo de cada nó não visitado
        soma = 0
        for local in nao_visitados:
            menor_dist = min(distancia_km(local, outro, coordenadas) 
                           for outro in nao_visitados.union({rota_atual[-1]}) 
                           if outro != local)
            soma += menor_dist
        return soma

    def branch_and_bound_rec(custo_atual: float, rota_atual: List[str], visitados: set):
        """Função recursiva do Branch and Bound."""
        nonlocal melhor_rota, melhor_distancia
        
        # Verifica se todos os pontos foram visitados
        if len(visitados) == len(todos_locais):
            if custo_atual < melhor_distancia:
                melhor_distancia = custo_atual
                melhor_rota = rota_atual[:]
            return
        
        # Poda se o custo atual já é maior que o melhor encontrado
        if custo_atual >= melhor_distancia:
            return
        
        # Calcula limite inferior
        limite = custo_atual + calcular_limite_inferior(rota_atual, todos_locais - visitados)
        if limite >= melhor_distancia:
            return
        
        # Explora os próximos pontos possíveis
        atual = rota_atual[-1]
        for proximo in todos_locais - visitados:
            dist = distancia_km(atual, proximo, coordenadas)
            branch_and_bound_rec(
                custo_atual + dist,
                rota_atual + [proximo],
                visitados | {proximo}
            )

    # Inicia a busca
    branch_and_bound_rec(0, [inicio], {inicio})
    
    if melhor_rota is None:
        print("⚠️ Não foi possível encontrar uma rota válida")
        return [], 0

    print(f"⏱️ Tempo de execução: {time.time() - start_time:.2f} segundos")
    return melhor_rota, melhor_distancia

def main():
    """Função principal que executa e compara os algoritmos."""
    try:
        print("🚀 Iniciando otimização de rotas...")
        
        def imprimir_rota(rota: List[str], titulo: str):
            """Imprime uma rota formatada."""
            print(f"\n=== {titulo} ===")
            for i, endereco in enumerate(rota):
                print(f"{i+1}. {endereco}")

        # Geocodifica todos os endereços
        coordenadas = geocodificar_enderecos()
        
        if not coordenadas:
            print("❌ Não foi possível obter as coordenadas dos endereços")
            return
        
        # Remove o ponto inicial da lista de endereços para evitar duplicação
        locais = [e for e in ENDERECOS if e != PONTO_INICIAL]
        
        # Gera o grafo com as distâncias
        grafo = gerar_grafo([PONTO_INICIAL] + locais, coordenadas)
        
        # Executa os algoritmos
        rota_vmp, dist_vmp = vizinho_mais_proximo(PONTO_INICIAL, locais, coordenadas)
        rota_dij, dist_dij = dijkstra(grafo, PONTO_INICIAL, locais)
        rota_bb, dist_bb = branch_and_bound(PONTO_INICIAL, locais, coordenadas)
        
        # Imprime os resultados
        print("\n🎯 Resultados:")
        print(f"\nVizinho Mais Próximo:")
        imprimir_rota(rota_vmp, "Rota")
        print(f"📏 Distância total: {dist_vmp:.2f} km")
        
        print(f"\nDijkstra:")
        imprimir_rota(rota_dij, "Rota")
        print(f"📏 Distância total: {dist_dij:.2f} km")
        
        print(f"\nBranch and Bound:")
        imprimir_rota(rota_bb, "Rota")
        print(f"📏 Distância total: {dist_bb:.2f} km")
        
        # Compara os resultados
        print("\n📊 Comparação:")
        resultados = [
            ("Vizinho Mais Próximo", dist_vmp),
            ("Dijkstra", dist_dij),
            ("Branch and Bound", dist_bb)
        ]
        melhor = min(resultados, key=lambda x: x[1])
        print(f"🏆 Melhor algoritmo: {melhor[0]} com {melhor[1]:.2f} km")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    main()
