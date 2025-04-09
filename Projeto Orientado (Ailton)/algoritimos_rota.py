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

# === ENDEREÇOS ===
ENDERECOS = [
    "Rua 12, 234 - Ituiutaba, MG",
    "Rua 14, 567 - Ituiutaba, MG",
    "Avenida 19, 890 - Ituiutaba, MG",
    "Rua 20, 432 - Ituiutaba, MG",
    "Rua 22, 765 - Ituiutaba, MG",
    "Avenida 25, 109 - Ituiutaba, MG",
    "Rua 26, 543 - Ituiutaba, MG",
    "Rua 28, 876 - Ituiutaba, MG",
    "Avenida 30, 210 - Ituiutaba, MG",
    "Rua 32, 654 - Ituiutaba, MG",
    "Rua 33, 987 - Ituiutaba, MG",
    "Avenida 35, 321 - Ituiutaba, MG",
    "Rua 36, 765 - Ituiutaba, MG",
    "Rua 38, 098 - Ituiutaba, MG",
    "Avenida 40, 432 - Ituiutaba, MG",
    "Rua 42, 876 - Ituiutaba, MG",
    "Rua 43, 109 - Ituiutaba, MG",
    "Avenida 45, 543 - Ituiutaba, MG",
    "Rua 46, 987 - Ituiutaba, MG",
    "Rua 48, 210 - Ituiutaba, MG",
    "Avenida 50, 654 - Ituiutaba, MG",
    "Rua 52, 987 - Ituiutaba, MG",
    "Rua 54, 321 - Ituiutaba, MG",
    "Avenida 55, 765 - Ituiutaba, MG",
    "Rua 56, 098 - Ituiutaba, MG",
    "Rua 58, 432 - Ituiutaba, MG",
    "Avenida 60, 876 - Ituiutaba, MG",
    "Rua 62, 109 - Ituiutaba, MG",
    "Rua 64, 543 - Ituiutaba, MG",
    "Avenida 65, 987 - Ituiutaba, MG",
    "Rua 66, 210 - Ituiutaba, MG",
    "Rua 68, 654 - Ituiutaba, MG",
    "Avenida 70, 987 - Ituiutaba, MG",
    "Rua 72, 321 - Ituiutaba, MG",
    "Rua 74, 765 - Ituiutaba, MG"
]
PONTO_INICIAL = "Rodoviária, 100 - Ituiutaba, MG"

# Coordenadas aproximadas de Ituiutaba, MG
ITUIUTABA_LAT = -18.9706
ITUIUTABA_LON = -49.4640

# Coordenadas pré-definidas para locais conhecidos
COORDENADAS_CONHECIDAS = {
    "Rodoviária, 100 - Ituiutaba, MG": (-18.9782, -49.4621)  # Coordenadas aproximadas da rodoviária
}

# API keys - Substitua por suas chaves reais
OPENCAGE_API_KEY = "SUA_CHAVE_OPENCAGE_AQUI"  # Obtenha em https://opencagedata.com/

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
    # Extrai número da rua/avenida
    partes = endereco.split(",")[0].split()
    try:
        # Tenta extrair o número da rua/avenida (ex: Rua 12 -> 12)
        num_rua = int(''.join(filter(str.isdigit, partes[1])))
        # Calcula deslocamento baseado no número da rua
        lat_offset = (num_rua % 30) * 0.0003
        lon_offset = (num_rua % 20) * 0.0005
    except (IndexError, ValueError):
        # Se não conseguir extrair um número, usa valor aleatório
        lat_offset = random.uniform(-0.008, 0.008)
        lon_offset = random.uniform(-0.008, 0.008)
    
    # Adiciona aleatoriedade mas mantém padrão de grade
    lat_offset += random.uniform(-0.0005, 0.0005)
    lon_offset += random.uniform(-0.0005, 0.0005)
    
    # Se for avenida, desloca em uma direção diferente
    if "Avenida" in endereco:
        return ITUIUTABA_LAT + lat_offset, ITUIUTABA_LON - lon_offset
    else:
        return ITUIUTABA_LAT - lat_offset, ITUIUTABA_LON + lon_offset

