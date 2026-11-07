
<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let avisos = $state<any[]>([]);
    let carregando = $state(true);
    let erro = $state('');

    function obterToken() {
        return sessionStorage.getItem('access_token');
    }

    async function carregarAvisos() {
        carregando = true;
        erro = '';

        const token = obterToken();

        if (!token) {
            goto('/login');
            return;
        }

        try {
            const resposta = await fetch(`${API_URL}/area-atleta/avisos`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (resposta.status === 401) {
                sessionStorage.removeItem('access_token');
                goto('/login');
                return;
            }

            if (!resposta.ok) {
                throw new Error('Não foi possível carregar os avisos.');
            }

            avisos = await resposta.json();
        } catch (e) {
            erro = e instanceof Error ? e.message : 'Erro ao carregar os avisos.';
        } finally {
            carregando = false;
        }
    }

    function formatarData(data: string) {
        return new Date(data).toLocaleString('pt-BR', {
            dateStyle: 'short',
            timeStyle: 'short'
        });
    }

    onMount(carregarAvisos);
</script>

<svelte:head>
    <title>Meus avisos</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">ÁREA DA ATLETA</p>
            <h1>Avisos e comunicados</h1>
            <p class="descricao">
                Fique por dentro dos comunicados da comissão.
            </p>
        </div>

        <button class="botao-voltar" onclick={() => goto('/atleta')}>
            Voltar ao painel
        </button>
    </header>

    {#if carregando}
        <p class="mensagem">Carregando avisos...</p>
    {:else if erro}
        <div class="alerta erro">{erro}</div>
        <button class="botao" onclick={carregarAvisos}>Tentar novamente</button>
    {:else if avisos.length === 0}
        <div class="vazio">
            <h2>Nenhum aviso publicado</h2>
            <p>Quando a comissão publicar um comunicado, ele aparecerá aqui.</p>
        </div>
    {:else}
        <p class="quantidade">
            {avisos.length} {avisos.length === 1 ? 'aviso publicado' : 'avisos publicados'}
        </p>

        <div class="lista">
            {#each avisos as aviso (aviso.id)}
                <article class="cartao">
                    <div class="topo-cartao">
                        <span class="categoria">
                            {aviso.elenco_id === null ? 'AVISO GERAL' : `ELENCO ${aviso.elenco_id}`}
                        </span>
                        <span class="data">{formatarData(aviso.data_publicacao)}</span>
                    </div>

                    <h2>{aviso.titulo}</h2>
                    <p class="conteudo">{aviso.conteudo}</p>
                </article>
            {/each}
        </div>
    {/if}
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
        margin-bottom: 32px;
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

    .botao-voltar,
    .botao {
        border: 0;
        border-radius: 8px;
        padding: 12px 18px;
        background: #236b50;
        color: white;
        font-weight: bold;
        cursor: pointer;
    }

    .botao-voltar:hover,
    .botao:hover {
        background: #174c38;
    }

    .quantidade {
        color: #68766f;
        margin-bottom: 18px;
    }

    .lista {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .cartao {
        padding: 24px;
        background: white;
        border: 1px solid #e3e9e5;
        border-left: 5px solid #236b50;
        border-radius: 10px;
        box-shadow: 0 3px 12px #173d3210;
    }

    .topo-cartao {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 18px;
    }

    .categoria {
        padding: 6px 10px;
        border-radius: 20px;
        background: #e8f2ec;
        color: #236b50;
        font-size: 11px;
        font-weight: bold;
    }

    .data {
        color: #78847e;
        font-size: 12px;
    }

    .cartao h2 {
        margin: 0 0 12px;
        color: #173d32;
        font-size: 21px;
    }

    .conteudo {
        color: #596a61;
        line-height: 1.7;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
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

    .erro {
        background: #fdeaea;
        color: #a52c2c;
    }

    @media (max-width: 600px) {
        .cabecalho {
            align-items: flex-start;
            flex-direction: column;
        }

        h1 {
            font-size: 27px;
        }
    }
</style>
