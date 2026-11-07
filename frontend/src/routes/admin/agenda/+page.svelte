
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let jogos = $state([]);
    let elencos = $state([]);
    let atletas = $state([]);

    let carregando = $state(true);
    let salvando = $state(false);
    let erro = $state('');
    let mensagem = $state('');

    let formularioAberto = $state(false);
    let editandoId = $state(null);

    let formulario = $state({
        local: '',
        time_adversario: '',
        data: '',
        elenco_id: ''
    });

    let gols = $state([]);
    let cartoes = $state([]);

    // Somente elencos ativos podem receber novos jogos.
    let elencosAtivos = $derived(
        elencos.filter((elenco) => elenco.status === true)
    );

    // Somente atletas ativas podem receber gols e cartões.
    let atletasAtivas = $derived(
        atletas.filter((atleta) => atleta.status === true)
    );

    // Calcula o placar automaticamente.
    let placarLocal = $derived(
        gols.filter(
            (gol) => Number(gol.id_jogador) !== 100
        ).length
    );

    let placarVisitante = $derived(
        gols.filter(
            (gol) => Number(gol.id_jogador) === 100
        ).length
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

    function formatarParaFormulario(data) {
        if (!data) return '';

        const dataObj = new Date(data);

        if (Number.isNaN(dataObj.getTime())) {
            return String(data).slice(0, 16);
        }

        const deslocamento = dataObj.getTimezoneOffset() * 60000;

        return new Date(dataObj.getTime() - deslocamento)
            .toISOString()
            .slice(0, 16);
    }

    function formatarData(data) {
        if (!data) return 'Não informada';

        const dataObj = new Date(data);

        if (Number.isNaN(dataObj.getTime())) {
            return data;
        }

        return dataObj.toLocaleString('pt-BR', {
            dateStyle: 'short',
            timeStyle: 'short'
        });
    }

    async function carregarDados() {
        carregando = true;
        erro = '';

        try {
            const [listaJogos, listaElencos, listaAtletas] =
                await Promise.all([
                    requisicao('/jogos/'),
                    requisicao('/elencos/'),
                    requisicao('/atletas/')
                ]);

            jogos = Array.isArray(listaJogos) ? listaJogos : [];
            elencos = Array.isArray(listaElencos) ? listaElencos : [];
            atletas = Array.isArray(listaAtletas) ? listaAtletas : [];

        } catch (e) {
            erro = e.message || 'Erro ao carregar os dados da agenda.';
        } finally {
            carregando = false;
        }
    }

    function limparFormulario() {
        formulario = {
            local: '',
            time_adversario: '',
            data: '',
            elenco_id: ''
        };

        gols = [];
        cartoes = [];
    }

    function novoJogo() {
        erro = '';
        mensagem = '';
        editandoId = null;

        limparFormulario();

        formularioAberto = true;
    }

    function editarJogo(jogo) {
        erro = '';
        mensagem = '';
        editandoId = jogo.id;

        formulario = {
            local: jogo.local ?? '',
            time_adversario: jogo.time_adversario ?? '',
            data: formatarParaFormulario(jogo.data),
            elenco_id: String(jogo.elenco_id ?? '')
        };

        // A API agrupa os gols por atleta.
        // Transformamos a quantidade em registros individuais.
        gols = (jogo.gols ?? []).flatMap((gol) =>
            Array.from(
                { length: Number(gol.quantidade) },
                () => ({
                    id_jogador: String(gol.id_jogador)
                })
            )
        );

        // Carrega os cartões já cadastrados.
        cartoes = (jogo.cartoes ?? []).map((cartao) => ({
            id_jogador: String(cartao.id_jogador),
            tipo: cartao.tipo
        }));

        formularioAberto = true;
    }

    function adicionarGol() {
        gols.push({
            id_jogador: ''
        });
    }

    function removerGol(indice) {
        gols.splice(indice, 1);
    }

    function adicionarCartao() {
        cartoes.push({
            id_jogador: '',
            tipo: 'amarelo'
        });
    }

    function removerCartao(indice) {
        cartoes.splice(indice, 1);
    }

    function cancelarFormulario() {
        formularioAberto = false;
        editandoId = null;
        limparFormulario();
    }

    function nomeElenco(elencoId) {
        const elenco = elencos.find(
            (item) => item.id === elencoId
        );

        return elenco
            ? `${elenco.ano}${elenco.status ? '' : ' (inativo)'}`
            : `Elenco #${elencoId}`;
    }

    function placarJogo(jogo) {
        if (
            jogo.gol_local === 0 &&
            jogo.gol_visitante === 0 &&
            (!jogo.gols || jogo.gols.length === 0)
        ) {
            return 'A definir';
        }

        return `${jogo.gol_local} x ${jogo.gol_visitante}`;
    }

    async function salvarJogo(evento) {
        evento.preventDefault();

        erro = '';
        mensagem = '';
        salvando = true;

        try {
            const elencoId = Number(formulario.elenco_id);

            // Confere se o elenco existe e está ativo.
            const elencoValido = elencosAtivos.some(
                (elenco) => elenco.id === elencoId
            );

            if (!Number.isInteger(elencoId) || !elencoValido) {
                throw new Error(
                    'Selecione um elenco existente e ativo.'
                );
            }

            if (!formulario.data) {
                throw new Error(
                    'Informe a data e o horário do jogo.'
                );
            }

            const dataObj = new Date(formulario.data);

            if (Number.isNaN(dataObj.getTime())) {
                throw new Error('Informe uma data válida.');
            }

            const local = formulario.local.trim();
            const adversario = formulario.time_adversario.trim();

            if (local.length < 2) {
                throw new Error(
                    'Informe um local com pelo menos 2 caracteres.'
                );
            }

            if (adversario.length < 2) {
                throw new Error(
                    'Informe o adversário com pelo menos 2 caracteres.'
                );
            }

            // Valida e prepara os gols.
            const golsFormatados = gols.map((gol) => {
                const id = Number(gol.id_jogador);

                if (!Number.isInteger(id) || id <= 0) {
                    throw new Error(
                        'Selecione uma atleta para cada gol.'
                    );
                }

                if (
                    id !== 100 &&
                    !atletasAtivas.some((atleta) => atleta.id === id)
                ) {
                    throw new Error(
                        'Uma das atletas selecionadas está inválida ou inativa.'
                    );
                }

                return {
                    id_jogador: id
                };
            });

            // Valida e prepara os cartões.
            const cartoesFormatados = cartoes.map((cartao) => {
                const id = Number(cartao.id_jogador);

                if (!Number.isInteger(id) || id <= 0 || id === 100) {
                    throw new Error(
                        'Selecione uma atleta válida para cada cartão.'
                    );
                }

                if (
                    !atletasAtivas.some((atleta) => atleta.id === id)
                ) {
                    throw new Error(
                        'Uma das atletas selecionadas está inválida ou inativa.'
                    );
                }

                if (
                    !['amarelo', 'vermelho'].includes(cartao.tipo)
                ) {
                    throw new Error(
                        'Selecione um tipo de cartão válido.'
                    );
                }

                return {
                    id_jogador: id,
                    tipo: cartao.tipo
                };
            });

            // Todos os dados são enviados na mesma requisição.
            const dados = {
                local,
                time_adversario: adversario,
                data: dataObj.toISOString(),
                elenco_id: elencoId,
                gols: golsFormatados,
                cartoes: cartoesFormatados
            };

            const estavaEditando = editandoId !== null;

            await requisicao(
                estavaEditando
                    ? `/jogos/${editandoId}`
                    : '/jogos/',
                {
                    method: estavaEditando ? 'PUT' : 'POST',
                    body: JSON.stringify(dados)
                }
            );

            formularioAberto = false;
            editandoId = null;

            mensagem = estavaEditando
                ? 'Jogo atualizado com sucesso!'
                : 'Jogo cadastrado com sucesso!';

            limparFormulario();

            await carregarDados();

        } catch (e) {
            erro = e.message || 'Erro ao salvar jogo.';
        } finally {
            salvando = false;
        }
    }

    async function excluirJogo(jogo) {
        const confirmar = window.confirm(
            `Deseja excluir o jogo contra ${jogo.time_adversario}?`
        );

        if (!confirmar) return;

        erro = '';
        mensagem = '';

        try {
            await requisicao(`/jogos/${jogo.id}`, {
                method: 'DELETE'
            });

            mensagem = 'Jogo excluído com sucesso!';

            await carregarDados();

        } catch (e) {
            erro = e.message || 'Erro ao excluir jogo.';
        }
    }

    onMount(() => {
        carregarDados();
    });
</script>

<svelte:head>
    <title>Agenda | Clube Futsal</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <p class="subtitulo">CLUBE FUTSAL</p>
            <h1>Gerenciamento da agenda</h1>
            <p>Organize as partidas, datas, locais e adversários.</p>
        </div>

        <button
            class="botao-secundario"
            onclick={() => goto('/admin')}
        >
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
                <h2>Jogos cadastrados</h2>
                <p>{jogos.length} jogo(s) encontrado(s)</p>
            </div>

            <button
                class="botao-principal"
                onclick={novoJogo}
            >
                + Novo jogo
            </button>
        </div>

        {#if formularioAberto}
            <section class="cartao">
                <h2>
                    {editandoId !== null
                        ? 'Editar jogo'
                        : 'Cadastrar jogo'}
                </h2>

                {#if elencosAtivos.length === 0}
                    <p class="alerta falha">
                        Não há elencos ativos cadastrados.
                        Cadastre ou ative um elenco antes de registrar
                        uma partida.
                    </p>
                {/if}

                <form onsubmit={salvarJogo}>
                    <h3>Informações da partida</h3>

                    <div class="campos">
                        <label>
                            Adversário
                            <input
                                type="text"
                                bind:value={formulario.time_adversario}
                                minlength="2"
                                maxlength="150"
                                placeholder="Ex.: CEP"
                                required
                            />
                        </label>

                        <label>
                            Local da partida
                            <input
                                type="text"
                                bind:value={formulario.local}
                                minlength="2"
                                maxlength="200"
                                placeholder="Ex.: Tramujas"
                                required
                            />
                        </label>

                        <label>
                            Data e horário
                            <input
                                type="datetime-local"
                                bind:value={formulario.data}
                                required
                            />
                        </label>

                        <label>
                            Elenco
                            <select
                                bind:value={formulario.elenco_id}
                                required
                                disabled={elencosAtivos.length === 0}
                            >
                                <option value="">
                                    Selecione um elenco
                                </option>

                                {#each elencosAtivos as elenco (elenco.id)}
                                    <option value={String(elenco.id)}>
                                        Elenco de {elenco.ano}
                                    </option>
                                {/each}
                            </select>
                        </label>
                    </div>

                    <!-- GOLS -->
                    <div class="secao-estatisticas">
                        <h3>Gols da partida</h3>

                        <p class="placar-preview">
                            Placar atual: {placarLocal} x {placarVisitante}
                        </p>

                        {#if gols.length === 0}
                            <p class="texto-ajuda">
                                Nenhum gol registrado. Você pode adicionar
                                os gols depois da partida.
                            </p>
                        {/if}

                        {#each gols as gol, indice (indice)}
                            <div class="linha-estatistica">
                                <label>
                                    Autora do gol

                                    <select
                                        bind:value={gol.id_jogador}
                                        required
                                    >
                                        <option value="">
                                            Selecione
                                        </option>

                                        {#each atletasAtivas as atleta (atleta.id)}
                                            <option value={String(atleta.id)}>
                                                {atleta.nome}
                                            </option>
                                        {/each}

                                        <option value="100">
                                            Adversário
                                        </option>
                                    </select>
                                </label>

                                <button
                                    type="button"
                                    class="botao-remover"
                                    onclick={() => removerGol(indice)}
                                >
                                    Remover
                                </button>
                            </div>
                        {/each}

                        <button
                            type="button"
                            class="botao-adicionar"
                            onclick={adicionarGol}
                        >
                            + Adicionar gol
                        </button>
                    </div>

                    <!-- CARTÕES -->
                    <div class="secao-estatisticas">
                        <h3>Cartões da partida</h3>

                        {#if cartoes.length === 0}
                            <p class="texto-ajuda">
                                Nenhum cartão registrado.
                            </p>
                        {/if}

                        {#each cartoes as cartao, indice (indice)}
                            <div class="linha-estatistica">
                                <label>
                                    Atleta

                                    <select
                                        bind:value={cartao.id_jogador}
                                        required
                                    >
                                        <option value="">
                                            Selecione uma atleta
                                        </option>

                                        {#each atletasAtivas as atleta (atleta.id)}
                                            <option value={String(atleta.id)}>
                                                {atleta.nome}
                                            </option>
                                        {/each}
                                    </select>
                                </label>

                                <label>
                                    Tipo de cartão

                                    <select
                                        bind:value={cartao.tipo}
                                        required
                                    >
                                        <option value="amarelo">
                                            Amarelo
                                        </option>

                                        <option value="vermelho">
                                            Vermelho
                                        </option>
                                    </select>
                                </label>

                                <button
                                    type="button"
                                    class="botao-remover"
                                    onclick={() => removerCartao(indice)}
                                >
                                    Remover
                                </button>
                            </div>
                        {/each}

                        <button
                            type="button"
                            class="botao-adicionar"
                            onclick={adicionarCartao}
                        >
                            + Adicionar cartão
                        </button>
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
                            disabled={
                                salvando || elencosAtivos.length === 0
                            }
                        >
                            {salvando ? 'Salvando...' : 'Salvar jogo'}
                        </button>
                    </div>
                </form>
            </section>
        {/if}

        <!-- LISTA DE JOGOS -->
        <section class="cartao">
            {#if carregando}
                <p class="estado">Carregando agenda...</p>

            {:else if jogos.length === 0}
                <p class="estado">
                    Nenhum jogo cadastrado. Você pode criar o primeiro!
                </p>

            {:else}
                <div class="tabela-responsiva">
                    <table>
                        <thead>
                            <tr>
                                <th>Data e horário</th>
                                <th>Adversário</th>
                                <th>Local</th>
                                <th>Placar</th>
                                <th>Elenco</th>
                                <th>Ações</th>
                            </tr>
                        </thead>

                        <tbody>
                            {#each jogos as jogo (jogo.id)}
                                <tr>
                                    <td>{formatarData(jogo.data)}</td>
                                    <td>{jogo.time_adversario}</td>
                                    <td>{jogo.local}</td>
                                    <td>{placarJogo(jogo)}</td>
                                    <td>{nomeElenco(jogo.elenco_id)}</td>

                                    <td>
                                        <div class="acoes">
                                            <button
                                                class="botao-editar"
                                                onclick={() => editarJogo(jogo)}
                                            >
                                                Editar
                                            </button>

                                            <button
                                                class="botao-excluir"
                                                onclick={() => excluirJogo(jogo)}
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

    h2 {
        margin-top: 0;
    }

    .cabecalho p:last-child {
        color: #d6e5dd;
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
        grid-template-columns: repeat(
            auto-fit,
            minmax(220px, 1fr)
        );
        gap: 18px;
    }

    label {
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-weight: bold;
        font-size: 14px;
    }

    input,
    select {
        width: 100%;
        box-sizing: border-box;
        border: 1px solid #d5dce5;
        border-radius: 8px;
        padding: 12px;
        font: inherit;
        background: white;
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

    /* Seções de gols e cartões */

    .secao-estatisticas {
        margin-top: 30px;
        padding-top: 22px;
        border-top: 1px solid #edf0f4;
    }

    .secao-estatisticas h3 {
        margin-bottom: 12px;
    }

    .placar-preview {
        display: inline-block;
        padding: 10px 16px;
        background: #e5efff;
        color: #2455a5;
        border-radius: 8px;
        font-weight: bold;
    }

    .texto-ajuda {
        color: #687386;
        font-size: 14px;
    }

    .linha-estatistica {
        display: grid;
        grid-template-columns: minmax(180px, 1fr) auto;
        align-items: end;
        gap: 12px;
        margin-bottom: 14px;
        padding: 14px;
        background: #f7f9fc;
        border-radius: 8px;
    }

    .linha-estatistica.com-cartao {
        grid-template-columns:
            minmax(160px, 1fr)
            minmax(140px, 1fr)
            auto;
    }

    .botao-adicionar,
    .botao-remover {
        border: none;
        border-radius: 8px;
        padding: 11px 14px;
        font-weight: bold;
        cursor: pointer;
    }

    .botao-adicionar {
        background: #e1f3e9;
        color: #17623a;
        margin-top: 8px;
    }

    .botao-remover {
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

        .linha-estatistica,
        .linha-estatistica.com-cartao {
            grid-template-columns: 1fr;
        }

        .linha-estatistica button {
            width: 100%;
        }
    }
</style>
