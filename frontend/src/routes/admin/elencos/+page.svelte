
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    // Estados reativos do Svelte 5
    let elencos = $state([]);
    let atletas = $state([]);
    let atletasDoElenco = $state([]);
    let elencoSelecionado = $state(null);
    let atletaSelecionadoId = $state('');

    let carregando = $state(true);
    let carregandoAtletas = $state(false);
    let salvando = $state(false);
    let erro = $state('');
    let mensagem = $state('');

    let formularioAberto = $state(false);
    let editandoId = $state(null);

    let formulario = $state({
        ano: new Date().getFullYear(),
        status: true
    });

    // Atletas ativos que ainda não pertencem ao elenco selecionado
    let atletasDisponiveis = $derived(
        atletas.filter(
            (atleta) =>
                atleta.status &&
                !atletasDoElenco.some(
                    (item) => item.id === atleta.id
                )
        )
    );

    function obterToken() {
        return sessionStorage.getItem('access_token');
    }

    async function requisicao(caminho, opcoes = {}) {
        const token = obterToken();

        if (!token) {
            goto('/login');
            throw new Error('Entre novamente no sistema.');
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
                // Mantém a mensagem padrão.
            }

            throw new Error(
                typeof detalhe === 'string'
                    ? detalhe
                    : 'Verifique os dados informados.'
            );
        }

        if (resposta.status === 204) return null;

        const texto = await resposta.text();
        return texto ? JSON.parse(texto) : null;
    }

    async function carregarElencos() {
        carregando = true;
        erro = '';

        try {
            elencos = await requisicao('/elencos/');
        } catch (e) {
            erro = e.message || 'Erro ao carregar elencos.';
        } finally {
            carregando = false;
        }
    }

    async function carregarAtletasDisponiveis() {
        try {
            atletas = await requisicao('/atletas/');
        } catch (e) {
            erro = e.message || 'Erro ao carregar atletas.';
        }
    }

    function novoElenco() {
        editandoId = null;
        erro = '';
        mensagem = '';

        formulario = {
            ano: new Date().getFullYear(),
            status: true
        };

        formularioAberto = true;
    }

    function editarElenco(elenco) {
        editandoId = elenco.id;
        erro = '';
        mensagem = '';

        formulario = {
            ano: elenco.ano,
            status: elenco.status
        };

        formularioAberto = true;
    }

    function cancelarFormulario() {
        formularioAberto = false;
        editandoId = null;
    }

    async function salvarElenco(evento) {
        evento.preventDefault();

        erro = '';
        mensagem = '';
        salvando = true;

        try {
            const ano = Number(formulario.ano);

            if (!Number.isInteger(ano) || ano < 1900 || ano > 2200) {
                throw new Error('Informe um ano válido.');
            }

            const estavaEditando = editandoId !== null;
            const dados = {
                ano,
                status: formulario.status
            };

            await requisicao(
                estavaEditando
                    ? `/elencos/${editandoId}`
                    : '/elencos/',
                {
                    method: estavaEditando ? 'PUT' : 'POST',
                    body: JSON.stringify(dados)
                }
            );

            formularioAberto = false;
            editandoId = null;

            mensagem = estavaEditando
                ? 'Elenco atualizado com sucesso!'
                : 'Elenco cadastrado com sucesso!';

            await carregarElencos();
        } catch (e) {
            erro = e.message || 'Erro ao salvar elenco.';
        } finally {
            salvando = false;
        }
    }

    async function visualizarAtletas(elenco) {
        elencoSelecionado = elenco;
        atletasDoElenco = [];
        atletaSelecionadoId = '';
        carregandoAtletas = true;
        erro = '';
        mensagem = '';

        try {
            const resultado = await requisicao(
                `/elencos/${elenco.id}/atletas`
            );

            atletasDoElenco = Array.isArray(resultado)
                ? resultado
                : [];

            await carregarAtletasDisponiveis();
        } catch (e) {
            erro = e.message || 'Erro ao consultar os atletas do elenco.';
        } finally {
            carregandoAtletas = false;
        }
    }

    async function adicionarAtleta() {
        if (!elencoSelecionado || !atletaSelecionadoId) {
            erro = 'Selecione um atleta para adicionar.';
            return;
        }

        erro = '';
        mensagem = '';

        try {
            await requisicao(
                `/elencos/${elencoSelecionado.id}/atletas/${atletaSelecionadoId}`,
                { method: 'POST' }
            );

            mensagem = 'Atleta adicionado ao elenco com sucesso!';
            await visualizarAtletas(elencoSelecionado);
        } catch (e) {
            erro = e.message || 'Erro ao adicionar atleta.';
        }
    }

    async function removerAtleta(atleta) {
        const confirmar = window.confirm(
            `Deseja remover ${atleta.nome} deste elenco? O cadastro do atleta será mantido.`
        );

        if (!confirmar) return;

        erro = '';
        mensagem = '';

        try {
            await requisicao(
                `/elencos/${elencoSelecionado.id}/atletas/${atleta.id}`,
                { method: 'DELETE' }
            );

            mensagem = 'Atleta removido do elenco com sucesso!';
            await visualizarAtletas(elencoSelecionado);
        } catch (e) {
            erro = e.message || 'Erro ao remover atleta.';
        }
    }

    async function excluirElenco(elenco) {
        const confirmar = window.confirm(
            `Deseja excluir o elenco de ${elenco.ano}?`
        );

        if (!confirmar) return;

        erro = '';
        mensagem = '';

        try {
            await requisicao(`/elencos/${elenco.id}`, {
                method: 'DELETE'
            });

            if (elencoSelecionado?.id === elenco.id) {
                elencoSelecionado = null;
                atletasDoElenco = [];
            }

            mensagem = 'Elenco excluído com sucesso!';
            await carregarElencos();
        } catch (e) {
            erro = e.message || 'Erro ao excluir elenco.';
        }
    }

    onMount(() => {
        carregarElencos();
    });
