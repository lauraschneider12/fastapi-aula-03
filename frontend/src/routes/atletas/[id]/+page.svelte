
<script>
    import { onMount, tick } from 'svelte';
    import { page } from '$app/state';

    import {
        buscarEstatisticasAtleta,
        buscarAtletasPublicos
    } from '#lib/api';

    let atleta = $state(null);
    let estatisticas = $state(null);
    let temporadas = $state([]);
    let temporadaSelecionada = $state('');

    let carregando = $state(true);
    let erro = $state('');
    let googleChartsCarregado = $state(false);

    let atletaId = $derived(page.params.id);

    let temporadaAtual = $derived(
        temporadas.find(
            (temporada) =>
                String(temporada.elenco_id) ===
                String(temporadaSelecionada)
        )
    );

    onMount(() => {
        carregarPerfil();
    });

    async function carregarPerfil() {
        carregando = true;
        erro = '';
        googleChartsCarregado = false;

        try {
            const idAtual = atletaId;

            const [dadosEstatisticas, atletas] = await Promise.all([
                buscarEstatisticasAtleta(idAtual),
                buscarAtletasPublicos()
            ]);

            estatisticas = dadosEstatisticas;

            const listaAtletas = Array.isArray(atletas)
                ? atletas
                : atletas?.atletas ?? [];

            atleta = listaAtletas.find(
                (item) => String(item.id) === String(idAtual)
            );

            temporadas = dadosEstatisticas.temporadas ?? [];

            temporadaSelecionada =
                temporadas.length > 0
                    ? String(temporadas[0].elenco_id)
                    : '';

            if (temporadas.length > 0) {
                await carregarGoogleCharts();
            }
        } catch (error) {
            console.error('Erro ao carregar perfil:', error);
            erro = 'Não foi possível carregar o perfil da atleta.';
        } finally {
            carregando = false;
        }
    }

    function carregarGoogleCharts() {
        return new Promise((resolve, reject) => {
            if (window.google?.visualization) {
                googleChartsCarregado = true;
                resolve();
                return;
            }

            const iniciarBiblioteca = () => {
                if (!window.google?.charts) {
                    reject(
                        new Error('Google Charts não foi carregado.')
                    );
                    return;
                }

                window.google.charts.load('current', {
                    packages: ['corechart']
                });

                window.google.charts.setOnLoadCallback(() => {
                    googleChartsCarregado = true;
                    resolve();
                });
            };

            const scriptExistente = document.querySelector(
                'script[src="https://www.gstatic.com/charts/loader.js"]'
            );

            if (scriptExistente) {
                if (window.google?.charts) {
                    iniciarBiblioteca();
                } else {
                    scriptExistente.addEventListener(
                        'load',
                        iniciarBiblioteca,
                        { once: true }
                    );

                    scriptExistente.addEventListener(
                        'error',
                        () => reject(
                            new Error('Falha ao carregar Google Charts.')
                        ),
                        { once: true }
                    );
                }

                return;
            }

            const script = document.createElement('script');

            script.src =
                'https://www.gstatic.com/charts/loader.js';

            script.async = true;
            script.onload = iniciarBiblioteca;

            script.onerror = () => {
                reject(
                    new Error(
                        'Não foi possível carregar Google Charts.'
                    )
                );
            };

            document.head.appendChild(script);
        });
    }

    
