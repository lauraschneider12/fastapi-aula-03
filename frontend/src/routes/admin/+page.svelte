
<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    import { UsersRound, Shield, CalendarDays, Dumbbell, Megaphone, ClipboardCheck } from '@lucide/svelte';

    onMount(() => {
        const token = sessionStorage.getItem('access_token');

        if (!token) {
            goto('/login');
        }
    });

    const secoes = [
        {
            titulo: 'Atletas',
            descricao: 'Cadastrar, consultar e gerenciar atletas.',
            icone: UsersRound,
            rota: '/admin/atletas'
        },
        {
            titulo: 'Elencos',
            descricao: 'Consultar e organizar os elencos do clube.',
            icone: Shield,
            rota: '/admin/elencos'
        },
        {
            titulo: 'Agenda de jogos',
            descricao: 'Consultar a agenda e os próximos jogos.',
            icone: CalendarDays,
            rota: '/admin/agenda'
        },
        {
            titulo: 'Treinos',
            descricao: 'Cadastrar e organizar os treinos dos elencos.',
            icone: Dumbbell,
            rota: '/admin/treinos'
        },
        {
            titulo: 'Avisos',
            descricao: 'Publicar e gerenciar comunicados para as atletas.',
            icone: Megaphone,
            rota: '/admin/avisos'
        },
        {
            titulo: 'Presenças',
            descricao: 'Registrar e consultar a presença nos treinos.',
            icone: ClipboardCheck,
            rota: '/admin/presencas'
        }
    ];

    function sair() {
        sessionStorage.removeItem('access_token');
        goto('/login');
    }
</script>

<svelte:head>
    <title>Painel Administrativo | Clube Futsal</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">CLUBE FUTSAL</p>
            <h1>Painel Administrativo</h1>
            <p class="descricao">
                Bem-vindo ao painel de gerenciamento do clube.
            </p>
        </div>

        <button class="botao-sair" onclick={sair}>
            Sair
        </button>
    </header>

    <main>
        <h2>Gerenciamento do clube</h2>

        <div class="grade">
            {#each secoes as secao}
                <article class="cartao">
                    <div class="icone">
                        <secao.icone size={32} strokeWidth={1.8} />
                    </div>

                    <h3>{secao.titulo}</h3>
                    <p>{secao.descricao}</p>

                    <button
                        class="botao-acessar"
                        onclick={() => goto(secao.rota)}
                    >
                        Acessar
                    </button>
                </article>
            {/each}
        </div>
    </main>
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
        margin-bottom: 36px;
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
    }

    .botao-sair,
    .botao-acessar {
        border: none;
        border-radius: 8px;
        padding: 12px 18px;
        cursor: pointer;
        font-weight: bold;
    }

    .botao-sair {
        background: white;
        color: #173d32;
    }

    h2 {
        margin-bottom: 22px;
    }

    .grade {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 22px;
}

@media (max-width: 900px) {
    .grade {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

    .cartao {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 3px 12px #0000000a;
    }

    .icone {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 58px;
        height: 58px;
        border-radius: 12px;
        background: #e8f2ec;
        color: #236b50;
        margin-bottom: 18px;
    }

    .cartao h3 {
        margin-bottom: 10px;
    }

    .cartao p {
        color: #687386;
        min-height: 42px;
        line-height: 1.5;
    }

    .botao-acessar {
        background: #236b50;
        color: white;
        width: 100%;
        margin-top: 12px;
    }

    .botao-acessar:hover {
        background: #194e3a;
    }

   @media (max-width: 600px) {
    .pagina {
        padding: 16px;
    }

    .cabecalho {
        align-items: flex-start;
        flex-direction: column;
    }

    .grade {
        grid-template-columns: 1fr;
    }
}
</style>
