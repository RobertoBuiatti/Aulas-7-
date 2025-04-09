const axios = require('axios');
const fs = require('fs').promises;

// Configuração do User-Agent para a API Nominatim
const axiosInstance = axios.create({
    headers: {
        'User-Agent': 'NodeJS-Geocoding-App'
    }
});

// Lê os endereços do arquivo JSON
async function carregarEnderecos() {
    const dados = await fs.readFile('./Endereços.json', 'utf8');
    return JSON.parse(dados);
}
const CACHE_FILE = 'coordenadas_cache.txt';


// Função para carregar o cache existente
async function carregarCache() {
    try {
        const data = await fs.readFile(CACHE_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return {};
    }
}

// Função para salvar o cache
async function salvarCache(cache) {
    await fs.writeFile(CACHE_FILE, JSON.stringify(cache, null, 2));
}

// Função para obter coordenadas de um endereço usando Nominatim
async function obterCoordenadas(endereco) {
    try {
        const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(endereco)}&format=json&limit=1`;
        const response = await axiosInstance.get(url);
        
        if (response.data && response.data.length > 0) {
            return {
                lat: parseFloat(response.data[0].lat),
                lng: parseFloat(response.data[0].lon)
            };
        }
        throw new Error('Endereço não encontrado');
    } catch (error) {
        console.error(`Erro ao obter coordenadas para ${endereco}:`, error.message);
        return null;
    }

    // Aguarda 1 segundo entre as requisições para respeitar os limites da API
    await new Promise(resolve => setTimeout(resolve, 1000));
}

async function main() {
    const cache = await carregarCache();
    const { enderecos, ponto_inicial } = await carregarEnderecos();
    const todosEnderecos = [ponto_inicial, ...enderecos];
    const resultado = [];

    for (const endereco of todosEnderecos) {
        if (cache[endereco]) {
            console.log(`Usando cache para ${endereco}`);
            resultado.push({ endereco, coordenadas: cache[endereco] });
            continue;
        }

        console.log(`Obtendo coordenadas para ${endereco}`);
        const coordenadas = await obterCoordenadas(endereco);
        
        if (coordenadas) {
            cache[endereco] = coordenadas;
            resultado.push({ endereco, coordenadas });
            // Salva o cache a cada nova coordenada obtida
            await salvarCache(cache);
        }

        // Aguarda 1 segundo entre as requisições para respeitar limites da API
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Salva o resultado final em um arquivo JSON
    await fs.writeFile(
        'coordenadas_resultado.json',
        JSON.stringify(resultado, null, 2)
    );
    
    console.log('Processo concluído! Resultados salvos em coordenadas_resultado.json');
}

main().catch(console.error);