$effect(() => {
    const temporada = temporadaAtual;
    const bibliotecaCarregada = googleChartsCarregado;
    const carregamentoFinalizado = !carregando;

    if (
        temporada &&
        bibliotecaCarregada &&
        carregamentoFinalizado
    ) {
        let cancelado = false;

        tick().then(() => {
            if (!cancelado) {
                desenharGrafico(temporada);
            }
        });

        return () => {
            cancelado = true;
        };
    }
});


    function desenharGrafico(temporada) {
        if (!window.google?.visualization || !temporada) {
            return;
        }

        const elemento = document.getElementById(
            'grafico-estatisticas'
        );

        if (!elemento) {
            console.warn('Elemento do gráfico ainda não encontrado.');
            return;
        }

        const dados =
            window.google.visualization.arrayToDataTable([
                ['Estatística', 'Quantidade', { role: 'style' }],
                ['Gols', Number(temporada.gols ?? 0), '#286b50'],
                ['Partidas', Number(temporada.partidas ?? 0), '#3979b9'],
                ['Cartões', Number(temporada.cartoes ?? 0), '#e5a33d']
            ]);

        const opcoes = {
            legend: {
                position: 'none'
            },
            backgroundColor: 'transparent',
            chartArea: {
                width: '75%',
                height: '80%'
            },
            vAxis: {
                minValue: 0,
                format: '0',
                textStyle: {
                    color: '#536174',
                    fontSize: 13
                },
                gridlines: {
                    color: '#edf0f3'
                }
            },
            hAxis: {
                textStyle: {
                    color: '#536174'
                }
            },
            height: 300,
            fontName: 'Arial',
            bar: {
                groupWidth: '55%'
            }
        };

        const grafico =
            new window.google.visualization.ColumnChart(elemento);

        grafico.draw(dados, opcoes);
    }

    function nomePosicao(posicao) {
        if (!posicao) return 'Posição não informada';

        const posicoes = {
            goleira: 'Goleira',
            goleiro: 'Goleira',
            fixa: 'Fixa',
            fixo: 'Fixa',
            ala: 'Ala',
            'pivô': 'Pivô',
            pivo: 'Pivô'
        };

        return posicoes[String(posicao).toLowerCase()] ?? posicao;
    }
</script>