def geocodificar_com_opencage(endereco):
    """Geocodifica um endereço usando OpenCage API."""
    try:
        base_url = "https://api.opencagedata.com/geocode/v1/json"
        params = {
            'q': endereco,
            'key': OPENCAGE_API_KEY,
            'language': 'pt-BR',
            'countrycode': 'br',
            'limit': 1,
            # Limitar busca próximo a Ituiutaba
            'bounds': f"{ITUIUTABA_LON-0.2},{ITUIUTABA_LAT-0.2},{ITUIUTABA_LON+0.2},{ITUIUTABA_LAT+0.2}"
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data.get('results'):
            resultado = data['results'][0]
            lat = resultado['geometry']['lat']
            lon = resultado['geometry']['lng']
            return lat, lon
        else:
            print(f"⚠️ OpenCage falhou: {data.get('status', {}).get('message', 'Erro desconhecido')}")
            return None
    except Exception as e:
        print(f"⚠️ Erro no OpenCage: {str(e)}")
        return None

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
    # Verifica se o endereço está nas coordenadas conhecidas
    if endereco in COORDENADAS_CONHECIDAS:
        print(f"📍 Usando coordenada conhecida para: {endereco}")
        return COORDENADAS_CONHECIDAS[endereco]
    
    # Prepara os geocodificadores
    nominatim = Nominatim(
        user_agent="otimizador_roberto_v3",
        timeout=20
    )
    
    photon = Photon(
        user_agent="otimizador_roberto_v3",
        timeout=20
    )
    
    for tentativa in range(max_tentativas):
        # Pausa entre tentativas para evitar limitações de taxa
        time.sleep(1 + tentativa)
        
        # Preparar endereço de busca baseado na tentativa atual
        if tentativa == 0:
            # Primeira tentativa: endereço formatado padrão
            endereco_busca = endereco.replace(" - ", ", ")
        elif tentativa == 1:
            # Segunda tentativa: formato simplificado
            partes = endereco.split(" - ")
            endereco_busca = f"{partes[0]}, Ituiutaba, Minas Gerais, Brasil"
        elif tentativa == 2:
            # Terceira tentativa: apenas o nome da rua/avenida
            rua = endereco.split(",")[0].strip()
            endereco_busca = f"{rua}, Ituiutaba, MG, Brasil"
        elif tentativa == 3:
            # Quarta tentativa: formato ainda mais genérico
            if "Rua" in endereco or "Avenida" in endereco:
                partes = endereco.split(",")[0].split()
                if len(partes) >= 2:
                    via_tipo = partes[0]  # Rua/Avenida
                    via_num = partes[1]   # número da rua
                    endereco_busca = f"{via_tipo} {via_num}, Ituiutaba, Minas Gerais"
                else:
                    endereco_busca = f"Centro, Ituiutaba, MG"
            else:
                endereco_busca = f"Centro, Ituiutaba, MG"
        else:
            # Última tentativa: busca muito genérica
            endereco_busca = "Ituiutaba, Minas Gerais, Brasil"

        print(f"🔍 Tentativa {tentativa + 1} - {endereco_busca}")
        
        # Tenta primeiro com Nominatim
        try:
            print("🔍 Tentando com Nominatim...")
            location = nominatim.geocode(
                endereco_busca,
                exactly_one=True,
                country_codes="BR",
                language="pt-BR",
                timeout=20,
                # Área de busca aproximada
                bounded=True,
                viewbox=((ITUIUTABA_LON - 0.2, ITUIUTABA_LAT - 0.2),
                        (ITUIUTABA_LON + 0.2, ITUIUTABA_LAT + 0.2))
            )
            
            if location:
                print("✅ Nominatim encontrou resultado!")
                return location.latitude, location.longitude
                
        except Exception as e:
            print(f"⚠️ Nominatim falhou: {str(e)}")
        
        # Se Nominatim falhar, tenta com OpenCage
        print("🔍 Tentando com OpenCage...")
        resultado_opencage = geocodificar_com_opencage(endereco_busca)
        if resultado_opencage:
            print("✅ OpenCage encontrou resultado!")
            return resultado_opencage
        
        # Se OpenCage falhar, tenta com Photon
        print("🔍 Tentando com Photon...")
        try:
            location = photon.geocode(
                endereco_busca,
                exactly_one=True,
                language="pt",
                timeout=20
            )
            
            if location:
                print("✅ Photon encontrou resultado!")
                return location.latitude, location.longitude
                
        except Exception as e:
            print(f"⚠️ Photon via geopy falhou: {str(e)}")
        
        # Se geocodificador por geopy falhar, tenta API direta do Photon
        resultado_photon_api = geocodificar_com_photon(endereco_busca)
        if resultado_photon_api:
            print("✅ API Photon encontrou resultado!")
            return resultado_photon_api
    
    # Se todas as tentativas falharam, gera coordenada sintética
    print(f"⚠️ Todos os geocodificadores falharam. Usando coordenada sintética para: {endereco}")
    return gerar_coordenada_sintetica(endereco)

def geocodificar_enderecos():
    """Converte todos os endereços para coordenadas usando múltiplos geocodificadores."""
    print("🌍 Geocodificando endereços...")
    
    # Tenta carregar cache primeiro
    coordenadas = carregar_cache_coordenadas()
    
    # Verifica quais endereços ainda precisam ser geocodificados
    todos_enderecos = [PONTO_INICIAL] + ENDERECOS
    enderecos_faltantes = [e for e in todos_enderecos if e not in coordenadas]
    
    if enderecos_faltantes:
        print(f"🔍 Geocodificando {len(enderecos_faltantes)} endereços faltantes...")
        
        for i, endereco in enumerate(enderecos_faltantes, 1):
            print(f"\n🏃 Processando endereço {i}/{len(enderecos_faltantes)}: {endereco}")
            
            resultado = tentar_geocodificar(endereco)
            coordenadas[endereco] = resultado
            
            # Salva o cache a cada 5 endereços para não perder progresso
            if i % 5 == 0:
                salvar_cache_coordenadas(coordenadas)
        
        # Salva o cache final
        salvar_cache_coordenadas(coordenadas)
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
        for j, destino in enumerate(enderecos):
            if i != j:
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
    """Algoritmo de Dijkstra para encontrar caminhos."""
    print("\n📍 Calculando rota por Dijkstra...")
    start_time = time.time()
    
    caminho = [inicio]
    atual = inicio
    total = 0
    visitados = set([inicio])
    nao_visitados = set(locais)

    while nao_visitados:
        menores = {}
        for destino in nao_visitados:
            try:
                distancia = nx.dijkstra_path_length(grafo, atual, destino, weight='weight')
                menores[destino] = distancia
            except nx.NetworkXNoPath:
                continue
        
        if not menores:
            print("⚠️ Não foi possível encontrar caminhos para todos os pontos.")
            break
            
        proximo = min(menores, key=menores.get)
        caminho.append(proximo)
        total += menores[proximo]
        visitados.add(proximo)
        nao_visitados.remove(proximo)
        atual = proximo

    print(f"⏱️ Tempo de execução: {time.time() - start_time:.2f} segundos")
    return caminho, total

def a_star(grafo: nx.Graph, inicio: str, locais: List[str], coordenadas: Dict) -> Tuple[List[str], float]:
    """Algoritmo A* para encontrar caminhos."""
    print("\n⭐ Calculando rota por A*...")
    start_time = time.time()
    
    def heuristica(a: str, b: str) -> float:
        """Função heurística para A*: distância em linha reta."""
        return distancia_km(a, b, coordenadas)
    
    caminho = [inicio]
    atual = inicio
    total = 0
    visitados = set([inicio])
    nao_visitados = set(locais)

    while nao_visitados:
        menores = {}
        for destino in nao_visitados:
            try:
                distancia = nx.astar_path_length(grafo, atual, destino, 
                                                heuristic=lambda u, v: heuristica(u, v),
                                                weight='weight')
                menores[destino] = distancia
            except nx.NetworkXNoPath:
                continue
        
        if not menores:
            print("⚠️ Não foi possível encontrar caminhos para todos os pontos.")
            break
            
        proximo = min(menores, key=menores.get)
        caminho.append(proximo)
        total += menores[proximo]
        visitados.add(proximo)
        nao_visitados.remove(proximo)
        atual = proximo

    print(f"⏱️ Tempo de execução: {time.time() - start_time:.2f} segundos")
    return caminho, total

def branch_and_bound(inicio: str, locais: List[str], coordenadas: Dict, limite_vertices=10) -> Tuple[List[str], float]:
    """Algoritmo Branch and Bound para o problema do caixeiro viajante."""
    print("\n🌳 Calculando rota por Branch and Bound...")
    start_time = time.time()
    
    # Se o número de locais for grande, usa apenas um subconjunto
    if len(locais) > limite_vertices:
        print(f"⚠️ Número de locais ({len(locais)}) excede o limite para branch and bound ({limite_vertices}).")
        print(f"Usando apenas os primeiros {limite_vertices} locais.")
        locais_subset = locais[:limite_vertices]
    else:
        locais_subset = locais
    
    n = len(locais_subset)
    todos_vertices = [inicio] + locais_subset
    melhor_custo = float('inf')
    melhor_rota = None
    nos_visitados = 0
    
    def calcular_limite_inferior(rota_atual: List[str], nao_visitados: set) -> float:
        """Calcula um limite inferior para o custo restante."""
        if not nao_visitados:
            return 0
            
        # Estimativa otimista: menor aresta conectando cada vértice não visitado
        estimativa = 0
        for v in nao_visitados:
            menor_aresta = min(distancia_km(v, outro, coordenadas) 
                              for outro in todos_vertices if outro != v)
            estimativa += menor_aresta / 2  # Divide por 2 para evitar contar arestas duplicadas
        
        return estimativa

    def branch_and_bound_rec(custo_atual: float, rota_atual: List[str], visitados: set):
        nonlocal melhor_custo, melhor_rota, nos_visitados
        nos_visitados += 1
        
        # Se todos os vértices foram visitados
        if len(visitados) == n + 1:
            if custo_atual < melhor_custo:
                melhor_custo = custo_atual
                melhor_rota = rota_atual[:]
            return
            
        # Calcula limite inferior
        nao_visitados = set(todos_vertices) - visitados
        limite = custo_atual + calcular_limite_inferior(rota_atual, nao_visitados)
        
        if limite >= melhor_custo:
            return  # Poda o ramo
            
        # Tenta cada vértice não visitado como próximo na rota
        atual = rota_atual[-1]
        for proximo in todos_vertices:
            if proximo not in visitados:
                novo_custo = custo_atual + distancia_km(atual, proximo, coordenadas)
                
                # Poda se o custo parcial já excede o melhor
                if novo_custo < melhor_custo:
                    branch_and_bound_rec(novo_custo, rota_atual + [proximo], visitados | {proximo})

    # Inicia a recursão
    branch_and_bound_rec(0, [inicio], {inicio})
    
    # Se usamos um subconjunto, completa a rota usando vizinho mais próximo
    if len(locais_subset) < len(locais):
        print(f"🔄 Completando a rota para os {len(locais) - len(locais_subset)} locais restantes usando vizinho mais próximo...")
        
        locais_restantes = [loc for loc in locais if loc not in locais_subset]
        atual = melhor_rota[-1]
        
        while locais_restantes:
            proximo = min(locais_restantes, key=lambda x: distancia_km(atual, x, coordenadas))
            melhor_rota.append(proximo)
            melhor_custo += distancia_km(atual, proximo, coordenadas)
            locais_restantes.remove(proximo)
            atual = proximo
    
    print(f"⏱️ Tempo de execução: {time.time() - start_time:.2f} segundos (nós visitados: {nos_visitados})")
    return melhor_rota, melhor_custo

def main():
    """Função principal para execução dos algoritmos."""
    print("\n🚀 OTIMIZADOR DE ROTAS - ITUIUTABA, MG")
    print("=" * 50)
    
    try:
        # Converte endereços em coordenadas
        coordenadas = geocodificar_enderecos()
        
        # Gera grafo
        todos_enderecos = [PONTO_INICIAL] + ENDERECOS
        print(f"\n📊 Gerando grafo com {len(todos_enderecos)} pontos...")
        grafo = gerar_grafo(todos_enderecos, coordenadas)
        
        print("\n=== 🚗 Calculando rotas... ===")
        
        # Para melhor performance, limita o número de locais para branch and bound
        limite_bb = 10  # Limite para branch and bound
        
        # Executa algoritmos
        def imprimir_rota(rota: List[str], titulo: str):
            """Função auxiliar para imprimir rota detalhada"""
            print(f"\nRota {titulo}:")
            for i, ponto in enumerate(rota):
                if i == 0:
                    print(f"Início: {ponto}")
                else:
                    print(f"{i}. {ponto}")

        print("\n=== 🔄 Executando Vizinho Mais Próximo ===")
        rota_vmp, dist_vmp = vizinho_mais_proximo(PONTO_INICIAL, ENDERECOS[:], coordenadas)
        print(f"Distância total: {dist_vmp:.2f} km")
        imprimir_rota(rota_vmp, "Vizinho Mais Próximo")

        print("\n=== 📍 Executando Dijkstra ===")
        rota_dij, dist_dij = dijkstra(grafo, PONTO_INICIAL, ENDERECOS[:])
        print(f"Distância total: {dist_dij:.2f} km")
        imprimir_rota(rota_dij, "Dijkstra")

        print("\n=== ⭐ Executando A* ===")
        rota_ast, dist_ast = a_star(grafo, PONTO_INICIAL, ENDERECOS[:], coordenadas)
        print(f"Distância total: {dist_ast:.2f} km")
        imprimir_rota(rota_ast, "A*")

        # Branch and Bound só executa se houver 5 ou menos endereços
        if len(ENDERECOS) <= 5:
            print("\n=== 🌳 Executando Branch and Bound ===")
            rota_bb, dist_bb = branch_and_bound(PONTO_INICIAL, ENDERECOS[:], coordenadas, limite_bb)
            print(f"Distância total: {dist_bb:.2f} km")
            imprimir_rota(rota_bb, "Branch and Bound")
        else:
            print("\n⚠️ Branch and Bound não executado: número de endereços ({}) > 5".format(len(ENDERECOS)))
            rota_bb, dist_bb = None, float('inf')

        # Imprime resultados
        print("\n=== 📊 Resultados ===")
        
        print("\n🔁 Vizinho Mais Próximo:")
        print(f"- {rota_vmp[0]}")
        for i, r in enumerate(rota_vmp[1:], 1):
            print(f"{i}. {r}")
        print(f"Distância total: {dist_vmp:.2f} km\n")

        print("📍 Dijkstra:")
        print(f"- {rota_dij[0]}")
        for i, r in enumerate(rota_dij[1:], 1):
            print(f"{i}. {r}")
        print(f"Distância total: {dist_dij:.2f} km\n")

        print("⭐ A*:")
        print(f"- {rota_ast[0]}")
        for i, r in enumerate(rota_ast[1:], 1):
            print(f"{i}. {r}")
        print(f"Distância total: {dist_ast:.2f} km\n")
        
        if rota_bb is not None:
            print("🌳 Branch and Bound:")
            print(f"- {rota_bb[0]}")
            for i, r in enumerate(rota_bb[1:], 1):
                print(f"{i}. {r}")
            print(f"Distância total: {dist_bb:.2f} km\n")
        else:
            print("🌳 Branch and Bound: Não executado (muitos endereços)\n")
        
        # Compara resultados
        print("=== 📈 Comparação ===")
        # Calcula melhor distância apenas com algoritmos executados
        algoritmos_executados = [dist_vmp, dist_dij, dist_ast]
        if rota_bb is not None:
            algoritmos_executados.append(dist_bb)
        
        melhor_dist = min(algoritmos_executados)
        
        def calc_diferenca(dist):
            return ((dist - melhor_dist) / melhor_dist) * 100 if melhor_dist > 0 else 0
            
        print(f"\nDiferença percentual em relação à melhor solução:")
        print(f"Vizinho Mais Próximo: {calc_diferenca(dist_vmp):.2f}%")
        print(f"Dijkstra: {calc_diferenca(dist_dij):.2f}%")
        print(f"A*: {calc_diferenca(dist_ast):.2f}%")
        print(f"Branch and Bound: {calc_diferenca(dist_bb):.2f}%")
        
        # Identifica o melhor algoritmo
        algoritmos = {
            "Vizinho Mais Próximo": dist_vmp,
            "Dijkstra": dist_dij,
            "A*": dist_ast
        }
        if rota_bb is not None:
            algoritmos["Branch and Bound"] = dist_bb
        melhor_algoritmo = min(algoritmos.items(), key=lambda x: x[1])[0]
        print(f"\n🏆 Melhor algoritmo: {melhor_algoritmo} com distância de {melhor_dist:.2f} km")

    except Exception as e:
        print(f"❌ Erro durante a execução: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
