
<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let treinos = $state<any[]>([]);
    let presencas = $state<any[]>([]);
    let carregando = $state(true);
    let erro = $state('');
    let mensagem = $state('');
    let salvandoTreino = $state<number | null>(null);

    function obterToken() {
        return sessionStorage.getItem('access_token');
    }

    async function requisicao(caminho: string, opcoes: RequestInit = {}) {
        const token = obterToken();

        if (!token) {
            goto('/login');
            throw new Error('Entre novamente no sistema.');
        }

        const resposta = await fetch(`${API_URL}${caminho}`, {
            ...opcoes,
            headers: {
                ...(opcoes.body ? { 'Content-Type': 'application/json' } : {}),
                ...opcoes.headers,
                Authorization: `Bearer ${token}`
            }
        });

        if (resposta.status === 401) {
            sessionStorage.removeItem('access_token');
            goto('/login');
            throw new Error('Sua sessão expirou. Entre novamente.');
        }

        if (!resposta.ok) {
            let detalhe = 'Não foi possível realizar a operação.';

            try {
                const dados = await resposta.json();
                detalhe = typeof dados.detail === 'string'
                    ? dados.detail
                    : detalhe;
            } catch {
                // Mantém a mensagem padrão.
            }

            throw new Error(detalhe);
        }

        if (resposta.status === 204) {
            return null;
        }

        const texto = await resposta.text();
        return texto ? JSON.parse(texto) : null;
    }

    async function carregarDados() {
        carregando = true;
        erro = '';

        try {
            const [listaTreinos, listaPresencas] = await Promise.all([
                requisicao('/area-atleta/treinos'),
                requisicao('/presencas/minhas')
            ]);

            treinos = listaTreinos ?? [];
            presencas = listaPresencas ?? [];
        } catch (e) {
            erro = e instanceof Error ? e.message : 'Erro ao carregar as presenças.';
        } finally {
            carregando = false;
        }
    }

    function buscarPresenca(treinoId: number) {
        return presencas.find((item) => item.treino_id === treinoId);
    }

    async function confirmarPresenca(treinoId: number, confirmacao: boolean) {
        salvandoTreino = treinoId;
        mensagem = '';
        erro = '';

        try {
            await requisicao('/presencas/confirmar', {
                method: 'POST',
                body: JSON.stringify({
                    treino_id: treinoId,
                    confirmacao
                })
            });

            mensagem = confirmacao
                ? 'Sua confirmação foi registrada!'
                : 'Sua resposta foi registrada!';

            await carregarDados();
        } catch (e) {
            erro = e instanceof Error ? e.message : 'Não foi possível registrar sua resposta.';
        } finally {
            salvandoTreino = null;
        }
    }

    function formatarData(data: string) {
        return new Date(data).toLocaleString('pt-BR', {
            dateStyle: 'short',
            timeStyle: 'short'
        });
    }

    function textoConfirmacao(valor: boolean | null | undefined) {
        if (valor === true) return 'Vai comparecer';
        if (valor === false) return 'Não vai comparecer';
        return 'Ainda não respondeu';
    }

    function textoPresenca(valor: boolean | null | undefined) {
        if (valor === true) return 'Presença confirmada pela comissão';
        if (valor === false) return 'Ausência registrada pela comissão';
        return 'Presença ainda não registrada';
    }

    onMount(carregarDados);
</script>

