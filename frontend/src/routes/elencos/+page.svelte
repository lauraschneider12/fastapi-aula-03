
<script>
    import { onMount } from 'svelte';
    import { buscarElencosPublicos } from '#lib/api';

    let elencos = [];
    let carregando = true;
    let erro = '';

    function normalizarLista(resposta) {
        if (Array.isArray(resposta)) return resposta;

        if (Array.isArray(resposta?.elencos)) return resposta.elencos;
        if (Array.isArray(resposta?.items)) return resposta.items;
        if (Array.isArray(resposta?.data)) return resposta.data;

        return [];
    }

    async function carregarElencos() {
        carregando = true;
        erro = '';

        try {
            const resposta = await buscarElencosPublicos();
            elencos = normalizarLista(resposta);
        } catch (error) {
            console.error('Erro ao carregar elencos:', error);
            erro = 'Não foi possível carregar os elencos. Tente novamente.';
        } finally {
            carregando = false;
        }
    }

    onMount(() => {
        carregarElencos();
    });

    function atletasDoElenco(elenco) {
        return Array.isArray(elenco.atletas) ? elenco.atletas : [];
    }

    function nomePosicao(posicao) {
        if (!posicao) return 'Posição não informada';

        const posicoes = {
            goleira: 'Goleira',
            goleiro: 'Goleira',
            fixa: 'Fixa',
            fixo: 'Fixa',
            ala: 'Ala',
            pivô: 'Pivô',
            pivo: 'Pivô'
        };

        return posicoes[String(posicao).toLowerCase()] || posicao;
    }
</script>

