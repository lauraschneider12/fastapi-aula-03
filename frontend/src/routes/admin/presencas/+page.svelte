
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = 'http://localhost:17000';

    let treinos = $state([]);
    let elencos = $state([]);
    let presencas = $state([]);
    let atletasDoTreino = $state([]);

    let treinoSelecionado = $state('');
    let carregando = $state(false);
    let erro = $state('');
    let mensagem = $state('');
    let salvandoId = $state(null);

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

    async function carregarInicial() {
        carregando = true;
        erro = '';

        try {
            const [dadosTreinos, dadosElencos] = await Promise.all([
                requisicao('/treinos/'),
                fetch(`${API_URL}/publico/elencos`).then(async resposta => {
                    if (!resposta.ok) {
                        throw new Error('Não foi possível carregar os elencos.');
                    }
                    return resposta.json();
                })
            ]);

            treinos = dadosTreinos;
            elencos = dadosElencos;
        } catch (e) {
            erro = e.message;
        } finally {
            carregando = false;
        }
    }

    const treinoAtual = $derived(
        treinos.find(t => String(t.id) === String(treinoSelecionado))
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

    function situacaoConfirmacao(valor) {
        if (valor === true) return 'Confirmou';
        if (valor === false) return 'Não irá';
        return 'Não respondeu';
    }

    function situacaoPresenca(valor) {
        if (valor === true) return 'Presente';
        if (valor === false) return 'Ausente';
        return 'Não registrada';
    }

    function registroDaAtleta(atletaId) {
        return presencas.find(p => p.atleta_id === atletaId);
    }

    async function selecionarTreino() {
        erro = '';
        mensagem = '';
        presencas = [];
        atletasDoTreino = [];

        if (!treinoSelecionado || !treinoAtual) return;

        carregando = true;

        try {
            const elenco = elencos.find(
                e => e.id === treinoAtual.elenco_id
            );

            if (!elenco) {
                throw new Error('Não foi possível localizar o elenco do treino.');
            }

            atletasDoTreino = elenco.atletas || [];

            presencas = await requisicao(
                `/presencas/treino/${treinoAtual.id}`
            );
        } catch (e) {
            erro = e.message;
        } finally {
            carregando = false;
        }
    }

    async function registrarPresenca(atleta, presente) {
        erro = '';
        mensagem = '';
        salvandoId = atleta.id;

        try {
            await requisicao('/presencas/registrar', {
                method: 'PUT',
                body: JSON.stringify({
                    atleta_id: atleta.id,
                    treino_id: treinoAtual.id,
                    presente
                })
            });

            mensagem = `Presença de ${atleta.nome} registrada com sucesso!`;

            presencas = await requisicao(
                `/presencas/treino/${treinoAtual.id}`
            );
        } catch (e) {
            erro = e.message;
        } finally {
            salvandoId = null;
        }
    }

    onMount(carregarInicial);
</script>

<svelte:head>
    <title>Gerenciar Presenças</title>
</svelte:head>

<div class="pagina">
    <header class="cabecalho">
        <div>
            <h1>Controle de Presenças</h1>
            <p>Registre a presença real das atletas nos treinos.</p>
        </div>

        <button class="secundario" onclick={() => goto('/admin')}>
            Voltar ao painel
        </button>
    </header>

    {#if erro}
        <div class="alerta falha">{erro}</div>
    {/if}

    {#if mensagem}
        <div class="alerta sucesso">{mensagem}</div>
    {/if}

    <section class="cartao">
        <h2>Selecionar treino</h2>

        <div class="campo">
            <label for="treino">Treino</label>

            <select
                id="treino"
                bind:value={treinoSelecionado}
                onchange={selecionarTreino}
            >
                <option value="">Selecione um treino</option>

                {#each treinos as treino}
                    <option value={String(treino.id)}>
                        {formatarData(treino.data)} — {treino.local}
                    </option>
                {/each}
            </select>
        </div>

        {#if treinoAtual}
            <div class="informacoes">
                <p><strong>Local:</strong> {treinoAtual.local}</p>
                <p><strong>Descrição:</strong> {treinoAtual.descricao}</p>
                <p><strong>Elenco:</strong> {
                    elencos.find(e => e.id === treinoAtual.elenco_id)?.ano
                    ?? treinoAtual.elenco_id
                }</p>
            </div>
        {/if}
    </section>

    {#if treinoSelecionado}
        <section class="cartao">
            <div class="titulo-lista">
                <h2>Atletas do treino</h2>
                <span>{atletasDoTreino.length} atleta(s)</span>
            </div>

            {#if carregando}
                <p class="estado">Carregando informações...</p>
            {:else if atletasDoTreino.length === 0}
                <p class="estado">
                    Nenhuma atleta encontrada para o elenco deste treino.
                </p>
            {:else}
                <div class="tabela-responsiva">
                    <table>
                        <thead>
                            <tr>
                                <th>Atleta</th>
                                <th>Confirmação prévia</th>
                                <th>Presença real</th>
                                <th>Registrar</th>
                            </tr>
                        </thead>

                        <tbody>
                            {#each atletasDoTreino as atleta}
                                {@const registro = registroDaAtleta(atleta.id)}

                                <tr>
                                    <td>{atleta.nome}</td>

                                    <td>
                                        <span class="confirmacao">
                                            {situacaoConfirmacao(
                                                registro?.confirmacao ?? null
                                            )}
                                        </span>
                                    </td>

                                    <td>
                                        <span class:presente={registro?.presente === true}
                                            class:ausente={registro?.presente === false}
                                            class:pendente={registro?.presente == null}>
                                            {situacaoPresenca(
                                                registro?.presente ?? null
                                            )}
                                        </span>
                                    </td>

                                    <td>
                                        <div class="acoes">
                                            <button
                                                class="botao-presente"
                                                disabled={salvandoId !== null}
                                                onclick={() => registrarPresenca(atleta, true)}
                                            >
                                                {salvandoId === atleta.id
                                                    ? 'Salvando...'
                                                    : 'Presente'}
                                            </button>

                                            <button
                                                class="botao-ausente"
                                                disabled={salvandoId !== null}
                                                onclick={() => registrarPresenca(atleta, false)}
                                            >
                                                Ausente
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
    {:else if !carregando}
        <section class="cartao">
            <p class="estado">
                Selecione um treino para consultar e registrar as presenças.
            </p>
        </section>
    {/if}
</div>

<style>
    :global(body) {
        margin: 0;
        background: #f3f5f9;
    }

    .pagina {
        max-width: 1200px;
        margin: auto;
        padding: 35px 25px;
        color: #26352f;
    }

    .cabecalho, .titulo-lista {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
    }

    .cabecalho {
        margin-bottom: 28px;
    }

    h1, h2 {
        color: #173d32;
    }

    h1 {
        margin: 0 0 8px;
        font-size: 28px;
    }

    h2 {
        margin: 0 0 20px;
        font-size: 20px;
    }

    .cabecalho p {
        color: #68756f;
        margin: 0;
    }

    .cartao {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 22px;
        box-shadow: 0 2px 10px #00000008;
    }

    .campo {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    label {
        font-size: 14px;
        font-weight: 600;
    }

    select {
        width: 100%;
        box-sizing: border-box;
        padding: 11px 12px;
        border: 1px solid #d5ddd8;
        border-radius: 7px;
        background: white;
        font: inherit;
    }

    button {
        border: none;
        border-radius: 7px;
        padding: 10px 13px;
        font-weight: 600;
        cursor: pointer;
    }

    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .secundario {
        background: #e5ebe7;
        color: #34483e;
    }

    .informacoes {
        margin-top: 20px;
        padding: 15px;
        border-radius: 8px;
        background: #f8faf9;
        color: #46564e;
    }

    .informacoes p {
        margin: 7px 0;
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
        min-width: 750px;
        border-collapse: collapse;
    }

    th, td {
        text-align: left;
        padding: 14px 12px;
        border-bottom: 1px solid #edf0ee;
        font-size: 14px;
    }

    th {
        background: #f8faf9;
        color: #53645b;
    }

    .acoes {
        display: flex;
        gap: 8px;
    }

    .botao-presente {
        background: #e4f4e9;
        color: #236b50;
    }

    .botao-ausente {
        background: #fbe9e9;
        color: #b83a3a;
    }

    .confirmacao {
        color: #53645b;
    }

    .presente {
        color: #236b50;
        font-weight: 600;
    }

    .ausente {
        color: #b83a3a;
        font-weight: 600;
    }

    .pendente {
        color: #8a7540;
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

        .cabecalho {
            align-items: stretch;
            flex-direction: column;
        }
    }
</style>
