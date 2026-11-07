<script>
    import { onMount, tick } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let carregando = $state(true);
    let erro = $state('');
    let estatisticas = $state(null);
    let temporadaSelecionada = $state('');
    let graficoElemento;

    async function carregarGoogleCharts() {
        if (!window.google) {
            await new Promise((resolve, reject) => {
                const script = document.createElement('script');
                script.src = 'https://www.gstatic.com/charts/loader.js';
                script.onload = resolve;
                script.onerror = reject;
                document.head.appendChild(script);
            });
        }

        await new Promise((resolve) => {
            window.google.charts.load('current', { packages: ['corechart'] });
            window.google.charts.setOnLoadCallback(resolve);
        });
    }

    async function requisicao(caminho) {
        const token = sessionStorage.getItem('access_token');

        if (!token) {
            goto('/login');
            throw new Error('Você precisa entrar no sistema novamente.');
        }

        const resposta = await fetch(`${API_URL}${caminho}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (resposta.status === 401) {
            sessionStorage.removeItem('access_token');
            goto('/login');
            throw new Error('Sua sessão expirou. Entre novamente.');
        }

        if (!resposta.ok) {
            const dados = await resposta.json().catch(() => ({}));
            throw new Error(dados.detail || 'Não foi possível carregar o histórico.');
        }

        return resposta.json();
    }

    function obterTemporadaSelecionada() {
        return estatisticas?.temporadas?.find(
            (temporada) => String(temporada.elenco_id) === String(temporadaSelecionada)
        );
    }

    async function desenharGrafico() {
        const temporada = obterTemporadaSelecionada();

        if (!temporada || !graficoElemento || !window.google?.visualization) {
            return;
        }

        const dados = window.google.visualization.arrayToDataTable([
            ['Estatística', 'Quantidade'],
            ['Gols', temporada.gols],
            ['Partidas', temporada.partidas],
            ['Cartões', temporada.cartoes]
        ]);

        const opcoes = {
            title: `Estatísticas da temporada ${temporada.ano}`,
            legend: { position: 'none' },
            height: 350,
            chartArea: { width: '80%', height: '70%' },
            vAxis: {
                minValue: 0,
                format: '0'
            },
            colors: ['#236b50']
        };

        const grafico = new window.google.visualization.ColumnChart(graficoElemento);
        grafico.draw(dados, opcoes);
    }

    async function selecionarTemporada() {
        await tick();
        desenharGrafico();
    }

    onMount(async () => {
        try {
            estatisticas = await requisicao('/area-atleta/estatisticas');

            if (estatisticas.temporadas?.length > 0) {
                temporadaSelecionada = String(estatisticas.temporadas[0].elenco_id);

                await carregarGoogleCharts();
                await tick();
                desenharGrafico();
            }
        } catch (e) {
            erro = e.message;
        } finally {
            carregando = false;
        }
    });
</script>

<svelte:head>
    <title>Meu histórico | Área da atleta</title>
</svelte:head>

<main class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">ÁREA DA ATLETA</p>
            <h1>Meu histórico</h1>
            <p class="descricao">
                Acompanhe suas estatísticas e seu desempenho em cada temporada.
            </p>
        </div>

        <a href="/atleta" class="botao-voltar">Voltar ao painel</a>
    </header>

    {#if carregando}
        <p class="mensagem">Carregando seu histórico...</p>
    {:else if erro}
        <p class="alerta falha">{erro}</p>
    {:else if !estatisticas?.temporadas?.length}
        <section class="cartao vazio">
            <h2>Nenhum histórico encontrado</h2>
            <p>Suas estatísticas aparecerão aqui quando houver dados registrados.</p>
        </section>
    {:else}
        <section class="cartao">
            <h2>Estatísticas por temporada</h2>

            <label for="temporada">Selecione uma temporada:</label>
            <select
                id="temporada"
                bind:value={temporadaSelecionada}
                onchange={selecionarTemporada}
            >
                {#each estatisticas.temporadas as temporada}
                    <option value={String(temporada.elenco_id)}>
                        {temporada.ano}
                    </option>
                {/each}
            </select>
        </section>

        {#if obterTemporadaSelecionada()}
            {@const temporada = obterTemporadaSelecionada()}

            <section class="estatisticas">
                <article class="cartao estatistica">
                    <span>Gols</span>
                    <strong>{temporada.gols}</strong>
                </article>

                <article class="cartao estatistica">
                    <span>Partidas</span>
                    <strong>{temporada.partidas}</strong>
                </article>

                <article class="cartao estatistica">
                    <span>Cartões</span>
                    <strong>{temporada.cartoes}</strong>
                </article>
            </section>

            <section class="cartao">
                <h2>Desempenho na temporada {temporada.ano}</h2>
                <div class="grafico" bind:this={graficoElemento}></div>
            </section>
        {/if}
    {/if}
</main>

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
        margin-bottom: 30px;
    }

    .subtitulo {
        color: #236b50;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    h1 {
        margin: 8px 0;
        color: #173d32;
    }

    .descricao {
        color: #68756e;
    }

    .botao-voltar {
        background: #173d32;
        color: white;
        padding: 12px 18px;
        border-radius: 8px;
        text-decoration: none;
        white-space: nowrap;
    }

    .cartao {
        background: white;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 22px;
        box-shadow: 0 2px 8px #0000000d;
    }

    .cartao h2 {
        margin-top: 0;
        color: #173d32;
    }

    label {
        display: block;
        margin: 15px 0 8px;
        font-weight: bold;
    }

    select {
        width: 100%;
        max-width: 300px;
        padding: 12px;
        border: 1px solid #ccd5cf;
        border-radius: 8px;
        background: white;
    }

    .estatisticas {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }

    .estatistica {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .estatistica span {
        color: #68756e;
    }

    .estatistica strong {
        font-size: 36px;
        color: #236b50;
    }

    .grafico {
        width: 100%;
        min-height: 350px;
    }

    .mensagem,
    .vazio {
        color: #68756e;
    }

    .alerta {
        padding: 15px;
        border-radius: 8px;
    }

    .falha {
        background: #fdeaea;
        color: #a52a2a;
    }

    @media (max-width: 650px) {
        .cabecalho {
            align-items: flex-start;
            flex-direction: column;
        }

        .estatisticas {
            grid-template-columns: 1fr;
            gap: 0;
        }
    }
</style>