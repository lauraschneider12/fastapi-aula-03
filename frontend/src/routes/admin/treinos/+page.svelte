
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let treinos = $state([]);
    let elencos = $state([]);
    let carregando = $state(true);
    let salvando = $state(false);
    let erro = $state('');
    let mensagem = $state('');

    let formularioAberto = $state(false);
    let editandoId = $state(null);
    let filtroElenco = $state('');

    let formulario = $state({
        data: '',
        local: '',
        descricao: '',
        elenco_id: ''
    });

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
                ...(opcoes.body ? { 'Content-Type': 'application/json' } : {}),
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
            let detalhe = 'Ocorreu um erro na operação.';

            try {
                const dados = await resposta.json();
                detalhe = typeof dados.detail === 'string'
                    ? dados.detail
                    : detalhe;
            } catch {
                // Mantém a mensagem padrão.
            }

            throw new Error(detalhe);
        }

        if (resposta.status === 204) return null;

        const texto = await resposta.text();
        return texto ? JSON.parse(texto) : null;
    }

    async function carregarDados() {
        carregando = true;
        erro = '';

        try {
            const [dadosTreinos, dadosElencos] = await Promise.all([
                requisicao('/treinos/'),
                requisicao('/elencos/')
            ]);

            treinos = dadosTreinos;
            elencos = dadosElencos;
        } catch (e) {
            erro = e.message || 'Não foi possível carregar os dados.';
        } finally {
            carregando = false;
        }
    }

    const elencosAtivos = $derived(
        elencos.filter(elenco => elenco.status === true)
    );

    const treinosFiltrados = $derived(
        [...treinos]
            .filter(treino =>
                !filtroElenco || String(treino.elenco_id) === filtroElenco
            )
            .sort((a, b) => new Date(a.data) - new Date(b.data))
    );

    function formatarData(data) {
        if (!data) return '';

        return new Date(data).toLocaleString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function dataParaFormulario(data) {
        const dataLocal = new Date(data);
        const deslocamento = dataLocal.getTimezoneOffset() * 60000;

        return new Date(dataLocal.getTime() - deslocamento)
            .toISOString()
            .slice(0, 16);
    }

    function nomeElenco(elencoId) {
        const elenco = elencos.find(e => e.id === elencoId);
        return elenco ? `Elenco ${elenco.ano}` : `Elenco ${elencoId}`;
    }

    function abrirCadastro() {
        editandoId = null;

        formulario = {
            data: '',
            local: '',
            descricao: '',
            elenco_id: ''
        };

        erro = '';
        mensagem = '';
        formularioAberto = true;
    }

    function editarTreino(treino) {
        editandoId = treino.id;

        formulario = {
            data: dataParaFormulario(treino.data),
            local: treino.local,
            descricao: treino.descricao,
            elenco_id: String(treino.elenco_id)
        };

        erro = '';
        mensagem = '';
        formularioAberto = true;
    }

    function cancelarFormulario() {
        formularioAberto = false;
        editandoId = null;
        erro = '';
    }

    async function salvarTreino() {
        erro = '';
        mensagem = '';

        if (
            !formulario.data ||
            !formulario.local.trim() ||
            !formulario.descricao.trim() ||
            !formulario.elenco_id
        ) {
            erro = 'Preencha todos os campos.';
            return;
        }

        salvando = true;

        try {
            const dados = {
                data: new Date(formulario.data).toISOString(),
                local: formulario.local.trim(),
                descricao: formulario.descricao.trim(),
                elenco_id: Number(formulario.elenco_id)
            };

            if (editandoId) {
                await requisicao(`/treinos/${editandoId}`, {
                    method: 'PUT',
                    body: JSON.stringify(dados)
                });

                mensagem = 'Treino atualizado com sucesso!';
            } else {
                await requisicao('/treinos/', {
                    method: 'POST',
                    body: JSON.stringify(dados)
                });

                mensagem = 'Treino cadastrado com sucesso!';
            }

            formularioAberto = false;
            editandoId = null;

            await carregarDados();
        } catch (e) {
            erro = e.message || 'Não foi possível salvar o treino.';
        } finally {
            salvando = false;
        }
    }

    async function excluirTreino(treino) {
        const confirmar = window.confirm(
            `Deseja realmente excluir o treino de ${formatarData(treino.data)}?`
        );

        if (!confirmar) return;

        erro = '';
        mensagem = '';

        try {
            await requisicao(`/treinos/${treino.id}`, {
                method: 'DELETE'
            });

            mensagem = 'Treino excluído com sucesso!';
            await carregarDados();
        } catch (e) {
            erro = e.message || 'Não foi possível excluir o treino.';
        }
    }

    onMount(() => {
        carregarDados();
    });
</script>

<svelte:head>
    <title>Gerenciar Treinos</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <h1>Gerenciamento de Treinos</h1>
            <p>Cadastre e organize os treinos dos elencos.</p>
        </div>

        <button class="botao-voltar" onclick={() => goto('/admin')}>
            Voltar ao painel
        </button>
    </header>

    <div class="barra-acoes">
        <div>
            <label for="filtro">Filtrar por elenco</label>

            <select id="filtro" bind:value={filtroElenco}>
                <option value="">Todos os elencos</option>

                {#each elencosAtivos as elenco}
                    <option value={String(elenco.id)}>
                        Elenco {elenco.ano}
                    </option>
                {/each}
            </select>
        </div>

        <button class="botao-principal" onclick={abrirCadastro}>
            + Novo treino
        </button>
    </div>

    {#if mensagem}
        <div class="alerta sucesso">{mensagem}</div>
    {/if}

    {#if erro && !formularioAberto}
        <div class="alerta falha">{erro}</div>
    {/if}

    {#if formularioAberto}
        <section class="cartao formulario">
            <h2>{editandoId ? 'Editar treino' : 'Cadastrar novo treino'}</h2>

            {#if erro}
                <div class="alerta falha">{erro}</div>
            {/if}

            <form onsubmit={(event) => {
                event.preventDefault();
                salvarTreino();
            }}>
                <div class="campos">
                    <div class="campo">
                        <label for="data">Data e horário</label>
                        <input
                            id="data"
                            type="datetime-local"
                            bind:value={formulario.data}
                            required
                        />
                    </div>

                    <div class="campo">
                        <label for="local">Local</label>
                        <input
                            id="local"
                            type="text"
                            bind:value={formulario.local}
                            placeholder="Ex.: Ginásio Municipal"
                            minlength="2"
                            maxlength="200"
                            required
                        />
                    </div>

                    <div class="campo campo-completo">
                        <label for="descricao">Descrição</label>
                        <textarea
                            id="descricao"
                            bind:value={formulario.descricao}
                            placeholder="Descreva as atividades do treino..."
                            minlength="2"
                            required
                        ></textarea>
                    </div>

                    <div class="campo">
                        <label for="elenco">Elenco</label>
                        <select
                            id="elenco"
                            bind:value={formulario.elenco_id}
                            required
                        >
                            <option value="">Selecione um elenco</option>

                            {#each elencosAtivos as elenco}
                                <option value={String(elenco.id)}>
                                    Elenco {elenco.ano}
                                </option>
                            {/each}
                        </select>
                    </div>
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
                        {salvando
                            ? 'Salvando...'
                            : editandoId
                                ? 'Salvar alterações'
                                : 'Cadastrar treino'}
                    </button>
                </div>
            </form>
        </section>
    {/if}

    <section class="cartao">
        <div class="titulo-lista">
            <h2>Treinos cadastrados</h2>
            <span>{treinosFiltrados.length} treino(s)</span>
        </div>

        {#if carregando}
            <p class="estado">Carregando treinos...</p>
        {:else if treinosFiltrados.length === 0}
            <p class="estado">Nenhum treino encontrado.</p>
        {:else}
            <div class="tabela-responsiva">
                <table>
                    <thead>
                        <tr>
                            <th>Data e horário</th>
                            <th>Local</th>
                            <th>Descrição</th>
                            <th>Elenco</th>
                            <th>Ações</th>
                        </tr>
                    </thead>

                    <tbody>
                        {#each treinosFiltrados as treino}
                            <tr>
                                <td>{formatarData(treino.data)}</td>
                                <td>{treino.local}</td>
                                <td class="descricao">{treino.descricao}</td>
                                <td>{nomeElenco(treino.elenco_id)}</td>
                                <td>
                                    <div class="acoes">
                                        <button
                                            class="botao-editar"
                                            onclick={() => editarTreino(treino)}
                                        >
                                            Editar
                                        </button>

                                        <button
                                            class="botao-excluir"
                                            onclick={() => excluirTreino(treino)}
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
</div>

<style>
    :global(body) {
        margin: 0;
        background: #f3f5f9;
    }

    .pagina {
        max-width: 1200px;
        margin: 0 auto;
        padding: 35px 25px;
        color: #26352f;
    }

    .cabecalho {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        margin-bottom: 30px;
    }

    h1 {
        color: #173d32;
        margin: 0 0 8px;
        font-size: 28px;
    }

    h2 {
        color: #173d32;
        font-size: 20px;
        margin: 0 0 22px;
    }

    .cabecalho p {
        color: #68756f;
        margin: 0;
    }

    .barra-acoes {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 20px;
        margin-bottom: 22px;
    }

    .barra-acoes > div {
        display: flex;
        flex-direction: column;
        gap: 7px;
        width: 260px;
    }

    label {
        font-size: 14px;
        font-weight: 600;
        color: #34483e;
    }

    input, select, textarea {
        width: 100%;
        box-sizing: border-box;
        padding: 11px 12px;
        border: 1px solid #d5ddd8;
        border-radius: 7px;
        background: white;
        color: #26352f;
        font: inherit;
    }

    input:focus, select:focus, textarea:focus {
        outline: 2px solid #a7cbbb;
        border-color: #236b50;
    }

    textarea {
        min-height: 100px;
        resize: vertical;
    }

    button {
        border: none;
        border-radius: 7px;
        padding: 11px 17px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.2s;
    }

    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .botao-principal {
        background: #236b50;
        color: white;
    }

    .botao-principal:hover {
        background: #194e3a;
    }

    .botao-voltar, .botao-secundario {
        background: #e5ebe7;
        color: #34483e;
    }

    .botao-voltar:hover, .botao-secundario:hover {
        background: #d5ded8;
    }

    .cartao {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 22px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    }

    .formulario {
        border-top: 4px solid #236b50;
    }

    .campos {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 20px;
    }

    .campo {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .campo-completo {
        grid-column: 1 / -1;
    }

    .botoes-formulario {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
        margin-top: 25px;
    }

    .titulo-lista {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px;
    }

    .titulo-lista span {
        color: #68756f;
        font-size: 14px;
    }

    .tabela-responsiva {
        overflow-x: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        min-width: 750px;
    }

    th, td {
        text-align: left;
        padding: 14px 12px;
        border-bottom: 1px solid #edf0ee;
        font-size: 14px;
    }

    th {
        color: #53645b;
        background: #f8faf9;
        font-weight: 600;
    }

    td {
        color: #34483e;
    }

    .descricao {
        max-width: 240px;
        overflow-wrap: anywhere;
    }

    .acoes {
        display: flex;
        gap: 8px;
    }

    .botao-editar {
        background: #e6f0eb;
        color: #236b50;
    }

    .botao-excluir {
        background: #fbe9e9;
        color: #b83a3a;
    }

    .botao-editar:hover {
        background: #d1e5d9;
    }

    .botao-excluir:hover {
        background: #f4d4d4;
    }

    .alerta {
        padding: 13px 16px;
        border-radius: 7px;
        margin-bottom: 18px;
        font-size: 14px;
    }

    .sucesso {
        background: #e4f4e9;
        color: #236b50;
    }

    .falha {
        background: #fbe9e9;
        color: #a52f2f;
    }

    .estado {
        text-align: center;
        padding: 35px 10px;
        color: #68756f;
    }

    @media (max-width: 700px) {
        .pagina {
            padding: 22px 15px;
        }

        .cabecalho, .barra-acoes {
            align-items: stretch;
            flex-direction: column;
        }

        .barra-acoes > div {
            width: 100%;
        }

        .campos {
            grid-template-columns: 1fr;
        }

        .campo-completo {
            grid-column: auto;
        }

        .botoes-formulario {
            flex-direction: column-reverse;
        }

        .botoes-formulario button {
            width: 100%;
        }
    }
</style>