</script>

<svelte:head>
    <title>Elencos | Clube Futsal</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">CLUBE FUTSAL</p>
            <h1>Gerenciamento de elencos</h1>
            <p>Organize os elencos e os atletas de cada temporada.</p>
        </div>

        <button class="botao-secundario" onclick={() => goto('/admin')}>
            Voltar ao painel
        </button>
    </header>

    <main>
        {#if mensagem}
            <p class="alerta sucesso">{mensagem}</p>
        {/if}

        {#if erro}
            <p class="alerta falha">{erro}</p>
        {/if}

        <div class="barra-acoes">
            <div>
                <h2>Elencos cadastrados</h2>
                <p>{elencos.length} elenco(s) encontrado(s)</p>
            </div>

            <button class="botao-principal" onclick={novoElenco}>
                + Novo elenco
            </button>
        </div>

        {#if formularioAberto}
            <section class="cartao">
                <h2>
                    {editandoId !== null ? 'Editar elenco' : 'Cadastrar elenco'}
                </h2>

                <form onsubmit={salvarElenco}>
                    <div class="campos">
                        <label>
                            Ano do elenco
                            <input
                                type="number"
                                bind:value={formulario.ano}
                                min="1900"
                                max="2200"
                                required
                            />
                        </label>

                        <label class="campo-status">
                            <input
                                type="checkbox"
                                bind:checked={formulario.status}
                            />
                            Elenco ativo
                        </label>
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
                            {salvando ? 'Salvando...' : 'Salvar elenco'}
                        </button>
                    </div>
                </form>
            </section>
        {/if}

        <section class="cartao">
            {#if carregando}
                <p class="estado">Carregando elencos...</p>
            {:else if elencos.length === 0}
                <p class="estado">
                    Nenhum elenco cadastrado. Você pode criar o primeiro!
                </p>
            {:else}
                <div class="tabela-responsiva">
                    <table>
                        <thead>
                            <tr>
                                <th>Ano</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>

                        <tbody>
                            {#each elencos as elenco (elenco.id)}
                                <tr>
                                    <td>{elenco.ano}</td>
                                    <td>
                                        <span
                                            class="status"
                                            class:inativo={!elenco.status}
                                        >
                                            {elenco.status ? 'Ativo' : 'Inativo'}
                                        </span>
                                    </td>
                                    <td>
                                        <div class="acoes">
                                            <button
                                                class="botao-detalhes"
                                                onclick={() => visualizarAtletas(elenco)}
                                            >
                                                Ver atletas
                                            </button>

                                            <button
                                                class="botao-editar"
                                                onclick={() => editarElenco(elenco)}
                                            >
                                                Editar
                                            </button>

                                            <button
                                                class="botao-excluir"
                                                onclick={() => excluirElenco(elenco)}
                                            >
                                                Excluir
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </section>

        {#if elencoSelecionado}
            <section class="cartao detalhes">
                <div class="titulo-detalhes">
                    <div>
                        <p class="subtitulo-verde">ELENCO SELECIONADO</p>
                        <h2>Atletas do elenco de {elencoSelecionado.ano}</h2>
                        <p>
                            {atletasDoElenco.length} atleta(s) neste elenco
                        </p>
                    </div>

                    <button
                        class="botao-secundario"
                        onclick={() => {
                            elencoSelecionado = null;
                            atletasDoElenco = [];
                        }}
                    >
                        Fechar
                    </button>
                </div>

                <div class="adicionar-atleta">
                    <label>
                        Adicionar atleta
                        <select bind:value={atletaSelecionadoId}>
                            <option value="">Selecione um atleta</option>

                            {#each atletasDisponiveis as atleta (atleta.id)}
                                <option value={String(atleta.id)}>
                                    {atleta.nome} — {atleta.posicao} (#{atleta.numero})
                                </option>
                            {/each}
                        </select>
                    </label>

                    <button
                        class="botao-principal"
                        onclick={adicionarAtleta}
                        disabled={!atletaSelecionadoId || carregandoAtletas}
                    >
                        + Adicionar ao elenco
                    </button>
                </div>

                {#if carregandoAtletas}
                    <p class="estado">Carregando atletas...</p>
                {:else if atletasDoElenco.length === 0}
                    <p class="estado">
                        Este elenco ainda não possui atletas.
                    </p>
                {:else}
                    <div class="tabela-responsiva">
                        <table>
                            <thead>
                                <tr>
                                    <th>Número</th>
                                    <th>Nome</th>
                                    <th>Posição</th>
                                    <th>Ação</th>
                                </tr>
                            </thead>

                            <tbody>
                                {#each atletasDoElenco as atleta (atleta.id)}
                                    <tr>
                                        <td>#{atleta.numero}</td>
                                        <td>{atleta.nome}</td>
                                        <td>{atleta.posicao}</td>
                                        <td>
                                            <button
                                                class="botao-excluir"
                                                onclick={() => removerAtleta(atleta)}
                                            >
                                                Remover do elenco
                                            </button>
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                {/if}
            </section>
        {/if}
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

    .subtitulo-verde {
        color: #236b50;
        font-size: 12px;
        letter-spacing: 2px;
        font-weight: bold;
    }

    h1 {
        margin: 8px 0;
        font-size: 30px;
    }

    h2 {
        margin-top: 0;
    }

    .cabecalho p:last-child {
        color: #d6e5dd;
    }

    .barra-acoes,
    .titulo-detalhes {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        margin-bottom: 22px;
    }

    .barra-acoes p,
    .titulo-detalhes p:last-child {
        color: #687386;
        margin-bottom: 0;
    }

    .botao-principal,
    .botao-secundario,
    .botao-detalhes,
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
        cursor: not-allowed;
    }

    .botao-secundario {
        background: white;
        color: #173d32;
    }

    .cartao {
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

    .botao-detalhes {
        background: #dff5e8;
        color: #17623a;
    }

    .botao-editar {
        background: #e5efff;
        color: #2455a5;
    }

    .botao-excluir {
        background: #fde8e8;
        color: #a12727;
    }

    .adicionar-atleta {
        display: flex;
        align-items: flex-end;
        gap: 12px;
        margin-bottom: 24px;
    }

    .adicionar-atleta label {
        flex: 1;
    }

    @media (max-width: 650px) {
        .pagina {
            padding: 16px;
        }

        .cabecalho,
        .barra-acoes,
        .titulo-detalhes,
        .adicionar-atleta {
            align-items: flex-start;
            flex-direction: column;
        }

        .botoes-formulario {
            flex-direction: column-reverse;
        }

        .adicionar-atleta,
        .adicionar-atleta label,
        .adicionar-atleta button {
            width: 100%;
            box-sizing: border-box;
        }
    }
</style>
