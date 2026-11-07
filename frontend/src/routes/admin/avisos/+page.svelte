
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let avisos = $state([]);
    let elencos = $state([]);
    let carregando = $state(true);
    let salvando = $state(false);
    let erro = $state('');
    let mensagem = $state('');
    let formularioAberto = $state(false);
    let editandoId = $state(null);

    let formulario = $state({
        titulo: '',
        conteudo: '',
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
            } catch {}

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
            const [dadosAvisos, dadosElencos] = await Promise.all([
                requisicao('/avisos/'),
                requisicao('/elencos/')
            ]);

            avisos = dadosAvisos;
            elencos = dadosElencos;
        } catch (e) {
            erro = e.message;
        } finally {
            carregando = false;
        }
    }

    const elencosAtivos = $derived(
        elencos.filter(elenco => elenco.status === true)
    );

    const avisosOrdenados = $derived(
        [...avisos].sort(
            (a, b) => new Date(b.data_publicacao) - new Date(a.data_publicacao)
        )
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

    function nomeElenco(id) {
        if (id === null || id === undefined) return 'Todos os elencos';

        const elenco = elencos.find(e => e.id === id);
        return elenco ? `Elenco ${elenco.ano}` : `Elenco ${id}`;
    }

    function abrirCadastro() {
        editandoId = null;
        formulario = {
            titulo: '',
            conteudo: '',
            elenco_id: ''
        };

        erro = '';
        mensagem = '';
        formularioAberto = true;
    }

    function editarAviso(aviso) {
        editandoId = aviso.id;

        formulario = {
            titulo: aviso.titulo,
            conteudo: aviso.conteudo,
            elenco_id: aviso.elenco_id === null
                ? ''
                : String(aviso.elenco_id)
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

    async function salvarAviso() {
        erro = '';
        mensagem = '';

        if (!formulario.titulo.trim() || !formulario.conteudo.trim()) {
            erro = 'Preencha o título e o conteúdo do aviso.';
            return;
        }

        salvando = true;

        try {
            const dados = {
                titulo: formulario.titulo.trim(),
                conteudo: formulario.conteudo.trim(),
                elenco_id: formulario.elenco_id
                    ? Number(formulario.elenco_id)
                    : null
            };

            if (editandoId !== null) {
                await requisicao(`/avisos/${editandoId}`, {
                    method: 'PUT',
                    body: JSON.stringify(dados)
                });

                mensagem = 'Aviso atualizado com sucesso!';
            } else {
                await requisicao('/avisos/', {
                    method: 'POST',
                    body: JSON.stringify(dados)
                });

                mensagem = 'Aviso publicado com sucesso!';
            }

            formularioAberto = false;
            editandoId = null;

            await carregarDados();
        } catch (e) {
            erro = e.message;
        } finally {
            salvando = false;
        }
    }

    async function excluirAviso(aviso) {
        if (!window.confirm(`Deseja excluir o aviso "${aviso.titulo}"?`)) {
            return;
        }

        erro = '';
        mensagem = '';

        try {
            await requisicao(`/avisos/${aviso.id}`, {
                method: 'DELETE'
            });

            mensagem = 'Aviso excluído com sucesso!';
            await carregarDados();
        } catch (e) {
            erro = e.message;
        }
    }

    onMount(carregarDados);
</script>

<svelte:head>
    <title>Gerenciar Avisos</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <h1>Gerenciamento de Avisos</h1>
            <p>Publique comunicados para as atletas e os elencos.</p>
        </div>

        <button class="secundario" onclick={() => goto('/admin')}>
            Voltar ao painel
        </button>
    </header>

    <div class="barra-acoes">
        <span>{avisos.length} aviso(s) publicado(s)</span>

        <button class="principal" onclick={abrirCadastro}>
            + Novo aviso
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
            <h2>{editandoId !== null ? 'Editar aviso' : 'Publicar aviso'}</h2>

            {#if erro}
                <div class="alerta falha">{erro}</div>
            {/if}

            <form onsubmit={(event) => {
                event.preventDefault();
                salvarAviso();
            }}>
                <div class="campo">
                    <label for="titulo">Título</label>
                    <input
                        id="titulo"
                        bind:value={formulario.titulo}
                        maxlength="150"
                        required
                        placeholder="Ex.: Alteração no horário do treino"
                    />
                </div>

                <div class="campo">
                    <label for="conteudo">Conteúdo</label>
                    <textarea
                        id="conteudo"
                        bind:value={formulario.conteudo}
                        required
                        placeholder="Escreva o comunicado..."
                    ></textarea>
                </div>

                <div class="campo">
                    <label for="elenco">Destinatários</label>
                    <select id="elenco" bind:value={formulario.elenco_id}>
                        <option value="">Todos os elencos</option>

                        {#each elencosAtivos as elenco}
                            <option value={String(elenco.id)}>
                                Elenco {elenco.ano}
                            </option>
                        {/each}
                    </select>

                    <small>
                        Se não selecionar um elenco, o aviso será geral.
                    </small>
                </div>

                <div class="botoes">
                    <button
                        type="button"
                        class="secundario"
                        onclick={cancelarFormulario}
                        disabled={salvando}
                    >
                        Cancelar
                    </button>

                    <button
                        type="submit"
                        class="principal"
                        disabled={salvando}
                    >
                        {salvando ? 'Salvando...' : 'Salvar aviso'}
                    </button>
                </div>
            </form>
        </section>
    {/if}

    <section class="cartao">
        <h2>Avisos publicados</h2>

        {#if carregando}
            <p class="estado">Carregando avisos...</p>
        {:else if avisosOrdenados.length === 0}
            <p class="estado">Nenhum aviso publicado.</p>
        {:else}
            <div class="lista">
                {#each avisosOrdenados as aviso}
                    <article class="aviso">
                        <div class="aviso-topo">
                            <div>
                                <h3>{aviso.titulo}</h3>
                                <span class="destinatario">
                                    {nomeElenco(aviso.elenco_id)}
                                </span>
                            </div>

                            <span class="data">
                                {formatarData(aviso.data_publicacao)}
                            </span>
                        </div>

                        <p class="conteudo">{aviso.conteudo}</p>

                        <div class="acoes">
                            <button
                                class="editar"
                                onclick={() => editarAviso(aviso)}
                            >
                                Editar
                            </button>

                            <button
                                class="excluir"
                                onclick={() => excluirAviso(aviso)}
                            >
                                Excluir
                            </button>
                        </div>
                    </article>
                {/each}
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
        max-width: 1100px;
        margin: auto;
        padding: 35px 25px;
        color: #26352f;
    }

    .cabecalho, .barra-acoes, .aviso-topo {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
    }

    .cabecalho {
        margin-bottom: 28px;
    }

    h1, h2, h3 {
        color: #173d32;
    }

    h1 {
        margin: 0 0 8px;
        font-size: 28px;
    }

    h2 {
        margin: 0 0 22px;
        font-size: 20px;
    }

    h3 {
        margin: 0 0 10px;
        font-size: 18px;
    }

    .cabecalho p, .barra-acoes span {
        color: #68756f;
    }

    .barra-acoes {
        margin-bottom: 22px;
    }

    button {
        border: none;
        border-radius: 7px;
        padding: 11px 17px;
        font-weight: 600;
        cursor: pointer;
    }

    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .principal {
        background: #236b50;
        color: white;
    }

    .principal:hover {
        background: #194e3a;
    }

    .secundario {
        background: #e5ebe7;
        color: #34483e;
    }

    .cartao {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 22px;
        box-shadow: 0 2px 10px #00000008;
    }

    .formulario {
        border-top: 4px solid #236b50;
    }

    .campo {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 20px;
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
        font: inherit;
        background: white;
    }

    textarea {
        min-height: 130px;
        resize: vertical;
    }

    small {
        color: #68756f;
    }

    .botoes, .acoes {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 20px;
    }

    .aviso {
        padding: 20px 0;
        border-bottom: 1px solid #edf0ee;
    }

    .aviso:last-child {
        border-bottom: none;
    }

    .destinatario {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: #e6f0eb;
        color: #236b50;
        font-size: 12px;
    }

    .data {
        color: #68756f;
        font-size: 13px;
    }

    .conteudo {
        color: #46564e;
        white-space: pre-wrap;
        line-height: 1.6;
        overflow-wrap: anywhere;
    }

    .editar {
        background: #e6f0eb;
        color: #236b50;
    }

    .excluir {
        background: #fbe9e9;
        color: #b83a3a;
    }

    .alerta {
        padding: 13px 16px;
        border-radius: 7px;
        margin-bottom: 18px;
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
        padding: 30px;
        color: #68756f;
    }

    @media (max-width: 650px) {
        .pagina {
            padding: 22px 15px;
        }

        .cabecalho, .barra-acoes, .aviso-topo {
            align-items: stretch;
            flex-direction: column;
        }

        .botoes {
            flex-direction: column-reverse;
        }

        .botoes button {
            width: 100%;
        }
    }
</style>
