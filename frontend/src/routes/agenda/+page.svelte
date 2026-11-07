
<script lang="ts">
    import { onMount } from 'svelte';
    import { buscarJogosPublicos } from '#lib/api';

    type GolJogo = {
        id_jogador: number;
        nome: string;
        quantidade: number;
    };

    type Jogo = {
        id: number;
        local: string;
        time_adversario: string;
        data: string;
        gol_local: number;
        gol_visitante: number;
        elenco_id: number;
        gols: GolJogo[];
    };

    let jogos: Jogo[] = $state([]);
    let carregando = $state(true);
    let erro = $state('');

    onMount(async () => {
        try {
            jogos = await buscarJogosPublicos();

            jogos.sort(
                (a, b) =>
                    new Date(a.data).getTime() -
                    new Date(b.data).getTime()
            );
        } catch (e) {
            console.error(e);
            erro = 'Não foi possível carregar a agenda. Tente novamente mais tarde.';
        } finally {
            carregando = false;
        }
    });

    function formatarData(data: string) {
        return new Intl.DateTimeFormat('pt-BR', {
            day: '2-digit',
            month: 'long',
            year: 'numeric',
            timeZone: 'America/Sao_Paulo'
        }).format(new Date(data));
    }

    function formatarHorario(data: string) {
        return new Intl.DateTimeFormat('pt-BR', {
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'America/Sao_Paulo'
        }).format(new Date(data));
    }

    let proximosJogos = $derived(
        jogos.filter(jogo => new Date(jogo.data).getTime() >= Date.now())
    );

    let jogosRealizados = $derived(
        jogos.filter(jogo => new Date(jogo.data).getTime() < Date.now())
    );
</script>

<svelte:head>
    <title>Agenda de Jogos | Clube Futsal</title>
    <meta
        name="description"
        content="Confira os próximos jogos, horários, locais e resultados do Clube Futsal."
    />
</svelte:head>

<header class="cabecalho">
    <a href="/" class="logo">CLUBE <span>FUTSAL</span></a>

    <nav aria-label="Navegação principal">
        <a href="/">Início</a>
        <a href="/agenda" class="ativo">Agenda</a>
        <a href="/elencos">Elencos</a>
        <a href="/login" class="botao-login">Área administrativa</a>
    </nav>
</header>