<svelte:head>
    <title>Elencos | Clube Futsal</title>
    <meta
        name="description"
        content="Conheça os elencos e atletas do clube."
    />
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <nav class="navegacao">
            <a href="/" class="logo">CLUBE FUTSAL</a>

            <div class="links">
                <a href="/">Início</a>
                <a href="/agenda">Agenda</a>
                <a href="/elencos" class="ativo">Elencos</a>
                <a href="/login">Área administrativa</a>
            </div>
        </nav>

        <div class="hero">
            <p class="subtitulo">NOSSO TIME</p>
            <h1>Elencos</h1>
            <p>
                Conheça as atletas que representam nosso clube
                dentro das quadras.
            </p>
        </div>
    </header>

    <main class="conteudo">
        <div class="titulo-secao">
            <p class="subtitulo">TEMPORADAS</p>
            <h2>Nossas equipes</h2>
            <p>Confira os elencos e conheça nossas atletas.</p>
        </div>

        {#if carregando}
            <div class="mensagem">
                <div class="loader"></div>
                <p>Carregando elencos...</p>
            </div>

        {:else if erro}
            <div class="mensagem erro">
                <p>{erro}</p>
                <button onclick={carregarElencos}>Tentar novamente</button>
            </div>

        {:else if elencos.length === 0}
            <div class="mensagem">
                <p>Nenhum elenco disponível no momento.</p>
            </div>

        {:else}
            <div class="grade-elencos">
                {#each elencos as elenco (elenco.id)}
                    <section class="elenco">
                        <div class="elenco-cabecalho">
                            <div>
                                <span class="etiqueta">TEMPORADA</span>
                                <h3>{elenco.ano ?? 'Ano não informado'}</h3>
                            </div>

                            <span class="quantidade">
                                {atletasDoElenco(elenco).length}
                                {atletasDoElenco(elenco).length === 1
                                    ? 'atleta'
                                    : 'atletas'}
                            </span>
                        </div>

                        <div class="linha"></div>

                        {#if atletasDoElenco(elenco).length > 0}
                            <div class="grade-atletas">
                                {#each atletasDoElenco(elenco) as atleta (atleta.id)}
                                    <article class="atleta">
                                        <div class="numero">
                                            {atleta.numero ?? '—'}
                                        </div>

                                        <div class="dados-atleta">
                                            <h4>
    <a href={`/atletas/${atleta.id}`}>
        {atleta.nome}
    </a>
</h4>
                                            <p>{nomePosicao(atleta.posicao)}</p>
                                        </div>
                                    </article>
                                {/each}
                            </div>
                        {:else}
                            <p class="sem-atletas">
                                Nenhuma atleta cadastrada neste elenco.
                            </p>
                        {/if}
                    </section>
                {/each}
            </div>
        {/if}
    </main>

    <footer>
        <p>CLUBE FUTSAL</p>
        <span>Força que joga junto.</span>
    </footer>
</div>

<style>
    :global(body) {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f4f5f8;
        color: #202938;
    }

    :global(*) {
        box-sizing: border-box;
    }

    .pagina {
        min-height: 100vh;
    }

    .cabecalho {
        background: #101d35;
        color: white;
        padding: 0 7%;
    }

    .navegacao {
        min-height: 85px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        border-bottom: 1px solid #ffffff20;
    }

    .logo {
        color: white;
        font-weight: bold;
        letter-spacing: 2px;
        text-decoration: none;
    }

    .links {
        display: flex;
        flex-wrap: wrap;
        gap: 25px;
    }

    .links a {
        color: #d5dce8;
        text-decoration: none;
        font-size: 14px;
    }

    .links a:hover,
    .links a.ativo {
        color: white;
        text-decoration: underline;
        text-underline-offset: 7px;
    }

    .hero {
        padding: 75px 0 85px;
        max-width: 750px;
    }

    .subtitulo {
        color: #7dc7a5;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 3px;
    }

    .hero h1 {
        font-size: clamp(42px, 7vw, 68px);
        margin: 12px 0;
    }

    .hero > p:last-child {
        color: #c5cfdd;
        line-height: 1.7;
        font-size: 17px;
    }

    .conteudo {
        max-width: 1150px;
        margin: auto;
        padding: 65px 25px 85px;
    }

    .titulo-secao {
        margin-bottom: 35px;
    }

    .titulo-secao h2 {
        font-size: 32px;
        margin: 10px 0;
        color: #101d35;
    }

    .titulo-secao > p:last-child {
        color: #687386;
    }

    .grade-elencos {
        display: grid;
        gap: 28px;
    }

    .elenco {
        background: white;
        border-radius: 14px;
        padding: 30px;
        box-shadow: 0 4px 20px #101d350c;
    }

    .elenco-cabecalho {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
    }

    .etiqueta {
        color: #26805c;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 2px;
    }

    .elenco-cabecalho h3 {
        color: #101d35;
        font-size: 28px;
        margin: 8px 0 0;
    }

    .quantidade {
        background: #e9f4ee;
        color: #236b50;
        border-radius: 20px;
        padding: 9px 14px;
        font-size: 13px;
        font-weight: bold;
    }

    .linha {
        height: 1px;
        background: #e9edf1;
        margin: 25px 0;
    }

    .grade-atletas {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 15px;
    }

    .atleta {
        display: flex;
        align-items: center;
        gap: 15px;
        background: #f5f7f9;
        padding: 17px;
        border-radius: 10px;
    }

    .numero {
        width: 48px;
        height: 48px;
        flex-shrink: 0;
        display: grid;
        place-items: center;
        background: #173d32;
        color: white;
        border-radius: 9px;
        font-size: 19px;
        font-weight: bold;
    }

    .dados-atleta h4 {
        margin: 0 0 6px;
        color: #202938;
        font-size: 15px;
    }

    .dados-atleta p {
        margin: 0;
        color: #718096;
        font-size: 13px;
    }

    .sem-atletas {
        color: #718096;
    }

    .mensagem {
        background: white;
        border-radius: 12px;
        padding: 35px;
        text-align: center;
        color: #687386;
    }

    .mensagem button {
        background: #236b50;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        cursor: pointer;
    }

    .loader {
        width: 30px;
        height: 30px;
        border: 3px solid #dce8e1;
        border-top-color: #236b50;
        border-radius: 50%;
        animation: girar 0.8s linear infinite;
        margin: 0 auto 15px;
    }

    @keyframes girar {
        to {
            transform: rotate(360deg);
        }
    }

    footer {
        background: #101d35;
        color: white;
        text-align: center;
        padding: 30px;
    }

    footer p {
        font-weight: bold;
        letter-spacing: 2px;
    }

    footer span {
        color: #aeb9c9;
        font-size: 13px;
    }

    @media (max-width: 650px) {
        .cabecalho {
            padding: 0 20px;
        }

        .navegacao {
            align-items: flex-start;
            flex-direction: column;
            padding: 22px 0;
        }

        .links {
            gap: 15px;
        }

        .hero {
            padding: 55px 0;
        }

        .elenco {
            padding: 20px;
        }
    }
</style>