<svelte:head>
    <title>Minhas presenças</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">ÁREA DA ATLETA</p>
            <h1>Minhas presenças</h1>
            <p class="descricao">
                Confirme sua participação nos treinos e acompanhe suas presenças.
            </p>
        </div>

        <button class="botao-voltar" onclick={() => goto('/atleta')}>
            Voltar ao painel
        </button>
    </header>

    {#if mensagem}
        <div class="alerta sucesso">{mensagem}</div>
    {/if}

    {#if erro}
        <div class="alerta erro">{erro}</div>
    {/if}

    {#if carregando}
        <p class="mensagem">Carregando suas informações...</p>
    {:else if treinos.length === 0}
        <div class="vazio">
            <h2>Nenhum treino encontrado</h2>
            <p>Quando houver treinos cadastrados para seu elenco, eles aparecerão aqui.</p>
        </div>
    {:else}
        <div class="lista">
            {#each treinos as treino (treino.id)}
                {@const registro = buscarPresenca(treino.id)}

                <article class="cartao">
                    <div class="cabecalho-treino">
                        <div>
                            <span class="rotulo">DATA E HORÁRIO</span>
                            <strong class="data">{formatarData(treino.data)}</strong>
                        </div>

                        <span class="elenco">Elenco {treino.elenco_id}</span>
                    </div>

                    <h2>{treino.local}</h2>
                    <p class="descricao-treino">{treino.descricao}</p>

                    <div class="status">
                        <div>
                            <span class="rotulo">SUA CONFIRMAÇÃO</span>
                            <strong class:positivo={registro?.confirmacao === true}
                                class:negativo={registro?.confirmacao === false}>
                                {textoConfirmacao(registro?.confirmacao)}
                            </strong>
                        </div>

                        <div>
                            <span class="rotulo">PRESENÇA REAL</span>
                            <strong class:positivo={registro?.presente === true}
                                class:negativo={registro?.presente === false}>
                                {textoPresenca(registro?.presente)}
                            </strong>
                        </div>
                    </div>

                    <div class="acoes">
                        <button
                            class="botao-confirmar"
                            disabled={salvandoTreino === treino.id || registro?.confirmacao === true}
                            onclick={() => confirmarPresenca(treino.id, true)}
                        >
                            {salvandoTreino === treino.id ? 'Salvando...' : 'Vou comparecer'}
                        </button>

                        <button
                            class="botao-recusar"
                            disabled={salvandoTreino === treino.id || registro?.confirmacao === false}
                            onclick={() => confirmarPresenca(treino.id, false)}
                        >
                            {salvandoTreino === treino.id ? 'Salvando...' : 'Não vou comparecer'}
                        </button>
                    </div>
                </article>
            {/each}
        </div>
    {/if}

    <p class="observacao">
        Sua confirmação informa à comissão se você pretende comparecer.
        A presença real é registrada posteriormente pela comissão técnica.
    </p>
</div>

<style>
    :global(body) {
        margin: 0;
        background: #f3f5f9;
        font-family: Arial, sans-serif;
        color: #24352e;
    }

    .pagina {
        max-width: 1000px;
        margin: 0 auto;
        padding: 40px 24px;
    }

    .cabecalho {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        margin-bottom: 30px;
    }

    .subtitulo {
        color: #287354;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 1.5px;
    }

    h1 {
        margin: 8px 0;
        color: #173d32;
        font-size: 32px;
    }

    .descricao,
    .mensagem {
        color: #68766f;
    }

    .botao-voltar {
        border: 0;
        border-radius: 8px;
        padding: 12px 18px;
        background: #236b50;
        color: white;
        font-weight: bold;
        cursor: pointer;
    }

    .lista {
        display: flex;
        flex-direction: column;
        gap: 18px;
    }

    .cartao {
        padding: 24px;
        background: white;
        border: 1px solid #e3e9e5;
        border-radius: 12px;
        box-shadow: 0 3px 12px #173d3210;
    }

    .cabecalho-treino {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
    }

    .cabecalho-treino > div {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .rotulo {
        display: block;
        margin-bottom: 7px;
        color: #78847e;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .data {
        color: #236b50;
    }

    .elenco {
        padding: 6px 10px;
        border-radius: 20px;
        background: #e8f2ec;
        color: #236b50;
        font-size: 12px;
        font-weight: bold;
    }

    .cartao h2 {
        margin: 0 0 8px;
        color: #173d32;
    }

    .descricao-treino {
        color: #65736c;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    .status {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin: 22px 0;
        padding: 18px;
        border-radius: 8px;
        background: #f5f7f5;
    }

    .status strong {
        color: #68766f;
        font-size: 14px;
    }

    .status strong.positivo {
        color: #236b50;
    }

    .status strong.negativo {
        color: #b33b3b;
    }

    .acoes {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .acoes button {
        border: 0;
        border-radius: 8px;
        padding: 12px 18px;
        font-weight: bold;
        cursor: pointer;
    }

    .botao-confirmar {
        background: #236b50;
        color: white;
    }

    .botao-recusar {
        background: #f1e8e8;
        color: #9e3434;
    }

    .acoes button:disabled {
        opacity: 0.55;
        cursor: not-allowed;
    }

    .observacao {
        margin-top: 24px;
        color: #68766f;
        font-size: 13px;
        line-height: 1.6;
    }

    .vazio {
        padding: 45px 24px;
        text-align: center;
        background: white;
        border-radius: 12px;
    }

    .vazio h2 {
        color: #173d32;
    }

    .vazio p {
        color: #68766f;
    }

    .alerta {
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 16px;
    }

    .sucesso {
        background: #e5f4e9;
        color: #236b50;
    }

    .erro {
        background: #fdeaea;
        color: #a52c2c;
    }

    @media (max-width: 600px) {
        .cabecalho {
            align-items: flex-start;
            flex-direction: column;
        }

        .status {
            grid-template-columns: 1fr;
        }

        h1 {
            font-size: 27px;
        }
    }
</style>
