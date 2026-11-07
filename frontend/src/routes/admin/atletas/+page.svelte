
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let atletas = [];
    let carregando = true;
    let erro = '';
    let mensagem = '';
    let formularioAberto = false;
    let editandoId = null;
    let salvando = false;

    let formulario = {
        nome: '',
        posicao: '',
        numero: '',
        email: '',
        senha: '',
        status: true
    };

    function obterToken() {
        return sessionStorage.getItem('access_token');
    }

    async function requisicao(caminho, opcoes = {}) {
        const token = obterToken();

        if (!token) {
            goto('/login');
            throw new Error('Sua sessão expirou. Entre novamente.');
        }

        const resposta = await fetch(`${API_URL}${caminho}`, {
            ...opcoes,
            headers: {
                ...(opcoes.body
                    ? { 'Content-Type': 'application/json' }
                    : {}),
                ...opcoes.headers,
                Authorization: `Bearer ${token}`
            }
        });

        if (resposta.status === 401) {
            sessionStorage.removeItem('access_token');
            goto('/login');
            throw new Error('Sessão inválida. Entre novamente.');
        }

        if (!resposta.ok) {
            let detalhe = 'Não foi possível realizar a operação.';

            try {
                const dados = await resposta.json();
                detalhe = dados.detail || detalhe;
            } catch {
                // Mantém a mensagem padrão se a resposta não for JSON.
            }

            throw new Error(
                typeof detalhe === 'string'
                    ? detalhe
                    : 'Verifique os campos preenchidos.'
            );
        }

        if (resposta.status === 204) return null;

        const texto = await resposta.text();
        return texto ? JSON.parse(texto) : null;
    }

    async function carregarAtletas() {
        carregando = true;
        erro = '';

        try {
            atletas = await requisicao('/atletas/');
        } catch (e) {
            erro = e.message || 'Erro ao carregar atletas.';
        } finally {
            carregando = false;
        }
    }

    function novoAtleta() {
        editandoId = null;
        mensagem = '';
        erro = '';

        formulario = {
            nome: '',
            posicao: '',
            numero: '',
            email: '',
            senha: '',
            status: true
        };

        formularioAberto = true;
    }

    function editarAtleta(atleta) {
        editandoId = atleta.id;
        mensagem = '';
        erro = '';

        formulario = {
            nome: atleta.nome,
            posicao: atleta.posicao,
            numero: String(atleta.numero),
            email: '',
            senha: '',
            status: atleta.status
        };

        formularioAberto = true;
    }

    function cancelarFormulario() {
        formularioAberto = false;
        editandoId = null;
        erro = '';
    }

    async function salvarAtleta(evento) {
        evento.preventDefault();

        salvando = true;
        erro = '';
        mensagem = '';

        try {
            const numero = Number(formulario.numero);

            if (
                !formulario.nome.trim() ||
                !formulario.posicao.trim() ||
                !Number.isInteger(numero) ||
                numero < 1 ||
                numero > 99
            ) {
                throw new Error(
                    'Preencha nome, posição e um número entre 1 e 99.'
                );
            }

            let dados;
            let caminho;
            let metodo;

            if (editandoId !== null) {
                dados = {
                    nome: formulario.nome.trim(),
                    posicao: formulario.posicao.trim(),
                    numero,
                    status: formulario.status
                };

                caminho = `/atletas/${editandoId}`;
                metodo = 'PUT';
            } else {
                if (
                    !formulario.email.trim() ||
                    formulario.senha.length < 8
                ) {
                    throw new Error(
                        'Informe um e-mail e uma senha com pelo menos 8 caracteres.'
                    );
                }

                dados = {
                    nome: formulario.nome.trim(),
                    posicao: formulario.posicao.trim(),
                    numero,
                    email: formulario.email.trim(),
                    senha: formulario.senha
                };

                caminho = '/atletas/';
                metodo = 'POST';
            }

            await requisicao(caminho, {
                method: metodo,
                body: JSON.stringify(dados)
            });

            formularioAberto = false;
            editandoId = null;
            mensagem = editandoId === null
                ? 'Atleta salvo com sucesso!'
                : 'Atleta atualizado com sucesso!';

            await carregarAtletas();
        } catch (e) {
            erro = e.message || 'Erro ao salvar atleta.';
        } finally {
            salvando = false;
        }
    }

    async function desativarAtleta(atleta) {
        const confirmar = window.confirm(
            `Deseja desativar o atleta ${atleta.nome}?`
        );

        if (!confirmar) return;

        erro = '';
        mensagem = '';

        try {
            await requisicao(`/atletas/${atleta.id}`, {
                method: 'DELETE'
            });

            mensagem = 'Atleta desativado com sucesso!';
            await carregarAtletas();
        } catch (e) {
            erro = e.message || 'Erro ao desativar atleta.';
        }
    }

    onMount(() => {
        carregarAtletas();
    });