<svelte:head>
    <title>
        {estatisticas?.nome ?? 'Perfil da atleta'} | Clube Futsal
    </title>

    <meta
        name="description"
        content="Perfil e estatísticas da atleta do Clube Futsal."
    />
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <nav class="navegacao">
            <a href="/" class="logo">CLUBE FUTSAL</a>

            <div class="links">
                <a href="/">Início</a>
                <a href="/agenda">Agenda</a>
                <a href="/elencos">Elencos</a>
                <a href="/login">Área administrativa</a>
            </div>
        </nav>

        <div class="hero">
            <a href="/elencos" class="voltar">
                ← Voltar aos elencos
            </a>

            <p class="subtitulo">NOSSO TIME</p>

            <h1>Perfil da atleta</h1>

            <p>
                Acompanhe o desempenho e a trajetória da atleta.
            </p>
        </div>
    </header>

    <main class="conteudo">
        {#if carregando}
            <div class="mensagem">
                <div class="loader"></div>
                <p>Carregando perfil...</p>
            </div>

        {:else if erro}
            <div class="mensagem erro">
                <p>{erro}</p>
                <a href="/elencos">Voltar aos elencos</a>
            </div>

        {:else if estatisticas}
            <section class="perfil">
                <div class="foto">
                    <span>👤</span>
                </div>

                <div class="informacoes">
                    <span class="etiqueta">ATLETA</span>

                    <h2>{estatisticas.nome}</h2>

                    <p>
                        {nomePosicao(atleta?.posicao)}
                        · Camisa {atleta?.numero ?? '—'}
                    </p>
                </div>
            </section>

            <section class="temporada">
                <label for="temporada">
                    Selecionar temporada
                </label>

                <select
                    id="temporada"
                    bind:value={temporadaSelecionada}
                >
                    {#each temporadas as temporada}
                        <option value={String(temporada.elenco_id)}>
                            {temporada.ano}
                        </option>
                    {/each}
                </select>
            </section>

            {#if temporadaAtual}
                <section class="estatisticas">
                    <article class="card-stat gols">
                        <h3>{temporadaAtual.gols ?? 0}</h3>
                        <p>Gols</p>
                    </article>

                    <article class="card-stat partidas">
                        <h3>{temporadaAtual.partidas ?? 0}</h3>
                        <p>Partidas</p>
                    </article>

                    <article class="card-stat cartoes">
                        <h3>{temporadaAtual.cartoes ?? 0}</h3>
                        <p>Cartões</p>
                    </article>
                </section>

                <section class="grafico-card">
                    <div class="grafico-titulo">
                        <span class="etiqueta">DESEMPENHO</span>

                        <h2>Estatísticas da temporada</h2>

                        <p>
                            Comparação de gols, partidas e cartões.
                        </p>
                    </div>

                    {#if googleChartsCarregado}
                        <div id="grafico-estatisticas"></div>
                    {:else}
                        <div class="mensagem-grafico">
                            Carregando gráfico...
                        </div>
                    {/if}
                </section>

            {:else}
                <div class="mensagem">
                    Nenhuma temporada disponível para esta atleta.
                </div>
            {/if}
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

    .links a:hover {
        color: white;
    }

    .hero {
        padding: 65px 0 75px;
    }

    .voltar {
        color: #c5cfdd;
        text-decoration: none;
        font-size: 14px;
    }

    .subtitulo,
    .etiqueta {
        color: #7dc7a5;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 3px;
    }

    .hero h1 {
        font-size: clamp(38px, 6vw, 58px);
        margin: 12px 0;
    }

    .hero > p:last-child {
        color: #c5cfdd;
        line-height: 1.7;
    }

    .conteudo {
        max-width: 1050px;
        margin: auto;
        padding: 55px 25px 80px;
    }

    .perfil {
        display: flex;
        align-items: center;
        gap: 25px;
        background: white;
        padding: 30px;
        border-radius: 14px;
        box-shadow: 0 4px 20px #101d350c;
    }

    .foto {
        width: 105px;
        height: 105px;
        border-radius: 50%;
        background: #e9f1ed;
        display: grid;
        place-items: center;
        flex-shrink: 0;
    }

    .foto span {
        font-size: 48px;
    }

    .informacoes h2 {
        margin: 10px 0;
        color: #101d35;
        font-size: 28px;
    }

    .informacoes p {
        margin: 0;
        color: #718096;
    }

    .temporada {
        margin: 35px 0 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 260px;
    }

    .temporada label {
        font-size: 13px;
        font-weight: bold;
        color: #536174;
    }

    .temporada select {
        padding: 13px;
        border: 1px solid #dce2e8;
        border-radius: 8px;
        background: white;
        color: #202938;
        font-size: 15px;
    }

    .estatisticas {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
    }

    .card-stat {
        background: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 20px #101d350c;
        border-top: 4px solid transparent;
    }

    .card-stat h3 {
        font-size: 34px;
        margin: 12px 0 5px;
    }

    .card-stat p {
        color: #718096;
        margin: 0;
    }

    .card-stat.gols {
        border-top-color: #286b50;
    }

    .card-stat.gols h3 {
        color: #286b50;
    }

    .card-stat.partidas {
        border-top-color: #3979b9;
    }

    .card-stat.partidas h3 {
        color: #3979b9;
    }

    .card-stat.cartoes {
        border-top-color: #e5a33d;
    }

    .card-stat.cartoes h3 {
        color: #e5a33d;
    }

    .grafico-card {
        background: white;
        margin-top: 25px;
        padding: 30px;
        border-radius: 14px;
        box-shadow: 0 4px 20px #101d350c;
    }

    .grafico-titulo h2 {
        color: #101d35;
        margin: 10px 0;
    }

    .grafico-titulo p {
        color: #718096;
        font-size: 14px;
    }

    #grafico-estatisticas {
        width: 100%;
        min-height: 300px;
    }

    .mensagem-grafico {
        min-height: 300px;
        display: grid;
        place-items: center;
        color: #718096;
    }

    .mensagem {
        background: white;
        border-radius: 12px;
        padding: 35px;
        text-align: center;
        color: #687386;
    }

    .mensagem a {
        color: #236b50;
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

        .perfil {
            align-items: flex-start;
            flex-direction: column;
        }

        .estatisticas {
            grid-template-columns: 1fr;
        }

        .grafico-card {
            padding: 18px;
        }
    }
</style>
