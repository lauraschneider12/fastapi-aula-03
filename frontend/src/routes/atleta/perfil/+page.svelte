<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let carregando = $state(true);
    let erro = $state('');
    let perfil = $state(null);

    async function carregarPerfil() {
        const token = sessionStorage.getItem('access_token');

        if (!token) {
            goto('/login');
            return;
        }

        const resposta = await fetch(`${API_URL}/area-atleta/perfil`, {
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
            const dados = await resposta.json().catch(() => ({}));
            throw new Error(dados.detail || 'Não foi possível carregar seu perfil.');
        }

        perfil = await resposta.json();
    }

    onMount(async () => {
        try {
            await carregarPerfil();
        } catch (e) {
            erro = e.message;
        } finally {
            carregando = false;
        }
    });
</script>

<svelte:head>
    <title>Meu perfil | Área da atleta</title>
</svelte:head>

<main class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">ÁREA DA ATLETA</p>
            <h1>Meu perfil</h1>
            <p class="descricao">
                Consulte seus dados cadastrados no sistema.
            </p>
        </div>

        <a href="/atleta" class="botao-voltar">Voltar ao painel</a>
    </header>

    {#if carregando}
        <p class="mensagem">Carregando seu perfil...</p>
    {:else if erro}
        <p class="alerta falha">{erro}</p>
    {:else if perfil}
        <section class="cartao">
            <div class="identificacao">
                <div class="icone-perfil">
                    {perfil.nome?.charAt(0)?.toUpperCase() || 'A'}
                </div>

                <div>
                    <h2>{perfil.nome}</h2>
                    <p>Atleta cadastrada</p>
                </div>
            </div>

            <div class="dados">
                <div class="campo">
                    <span>Nome completo</span>
                    <strong>{perfil.nome}</strong>
                </div>

                <div class="campo">
                    <span>E-mail</span>
                    <strong>{perfil.email}</strong>
                </div>

                <div class="campo">
                    <span>Posição</span>
                    <strong>{perfil.posicao}</strong>
                </div>

                <div class="campo">
                    <span>Número da camisa</span>
                    <strong>{perfil.numero}</strong>
                </div>
            </div>
        </section>

        <section class="cartao">
            <h2>Meus elencos</h2>

            {#if perfil.elencos?.length}
                <div class="lista-elencos">
                    {#each perfil.elencos as elenco}
                        <article class="elenco">
                            <div>
                                <strong>Temporada {elenco.ano}</strong>
                                <p>Elenco #{elenco.id}</p>
                            </div>

                            <span class="status">Vinculada</span>
                        </article>
                    {/each}
                </div>
            {:else}
                <p class="mensagem">
                    Você ainda não está vinculada a nenhum elenco.
                </p>
            {/if}
        </section>
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
        padding: 28px;
        border-radius: 12px;
        margin-bottom: 22px;
        box-shadow: 0 2px 8px #0000000d;
    }

    .identificacao {
        display: flex;
        align-items: center;
        gap: 18px;
        padding-bottom: 25px;
        border-bottom: 1px solid #e8ece9;
    }

    .icone-perfil {
        width: 65px;
        height: 65px;
        border-radius: 50%;
        background: #dcece3;
        color: #236b50;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
    }

    .identificacao h2 {
        margin: 0 0 6px;
        color: #173d32;
    }

    .identificacao p {
        margin: 0;
        color: #68756e;
    }

    .dados {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 25px;
        padding-top: 25px;
    }

    .campo {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .campo span {
        color: #68756e;
        font-size: 14px;
    }

    .campo strong {
        color: #173d32;
        overflow-wrap: anywhere;
    }

    .cartao h2 {
        color: #173d32;
        margin-top: 0;
    }

    .lista-elencos {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .elenco {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px;
        padding: 18px;
        border: 1px solid #e3eae5;
        border-radius: 8px;
    }

    .elenco strong {
        color: #173d32;
    }

    .elenco p {
        margin: 6px 0 0;
        color: #68756e;
        font-size: 14px;
    }

    .status {
        background: #e2f2e8;
        color: #236b50;
        padding: 7px 12px;
        border-radius: 20px;
        font-size: 13px;
    }

    .mensagem {
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

        .dados {
            grid-template-columns: 1fr;
        }
    }
</style>