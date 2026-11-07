
const API_URL = 'http://localhost:17000';

export async function buscarJogosPublicos() {
    const resposta = await fetch(`${API_URL}/publico/jogos`);

    if (!resposta.ok) {
        throw new Error('Não foi possível carregar os jogos públicos.');
    }

    return resposta.json();
}

export async function buscarElencosPublicos() {
    const resposta = await fetch(`${API_URL}/publico/elencos`);

    if (!resposta.ok) {
        throw new Error('Não foi possível carregar os elencos.');
    }

    return resposta.json();
}

export async function buscarAtletasPublicos() {
    const resposta = await fetch(`${API_URL}/publico/atletas`);

    if (!resposta.ok) {
        throw new Error('Não foi possível carregar os atletas.');
    }

    return resposta.json();
}
export async function buscarEstatisticasAtleta(atletaId) {
    const resposta = await fetch(
        `${API_URL}/publico/atletas/${atletaId}/estatisticas`
    );

    if (!resposta.ok) {
        throw new Error('Não foi possível carregar as estatísticas da atleta.');
    }

    return resposta.json();
}