<main>
    <section class="hero">
        <div class="hero-conteudo">
            <span class="etiqueta">ACOMPANHE A TEMPORADA</span>
            <h1>Agenda de <span>jogos</span></h1>
            <p>
                Fique por dentro dos nossos confrontos, acompanhe os resultados
                e venha torcer pelo Clube Futsal.
            </p>
        </div>
    </section>

    <section class="conteudo">
        {#if carregando}
            <p class="mensagem">Carregando agenda...</p>
        {:else if erro}
            <p class="mensagem erro">{erro}</p>
        {:else}
            <section class="secao-jogos">
                <div class="titulo-secao">
                    <div>
                        <span class="etiqueta">NÃO PERCA</span>
                        <h2>Próximos jogos</h2>
                    </div>
                    <span class="contador">{proximosJogos.length} jogos</span>
                </div>

                {#if proximosJogos.length === 0}
                    <p class="mensagem">
                        Não há próximos jogos cadastrados no momento.
                    </p>
                {:else}
                    <div class="lista-jogos">
                        {#each proximosJogos as jogo (jogo.id)}
                            <article class="card-jogo">
                                <div class="data-jogo">
                                    <span class="rotulo">DATA</span>
                                    <strong>{formatarData(jogo.data)}</strong>
                                    <span class="horario">
                                        {formatarHorario(jogo.data)}
                                    </span>
                                </div>

                                <div class="confronto">
                                    <span class="rotulo">PRÓXIMO CONFRONTO</span>
                                    <h3>
                                        Clube Futsal <span>×</span>
                                        {jogo.time_adversario}
                                    </h3>
                                    <p>
                                        <span aria-hidden="true">📍</span>
                                        {jogo.local}
                                    </p>
                                </div>

                                <span class="status">Agendado</span>
                            </article>
                        {/each}
                    </div>
                {/if}
            </section>

            <section class="secao-jogos resultados">
                <div class="titulo-secao">
                    <div>
                        <span class="etiqueta">NOSSA TRAJETÓRIA</span>
                        <h2>Jogos realizados</h2>
                    </div>
                    <span class="contador">{jogosRealizados.length} jogos</span>
                </div>

                {#if jogosRealizados.length === 0}
                    <p class="mensagem">
                        Os resultados dos jogos aparecerão aqui após as partidas.
                    </p>
                {:else}
                    <div class="lista-jogos">
                        {#each [...jogosRealizados].reverse() as jogo (jogo.id)}
                            <article class="card-jogo">
                                <div class="data-jogo">
                                    <span class="rotulo">DATA</span>
                                    <strong>{formatarData(jogo.data)}</strong>
                                    <span class="horario">
                                        {formatarHorario(jogo.data)}
                                    </span>
                                </div>

                                <div class="confronto">
                                    <span class="rotulo">CONFRONTO</span>
                                    <h3>
                                        Clube Futsal <span>×</span>
                                        {jogo.time_adversario}
                                    </h3>
                                    <p>
                                        <span aria-hidden="true">📍</span>
                                        {jogo.local}
                                    </p>
                                </div>

                                <div class="resultado">
                                    <span class="rotulo">PLACAR</span>
                                    <strong>
                                        {jogo.gol_local ?? 0} × {jogo.gol_visitante ?? 0}
                                    </strong>
                                </div>

                                <div class="detalhes-gols">
                                    <span class="rotulo">GOLS DA PARTIDA</span>

                                    {#if jogo.gols && jogo.gols.length > 0}
                                        {#each jogo.gols as gol (gol.id_jogador)}
                                            <div class="gol-item">
                                                <span class="nome-goleadora">
                                                    ⚽ {gol.nome}
                                                </span>

                                                <span class="quantidade-gols">
                                                    {gol.quantidade}
                                                    {gol.quantidade === 1 ? 'gol' : 'gols'}
                                                </span>
                                            </div>
                                        {/each}
                                    {:else}
                                        <p class="sem-gols">
                                            Nenhum gol registrado.
                                        </p>
                                    {/if}
                                </div>
                            </article>
                        {/each}
                    </div>
                {/if}
            </section>
        {/if}
    </section>
</main>

<footer>
    <a href="/" class="logo">CLUBE <span>FUTSAL</span></a>
    <p>Paixão pelo futsal. Orgulho de vestir essa camisa.</p>
    <span>© {new Date().getFullYear()} Clube Futsal</span>
</footer>

<style>
    :global(*) {
        box-sizing: border-box;
    }

    :global(body) {
        margin: 0;
        background: #f4f7fb;
        color: #102039;
        font-family: Arial, Helvetica, sans-serif;
    }

    :global(a) {
        text-decoration: none;
    }

    .cabecalho {
        min-height: 76px;
        padding: 16px 7%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        background: #091426;
        color: white;
    }

    .logo {
        color: white;
        font-size: 1.15rem;
        font-weight: 900;
        letter-spacing: 1px;
        white-space: nowrap;
    }

    .logo span {
        color: #60a5fa;
    }

    nav {
        display: flex;
        align-items: center;
        gap: 26px;
        flex-wrap: wrap;
    }

    nav a {
        color: #c5d0df;
        font-size: 0.9rem;
        transition: color 0.2s;
    }

    nav a:hover,
    nav a.ativo {
        color: #60a5fa;
    }

    nav .botao-login {
        padding: 11px 16px;
        border: 1px solid #3b82f6;
        border-radius: 7px;
        color: white;
    }

    .hero {
        padding: 76px 7% 84px;
        color: white;
        background:
            radial-gradient(ellipse at 85% 30%, #1d4e89 0%, transparent 42%),
            linear-gradient(115deg, #0b172b, #102c50);
    }

    .hero-conteudo {
        max-width: 1100px;
        margin: 0 auto;
    }

    .etiqueta {
        color: #3b82f6;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 2px;
    }

    .hero .etiqueta {
        color: #93c5fd;
    }

    h1 {
        margin: 16px 0;
        font-size: clamp(2.6rem, 6vw, 4.6rem);
        letter-spacing: -2px;
    }

    h1 span {
        color: #60a5fa;
    }

    .hero p {
        max-width: 580px;
        color: #c4d1e2;
        font-size: 1.05rem;
        line-height: 1.8;
    }

    .conteudo {
        width: min(1100px, 86%);
        margin: 0 auto;
        padding: 64px 0 80px;
    }

    .secao-jogos + .secao-jogos {
        margin-top: 64px;
    }

    .titulo-secao {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 16px;
        margin-bottom: 26px;
    }

    h2 {
        margin: 8px 0 0;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        letter-spacing: -1px;
    }

    .contador {
        padding: 8px 12px;
        border-radius: 20px;
        background: #e0ecff;
        color: #1d4ed8;
        font-size: 0.8rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .lista-jogos {
        display: grid;
        gap: 16px;
    }

    .card-jogo {
        display: grid;
        grid-template-columns: minmax(150px, 0.8fr) minmax(220px, 1.7fr) auto;
        align-items: center;
        gap: 26px;
        padding: 26px;
        background: white;
        border: 1px solid #e0e7f0;
        border-radius: 14px;
        box-shadow: 0 5px 18px rgb(15 35 65 / 4%);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .card-jogo:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgb(15 35 65 / 8%);
    }

    .rotulo {
        display: block;
        margin-bottom: 10px;
        color: #8291a7;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .data-jogo strong {
        display: block;
        font-size: 0.94rem;
        line-height: 1.5;
        text-transform: capitalize;
    }

    .horario {
        display: block;
        margin-top: 5px;
        color: #64748b;
        font-size: 0.9rem;
    }

    .confronto h3 {
        margin: 0;
        font-size: 1.1rem;
        line-height: 1.5;
        overflow-wrap: anywhere;
    }

    .confronto h3 span {
        padding: 0 5px;
        color: #2563eb;
    }

    .confronto p {
        margin: 9px 0 0;
        color: #64748b;
        font-size: 0.9rem;
    }

    .status {
        padding: 8px 12px;
        border-radius: 20px;
        background: #e7f8ee;
        color: #187443;
        font-size: 0.78rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .resultado {
        text-align: center;
    }

    .resultado strong {
        display: inline-block;
        color: #1d4ed8;
        font-size: 1.15rem;
    }

    .detalhes-gols {
        grid-column: 1 / -1;
        padding-top: 16px;
        border-top: 1px solid #e0e7f0;
    }

    .gol-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        padding: 8px 0;
        border-bottom: 1px solid #f0f3f8;
    }

    .nome-goleadora {
        color: #102039;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .quantidade-gols {
        color: #1d4ed8;
        font-size: 0.85rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .sem-gols {
        color: #64748b;
        font-size: 0.85rem;
    }

    .mensagem {
        padding: 24px;
        border: 1px solid #e0e7f0;
        border-radius: 12px;
        background: white;
        color: #64748b;
        line-height: 1.6;
    }

    .mensagem.erro {
        border-color: #fecaca;
        color: #b91c1c;
    }

    footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 18px;
        padding: 30px 7%;
        background: #091426;
        color: #aab8cc;
        font-size: 0.85rem;
    }

    footer p {
        margin: 0;
    }

    footer > span {
        color: #7f91aa;
    }

    @media (max-width: 760px) {
        .cabecalho {
            align-items: flex-start;
            flex-direction: column;
            padding: 22px 6%;
        }

        nav {
            gap: 16px;
        }

        .hero {
            padding: 58px 6%;
        }

        .conteudo {
            width: 88%;
            padding: 44px 0 56px;
        }

        .card-jogo {
            grid-template-columns: 1fr;
            gap: 20px;
            padding: 22px;
        }

        .status {
            justify-self: start;
        }

        .resultado {
            text-align: left;
        }

        .detalhes-gols {
            grid-column: 1;
        }

        .titulo-secao {
            align-items: flex-start;
            flex-direction: column;
        }

        footer {
            flex-direction: column;
            align-items: flex-start;
        }
    }
</style>
