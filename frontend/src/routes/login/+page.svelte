
<script>
    import { goto } from '$app/navigation';

    let email = '';
    let senha = '';
    let carregando = false;
    let erro = '';

    const API_URL = 'http://localhost:17000';

    async function entrar(event) {
        event.preventDefault();

        erro = '';
        carregando = true;

        try {
            // Dados do formulário
            const dados = new URLSearchParams();

            dados.append('username', email);
            dados.append('password', senha);

            // Realiza o login
            const resposta = await fetch(`${API_URL}/auth/jwt/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: dados
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                throw new Error(
                    resultado.detail || 'E-mail ou senha incorretos.'
                );
            }

            // Salva o token
            sessionStorage.setItem(
                'access_token',
                resultado.access_token
            );

            // Busca os dados do usuário autenticado
            const respostaUsuario = await fetch(`${API_URL}/auth/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${resultado.access_token}`
                }
            });

            if (!respostaUsuario.ok) {
                throw new Error(
                    'Não foi possível identificar seu usuário.'
                );
            }

            const usuario = await respostaUsuario.json();
            console.log('Usuário autenticado:', usuario);
            console.log('Papel recebido:', usuario.role);

            // Redireciona conforme o papel do usuário
            if (usuario.role === 'administrador') {
                await goto('/admin');

            } else if (usuario.role === 'atleta') {
                await goto('/atleta');

            } else {
                throw new Error('Tipo de usuário não reconhecido.');
            }

        } catch (error) {
            console.error('Erro no login:', error);

            sessionStorage.removeItem('access_token');

            erro = error.message || 'Não foi possível entrar no sistema.';

        } finally {
            carregando = false;
        }
    }
</script>

<svelte:head>
    <title>Login | Clube Futsal Feminino</title>
    <meta name="description" content="Acesso à área do clube." />
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <a href="/" class="marca">
            <span class="marca-simbolo">F</span>

            <span>
                <strong>FUTSAL</strong>
                <small>CLUBE FEMININO</small>
            </span>
        </a>

        <a href="/" class="voltar">Voltar ao início</a>
    </header>

    <main class="conteudo">
        <section class="apresentacao">
            <p class="subtitulo">CLUBE FUTSAL FEMININO</p>

            <h1>Força que joga junto.</h1>

            <p>
                Um espaço para organizar, acompanhar e
                gerenciar tudo o que acontece no nosso clube.
            </p>

            <div class="detalhe">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </section>

        <section class="cartao">
            <div class="icone">🔐</div>

            <p class="identificacao">ÁREA RESTRITA</p>

            <h2>Bem-vindo de volta!</h2>

            <p class="descricao">
                Entre com suas credenciais para acessar seu painel.
            </p>

            <form onsubmit={entrar}>
                <label for="email">E-mail</label>

                <input
                    id="email"
                    type="email"
                    placeholder="Digite seu e-mail"
                    bind:value={email}
                    required
                />

                <label for="senha">Senha</label>

                <input
                    id="senha"
                    type="password"
                    placeholder="Digite sua senha"
                    bind:value={senha}
                    required
                />

                {#if erro}
                    <p class="erro">{erro}</p>
                {/if}

                <button type="submit" disabled={carregando}>
                    {carregando ? 'Entrando...' : 'Entrar no sistema'}
                </button>
            </form>

            <p class="aviso">
                Acesso exclusivo para administradores e atletas.
            </p>
        </section>
    </main>

    <footer>
        <p>CLUBE FUTSAL FEMININO</p>
        <span>Força que joga junto.</span>
    </footer>
</div>

<style>
    :global(body) {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #101d35;
        color: #202938;
    }

    :global(*) {
        box-sizing: border-box;
    }

    .pagina {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .cabecalho {
        height: 85px;
        padding: 0 7%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #ffffff20;
    }

    .marca {
        display: flex;
        align-items: center;
        gap: 12px;
        color: white;
        text-decoration: none;
    }

    .marca-simbolo {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        background: #236b50;
        border-radius: 10px;
        font-size: 23px;
        font-weight: bold;
    }

    .marca strong,
    .marca small {
        display: block;
    }

    .marca small {
        font-size: 9px;
        letter-spacing: 2px;
        margin-top: 4px;
        color: #aeb9c9;
    }

    .voltar {
        color: #d5dce8;
        text-decoration: none;
        font-size: 14px;
    }

    .voltar:hover {
        color: white;
    }

    .conteudo {
        flex: 1;
        width: 100%;
        max-width: 1150px;
        margin: auto;
        padding: 65px 25px;
        display: grid;
        grid-template-columns: 1fr 440px;
        align-items: center;
        gap: 70px;
    }

    .apresentacao {
        color: white;
    }

    .subtitulo,
    .identificacao {
        color: #7dc7a5;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 3px;
    }

    .apresentacao h1 {
        max-width: 520px;
        font-size: clamp(42px, 6vw, 65px);
        line-height: 1.1;
        margin: 20px 0;
    }

    .apresentacao > p:last-of-type {
        max-width: 430px;
        color: #c5cfdd;
        line-height: 1.8;
        font-size: 16px;
    }

    .detalhe {
        display: flex;
        gap: 8px;
        margin-top: 35px;
    }

    .detalhe span {
        width: 35px;
        height: 5px;
        background: #236b50;
        border-radius: 5px;
    }

    .detalhe span:nth-child(2) {
        background: #7dc7a5;
    }

    .cartao {
        background: white;
        border-radius: 16px;
        padding: 38px;
        box-shadow: 0 15px 50px #00000025;
    }

    .icone {
        font-size: 27px;
    }

    .identificacao {
        margin-top: 22px;
    }

    .cartao h2 {
        color: #101d35;
        font-size: 27px;
        margin: 10px 0;
    }

    .descricao {
        color: #718096;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 28px;
    }

    form {
        display: flex;
        flex-direction: column;
    }

    label {
        font-size: 13px;
        font-weight: bold;
        margin-bottom: 9px;
        color: #303b4b;
    }

    input {
        width: 100%;
        padding: 14px;
        border: 1px solid #dce2e9;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 14px;
        outline: none;
    }

    input:focus {
        border-color: #236b50;
        box-shadow: 0 0 0 3px #236b5018;
    }

    button {
        border: none;
        border-radius: 8px;
        padding: 15px;
        background: #236b50;
        color: white;
        font-weight: bold;
        cursor: pointer;
        font-size: 14px;
        margin-top: 5px;
    }

    button:hover {
        background: #194e3a;
    }

    button:disabled {
        opacity: 0.65;
        cursor: not-allowed;
    }

    .erro {
        color: #c0392b;
        background: #fdf0ef;
        border-radius: 7px;
        padding: 12px;
        font-size: 13px;
    }

    .aviso {
        color: #8993a2;
        font-size: 11px;
        text-align: center;
        margin-top: 25px;
        line-height: 1.5;
    }

    footer {
        padding: 25px;
        text-align: center;
        color: white;
        border-top: 1px solid #ffffff20;
    }

    footer p {
        font-weight: bold;
        letter-spacing: 2px;
        font-size: 11px;
    }

    footer span {
        color: #aeb9c9;
        font-size: 11px;
    }

    @media (max-width: 800px) {
        .conteudo {
            grid-template-columns: 1fr;
            gap: 35px;
            max-width: 550px;
        }

        .apresentacao h1 {
            font-size: 42px;
        }
    }

    @media (max-width: 480px) {
        .cartao {
            padding: 25px;
        }

        .cabecalho {
            padding: 0 20px;
        }
    }
</style>
