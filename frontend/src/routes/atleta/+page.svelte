
<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    const API_URL = 'http://localhost:17000';

    let carregando = $state(true);
    let nomeAtleta = $state('Atleta');

    const secoes = [
        {
            titulo: 'Minha agenda',
            descricao: 'Consulte os próximos treinos e compromissos do elenco.',
            icone: '📅',
            rota: '/atleta/treinos'
        },
        {
            titulo: 'Avisos',
            descricao: 'Confira os comunicados e informações do clube.',
            icone: '📢',
            rota: '/atleta/avisos'
        },
        {
            titulo: 'Presença',
            descricao: 'Confirme sua participação nos próximos treinos.',
            icone: '✅',
            rota: '/atleta/presenca'
        },
        {
            titulo: 'Meu histórico',
            descricao: 'Consulte seu histórico de participação e estatísticas.',
            icone: '📊',
            rota: '/atleta/historico'
        },
        {
            titulo: 'Meu perfil',
            descricao: 'Consulte suas informações pessoais e esportivas.',
            icone: '👤',
            rota: '/atleta/perfil'
        }
    ];

    onMount(async () => {
        const token = sessionStorage.getItem('access_token');

        if (!token) {
            goto('/login');
            return;
        }

        try {
            // Primeiro verifica se o usuário está autenticado
            const resposta = await fetch(`${API_URL}/auth/me`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (!resposta.ok) {
                sessionStorage.removeItem('access_token');
                goto('/login');
                return;
            }

            const usuario = await resposta.json();

            if (usuario.role !== 'atleta') {
                goto('/admin');
                return;
            }

            // Depois busca o nome completo da atleta
            const respostaPerfil = await fetch(
                `${API_URL}/area-atleta/perfil`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            if (respostaPerfil.status === 401) {
                sessionStorage.removeItem('access_token');
                goto('/login');
                return;
            }

            if (respostaPerfil.ok) {
                const dadosPerfil = await respostaPerfil.json();
                nomeAtleta = dadosPerfil.nome || 'Atleta';
            }

        } catch (error) {
            console.error('Erro ao carregar área da atleta:', error);
        } finally {
            carregando = false;
        }
    });

    function sair() {
        sessionStorage.removeItem('access_token');
        goto('/login');
    }
</script>

<svelte:head>
    <title>Área da Atleta | Clube Futsal</title>
</svelte:head>

<div class="pagina">

    <header class="cabecalho">
        <div>
            <p class="subtitulo">CLUBE FUTSAL FEMININO</p>
            <h1>Área da Atleta</h1>

            <p class="descricao">
                Bem-vinda ao seu espaço! Aqui você acompanha suas atividades no clube.
            </p>
        </div>

        <button class="botao-sair" onclick={sair}>
            Sair
        </button>
    </header>

    {#if carregando}
        <p class="carregando">Carregando sua área...</p>
    {:else}

        <main>
            <section class="boas-vindas">
                <div>
                    <span class="saudacao">BEM-VINDA!</span>

                    <h2>Olá, {nomeAtleta}!</h2>

                    <p>
                        Acompanhe sua rotina, fique por dentro dos avisos
                        e não perca seus próximos compromissos.
                    </p>
                </div>
            </section>

            <h2 class="titulo-secoes">Minha área</h2>

            <div class="grade">

                {#each secoes as secao}
                    <article class="cartao">

                        <span class="icone">
                            {secao.icone}
                        </span>

                        <h3>{secao.titulo}</h3>

                        <p>{secao.descricao}</p>

                        <a
                            class="botao-acessar"
                            href={secao.rota}
                        >
                            Acessar
                        </a>

                    </article>
                {/each}

            </div>
        </main>

    {/if}

</div>

<style>
    :global(body) {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f3f5f9;
        color: #202938;
    }

    .pagina {
        min-height: 100vh;
        padding: 36px;
        box-sizing: border-box;
    }

    .cabecalho {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        padding: 28px;
        background: #173d32;
        color: white;
        border-radius: 14px;
        margin-bottom: 30px;
    }

    .subtitulo {
        font-size: 12px;
        letter-spacing: 2px;
        font-weight: bold;
    }

    h1 {
        margin: 8px 0;
        font-size: 30px;
    }

    .descricao {
        color: #d6e5dd;
        line-height: 1.5;
    }

    .botao-sair {
        border: none;
        border-radius: 8px;
        padding: 12px 18px;
        cursor: pointer;
        font-weight: bold;
        background: white;
        color: #173d32;
    }

    .boas-vindas {
        background: white;
        border-radius: 12px;
        padding: 26px;
        margin-bottom: 32px;
        border-left: 5px solid #236b50;
        box-shadow: 0 3px 12px #0000000a;
    }

    .saudacao {
        color: #236b50;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 2px;
    }

    .boas-vindas h2 {
        margin: 10px 0;
        font-size: 24px;
    }

    .boas-vindas p {
        color: #687386;
        line-height: 1.6;
        margin-bottom: 0;
    }

    .titulo-secoes {
        margin-bottom: 22px;
    }

    .grade {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 22px;
    }

    .cartao {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 3px 12px #0000000a;
    }

    .icone {
        font-size: 32px;
    }

    .cartao h3 {
        margin-bottom: 10px;
    }

    .cartao p {
        color: #687386;
        min-height: 63px;
        line-height: 1.5;
    }

    .botao-acessar {
        display: block;
        box-sizing: border-box;
        text-align: center;
        text-decoration: none;
        background: #236b50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 18px;
        cursor: pointer;
        font-weight: bold;
        width: 100%;
        margin-top: 12px;
    }

    .botao-acessar:hover {
        background: #194e3a;
    }

    .carregando {
        text-align: center;
        padding: 40px;
        color: #687386;
    }

    @media (max-width: 600px) {
        .pagina {
            padding: 16px;
        }

        .cabecalho {
            align-items: flex-start;
            flex-direction: column;
        }

        h1 {
            font-size: 25px;
        }
    }
</style>