</script>

<svelte:head>
    <title>Atletas | Clube Futsal</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">CLUBE FUTSAL</p>
            <h1>Gerenciamento de atletas</h1>
            <p>Consulte e mantenha os atletas do clube atualizados.</p>
        </div>

        <button class="botao-secundario" onclick={() => goto('/admin')}>
            Voltar ao painel
        </button>
    </header>

    <main>
        <div class="barra-acoes">
            <div>
                <h2>Atletas cadastrados</h2>
                <p>{atletas.length} atleta(s) encontrado(s)</p>
            </div>

            <button class="botao-principal" onclick={novoAtleta}>
                + Novo atleta
            </button>
        </div>

        {#if mensagem}
            <p class="alerta sucesso">{mensagem}</p>
        {/if}

        {#if erro}
            <p class="alerta falha">{erro}</p>
        {/if}

        {#if formularioAberto}
            <section class="formulario-cartao">
                <h2>
                    {editandoId !== null ? 'Editar atleta' : 'Cadastrar atleta'}
                </h2>

                <form onsubmit={salvarAtleta}>
                    <div class="campos">
                        <label>
                            Nome completo
                            <input
                                bind:value={formulario.nome}
                                required
                                minlength="2"
                                maxlength="150"
                            />
                        </label>

                        <label>
                            Posição
                            <select bind:value={formulario.posicao} required>
                                <option value="">Selecione</option>
                                <option value="Goleiro">Goleiro</option>
                                <option value="Fixo">Fixo</option>
                                <option value="Ala">Ala</option>
                                <option value="Pivô">Pivô</option>
                            </select>
                        </label>

                        <label>
                            Número da camisa
                            <input
                                type="number"
                                bind:value={formulario.numero}
                                min="1"
                                max="99"
                                required
                            />
                        </label>

                        {#if editandoId === null}
                            <label>
                                E-mail para acesso
                                <input
                                    type="email"
                                    bind:value={formulario.email}
                                    required
                                />
                            </label>

                            <label>
                                Senha inicial
                                <input
                                    type="password"
                                    bind:value={formulario.senha}
                                    minlength="8"
                                    maxlength="128"
                                    required
                                />
                            </label>
                        {:else}
                            <label class="campo-status">
                                <input
                                    type="checkbox"
                                    bind:checked={formulario.status}
                                />
                                Atleta ativo
                            </label>
                        {/if}
                    </div>

                    <div class="botoes-formulario">
                        <button
                            type="button"
                            class="botao-secundario"
                            onclick={cancelarFormulario}
                            disabled={salvando}
                        >
                            Cancelar
                        </button>

                        <button
                            type="submit"
                            class="botao-principal"
                            disabled={salvando}
                        >
                            {salvando ? 'Salvando...' : 'Salvar atleta'}
                        </button>
                    </div>
                </form>
            </section>
        {/if}

        <section class="tabela-cartao">
            {#if carregando}
                <p class="estado">Carregando atletas...</p>
            {:else if atletas.length === 0}
                <p class="estado">
                    Nenhum atleta encontrado. Você pode cadastrar o primeiro!
                </p>
            {:else}
                <div class="tabela-responsiva">
                    <table>
                        <thead>
                            <tr>
                                <th>Número</th>
                                <th>Nome</th>
                                <th>Posição</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>

                        <tbody>
                            {#each atletas as atleta (atleta.id)}
                                <tr>
                                    <td>#{atleta.numero}</td>
                                    <td>{atleta.nome}</td>
                                    <td>{atleta.posicao}</td>
                                    <td>
                                        <span class:inativo={!atleta.status} class="status">
                                            {atleta.status ? 'Ativo' : 'Inativo'}
                                        </span>
                                    </td>
                                    <td>
                                        <div class="acoes">
                                            <button
                                                class="botao-editar"
                                                onclick={() => editarAtleta(atleta)}
                                            >
                                                Editar
                                            </button>

                                            {#if atleta.status}
                                                <button
                                                    class="botao-excluir"
                                                    onclick={() => desativarAtleta(atleta)}
                                                >
                                                    Desativar
                                                </button>
                                            {/if}
                                        </div>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </section>
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
        padding: 32px;
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
        margin-bottom: 32px;
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

    .cabecalho p:last-child {
        color: #d6e5dd;
    }

    h2 {
        margin-top: 0;
    }

    .barra-acoes {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        margin-bottom: 22px;
    }

    .barra-acoes p {
        color: #687386;
        margin-bottom: 0;
    }

    .botao-principal,
    .botao-secundario,
    .botao-editar,
    .botao-excluir {
        border: none;
        border-radius: 8px;
        padding: 11px 16px;
        font-weight: bold;
        cursor: pointer;
    }

    .botao-principal {
        background: #236b50;
        color: white;
    }

    .botao-principal:hover {
        background: #194e3a;
    }

    .botao-principal:disabled {
        opacity: 0.6;
        cursor: wait;
    }

    .botao-secundario {
        background: white;
        color: #173d32;
    }

    .formulario-cartao,
    .tabela-cartao {
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 3px 12px #0000000a;
    }

    .campos {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 18px;
    }

    label {
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-weight: bold;
        font-size: 14px;
    }

    input:not([type="checkbox"]),
    select {
        width: 100%;
        box-sizing: border-box;
        border: 1px solid #d5dce5;
        border-radius: 8px;
        padding: 12px;
        font: inherit;
        background: white;
    }

    .campo-status {
        flex-direction: row;
        align-items: center;
        align-self: end;
        padding: 12px 0;
    }

    .botoes-formulario {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
        margin-top: 24px;
    }

    .alerta {
        padding: 14px 16px;
        border-radius: 8px;
        margin-bottom: 18px;
    }

    .sucesso {
        background: #dff5e8;
        color: #17623a;
    }

    .falha {
        background: #fde8e8;
        color: #a12727;
    }

    .estado {
        padding: 28px 12px;
        text-align: center;
        color: #687386;
    }

    .tabela-responsiva {
        overflow-x: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }

    th,
    td {
        padding: 15px 12px;
        border-bottom: 1px solid #edf0f4;
        white-space: nowrap;
    }

    th {
        color: #687386;
        font-size: 13px;
    }

    .status {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: #dff5e8;
        color: #17623a;
        font-size: 12px;
        font-weight: bold;
    }

    .status.inativo {
        background: #edf0f4;
        color: #687386;
    }

    .acoes {
        display: flex;
        gap: 8px;
    }

    .botao-editar {
        background: #e5efff;
        color: #2455a5;
    }

    .botao-excluir {
        background: #fde8e8;
        color: #a12727;
    }

    @media (max-width: 650px) {
        .pagina {
            padding: 16px;
        }

        .cabecalho,
        .barra-acoes {
            align-items: flex-start;
            flex-direction: column;
        }

        .botoes-formulario {
            flex-direction: column-reverse;
        }
    }
</style>
