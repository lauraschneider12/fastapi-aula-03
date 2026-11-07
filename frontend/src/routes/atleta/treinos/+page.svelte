
<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let treinos = $state<any[]>([]);
    let carregando = $state(true);
    let erro = $state('');

    function obterToken() {
        return sessionStorage.getItem('access_token');
    }

    async function carregarTreinos() {
        carregando = true;
        erro = '';

        const token = obterToken();

        if (!token) {
            goto('/login');
            return;
        }

        try {
            const resposta = await fetch(`${API_URL}/area-atleta/treinos`, {
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
                throw new Error('Não foi possível carregar os treinos.');
            }

            treinos = await resposta.json();
        } catch (e) {
            erro = e instanceof Error ? e.message : 'Erro ao carregar os treinos.';
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

    onMount(carregarTreinos);
</script>

<svelte:head>
    <title>Meus treinos</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">ÁREA DA ATLETA</p>
            <h1>Meus treinos</h1>
            <p class="descricao">
                Confira os próximos treinos do seu elenco.
            </p>
        </div>

        <button class="botao-voltar" onclick={() => goto('/atleta')}>
            Voltar ao painel
        </button>
    </header>

    {#if carregando}
        <p class="mensagem">Carregando treinos...</p>
    {:else if erro}
        <div class="alerta erro">{erro}</div>
        <button class="botao" onclick={carregarTreinos}>Tentar novamente</button>
    {:else if treinos.length === 0}
        <div class="vazio">
            <h2>Nenhum treino encontrado</h2>
            <p>Quando a comissão cadastrar novos treinos para seu elenco, eles aparecerão aqui.</p>
        </div>
    {:else}
        <p class="quantidade">
            {treinos.length} {treinos.length === 1 ? 'treino encontrado' : 'treinos encontrados'}
        </p>

        <div class="lista">
            {#each treinos as treino (treino.id)}
                <article class="cartao">
                    <div class="data">
                        <span>DATA E HORÁRIO</span>
                        <strong>{formatarData(treino.data)}</strong>
                    </div>

                    <h2>{treino.local}</h2>
                    <p>{treino.descricao}</p>

                    <span class="elenco">Elenco {treino.elenco_id}</span>
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
        max-width: 1100px;
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

    .descricao {
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
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 18px;
    }

    .cartao {
        background: white;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e3e9e5;
        box-shadow: 0 3px 12px #173d3210;
    }

    .data {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 20px;
    }

    .data span {
        color: #718078;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .data strong {
        color: #236b50;
    }

    .cartao h2 {
        margin: 0 0 10px;
        color: #173d32;
        font-size: 21px;
    }

    .cartao p {
        color: #65736c;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    .elenco {
        display: inline-block;
        margin-top: 10px;
        padding: 6px 10px;
        border-radius: 20px;
        background: #e8f2ec;
        color: #236b50;
        font-size: 12px;
        font-weight: bold;
    }

    .mensagem {
        color: #68766f;
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
