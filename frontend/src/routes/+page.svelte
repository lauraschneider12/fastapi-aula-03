
<script lang="ts">
    const destaques = [
        {
            numero: '01',
            titulo: 'Nosso elenco',
            descricao: 'Conheça as atletas que representam o clube.',
            link: '/elencos',
            acao: 'Conhecer o elenco'
        },
        {
            numero: '02',
            titulo: 'Agenda esportiva',
            descricao: 'Acompanhe os próximos confrontos e resultados.',
            link: '/agenda',
            acao: 'Ver calendário'
        }
    ];

    const valores = [
        {
            numero: '01',
            titulo: 'Compromisso',
            descricao: 'Dedicação diária dentro e fora das quadras.'
        },
        {
            numero: '02',
            titulo: 'Coletividade',
            descricao: 'Cada atleta faz parte de algo maior.'
        },
        {
            numero: '03',
            titulo: 'Desenvolvimento',
            descricao: 'Evolução esportiva construída em equipe.'
        }
    ];
</script>

<svelte:head>
    <title>Futsal Feminino | Nosso Clube</title>
    <meta
        name="description"
        content="Conheça nosso clube de futsal feminino, acompanhe o elenco e confira a agenda de jogos."
    />
    <meta name="theme-color" content="#081426" />
</svelte:head>

<div class="site">
    <header class="topbar">
        <a class="brand" href="/" aria-label="Página inicial">
            <span class="brand-symbol">F<span>.</span></span>
            <span class="brand-copy">
                <strong>FUTSAL</strong>
                <small>CLUBE FEMININO</small>
            </span>
        </a>

        <nav aria-label="Navegação principal">
            <a class="nav-active" href="/">Início</a>
            <a href="#sobre">O clube</a>
            <a href="/elencos">Elenco</a>
            <a href="/agenda">Agenda</a>
        </nav>

        <a class="header-cta" href="/login">
            Entrar <span>↗</span>
        </a>
    </header>

    <main>
        <section class="hero">
            <div class="hero-content">
                <div class="eyebrow">
                    <span class="status-dot"></span>
                    FUTSAL FEMININO · ESPÍRITO DE EQUIPE
                </div>

                <h1>
                    FORÇA QUE<br />
                    <span>JOGA JUNTO.</span>
                </h1>

                <p class="hero-description">
                    Mais do que um esporte, uma equipe que cresce,
                    compete e constrói sua história dentro das quadras.
                </p>

                <div class="hero-actions">
                    <a class="button-primary" href="/elencos">
                        Conheça o elenco <span>↗</span>
                    </a>
                    <a class="button-secondary" href="/agenda">
                        Explorar agenda <span>→</span>
                    </a>
                </div>

                <div class="hero-footnote">
                    <span class="footnote-line"></span>
                    TALENTO · DISCIPLINA · COLETIVIDADE
                </div>
            </div>

            <div class="court-art" aria-label="Ilustração gráfica de uma quadra de futsal">
                <div class="court-label">O JOGO COMEÇA AQUI</div>

                <div class="court">
                    <div class="court-center"></div>
                    <div class="center-circle"></div>
                    <div class="center-dot"></div>

                    <div class="area area-left"></div>
                    <div class="area area-right"></div>

                    <div class="goal goal-left"></div>
                    <div class="goal goal-right"></div>

                    <div class="court-mark mark-one"></div>
                    <div class="court-mark mark-two"></div>
                </div>

                <div class="art-caption">
                    <span>01 / IDENTIDADE</span>
                    <span>QUADRA · EQUIPE · HISTÓRIA</span>
                </div>

                <div class="art-number" aria-hidden="true">F</div>
            </div>

            <div class="hero-index" aria-hidden="true">01 — 03</div>
        </section>

        <section class="principles" aria-label="Princípios do clube">
            <div class="principle-intro">NOSSA ESSÊNCIA</div>
            <div class="principle-item">
                <span>01</span>
                <strong>Talento</strong>
            </div>
            <div class="principle-item">
                <span>02</span>
                <strong>Disciplina</strong>
            </div>
            <div class="principle-item">
                <span>03</span>
                <strong>União</strong>
            </div>
            <div class="principle-note">UMA EQUIPE. UM PROPÓSITO.</div>
        </section>

        <section class="about section-wrap" id="sobre">
            <div class="section-heading">
                <span class="eyebrow">01 / QUEM SOMOS</span>
                <h2>UMA PAIXÃO.<br />MUITOS <span>OBJETIVOS.</span></h2>
            </div>

            <div class="about-copy">
                <p>
                    Acreditamos na força do esporte para desenvolver
                    talentos, fortalecer vínculos e abrir caminhos para
                    o futsal feminino.
                </p>
                <p>
                    Cada treino, cada partida e cada conquista fazem
                    parte de uma história construída coletivamente.
                </p>
                <a class="text-link" href="/elencos">
                    Conheça nossas atletas <span>↗</span>
                </a>
            </div>
        </section>

        <section class="features">
            {#each destaques as destaque}
                <a class="feature-card" href={destaque.link}>
                    <div class="feature-top">
                        <span>{destaque.numero} / CLUBE</span>
                        <span class="feature-arrow">↗</span>
                    </div>

                    <div class="feature-content">
                        <h3>{destaque.titulo}</h3>
                        <p>{destaque.descricao}</p>
                    </div>

                    <div class="feature-bottom">
                        <span>{destaque.acao}</span>
                        <span>→</span>
                    </div>
                </a>
            {/each}
        </section>

        <section class="values section-wrap">
            <div class="values-heading">
                <span class="eyebrow">02 / O QUE NOS MOVE</span>
                <h2>MAIS QUE JOGO.<br /><span>É PROPÓSITO.</span></h2>
            </div>

            <div class="values-list">
                {#each valores as valor}
                    <article class="value-item">
                        <span class="value-number">{valor.numero}</span>
                        <div>
                            <h3>{valor.titulo}</h3>
                            <p>{valor.descricao}</p>
                        </div>
                        <span class="value-symbol">↗</span>
                    </article>
                {/each}
            </div>
        </section>

        <section class="closing">
            <span class="eyebrow">NOSSO PRÓXIMO CAPÍTULO</span>
            <h2>A NOSSA HISTÓRIA<br />CONTINUA <span>EM QUADRA.</span></h2>
            <p>Acompanhe os jogos e conheça quem faz parte dessa jornada.</p>

            <div class="closing-actions">
                <a class="button-primary" href="/agenda">
                    Ver agenda de jogos <span>↗</span>
                </a>
                <a class="button-secondary" href="/elencos">
                    Conhecer elenco <span>→</span>
                </a>
            </div>

            <div class="closing-decoration" aria-hidden="true">F.</div>
        </section>
    </main>

    <footer class="footer">
        <a class="brand footer-brand" href="/">
            <span class="brand-symbol">F<span>.</span></span>
            <span class="brand-copy">
                <strong>FUTSAL</strong>
                <small>CLUBE FEMININO</small>
            </span>
        </a>

        <p>Paixão pelo esporte. Orgulho de representar.</p>

        <div class="footer-links">
            <a href="/">Início</a>
            <a href="/elencos">Elenco</a>
            <a href="/agenda">Agenda</a>
        </div>

        <span class="copyright">© {new Date().getFullYear()} · TODOS OS DIREITOS RESERVADOS</span>
    </footer>
</div>

<style>
    :global(*) {
        box-sizing: border-box;
    }

    :global(html) {
        scroll-behavior: smooth;
        scroll-padding-top: 90px;
    }

    :global(body) {
        margin: 0;
        background: #081426;
        color: #f2f5fa;
        font-family: Arial, Helvetica, sans-serif;
    }

    :global(body)::selection {
        background: #8bbcff;
        color: #081426;
    }

    :global(a) {
        color: inherit;
        text-decoration: none;
    }

    .site {
        min-height: 100vh;
        overflow: hidden;
        background: #081426;
    }

    .topbar {
        min-height: 88px;
        padding: 0 7%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 28px;
        border-bottom: 1px solid #23334a;
        background: #081426;
    }

    .brand {
        display: inline-flex;
        align-items: center;
        gap: 11px;
        flex-shrink: 0;
    }

    .brand-symbol {
        display: grid;
        place-items: center;
        width: 43px;
        height: 43px;
        border: 1px solid #638dc3;
        font-size: 27px;
        font-weight: 900;
        letter-spacing: -3px;
    }

    .brand-symbol span,
    .brand-copy small {
        color: #76aef5;
    }

    .brand-copy {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .brand-copy strong {
        font-size: 15px;
        letter-spacing: 2px;
    }

    .brand-copy small {
        font-size: 9px;
        letter-spacing: 1.7px;
    }

    nav {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 32px;
    }

    nav a {
        color: #aab8ca;
        font-size: 12px;
        transition: color 0.2s;
    }

    nav a:hover,
    nav .nav-active {
        color: #ffffff;
    }

    nav .nav-active::after {
        display: block;
        width: 16px;
        height: 2px;
        margin-top: 8px;
        background: #76aef5;
        content: '';
    }

    .header-cta {
        padding: 13px 16px;
        border: 1px solid #3b526e;
        font-size: 11px;
        white-space: nowrap;
        transition: background 0.2s;
    }

    .header-cta span {
        margin-left: 12px;
        color: #76aef5;
    }

    .header-cta:hover {
        background: #142a45;
    }

    .hero {
        position: relative;
        display: grid;
        grid-template-columns: 1fr 0.92fr;
        align-items: center;
        gap: 35px;
        min-height: 610px;
        padding: 75px 9% 85px;
        background:
            radial-gradient(ellipse at 83% 48%, #122a48 0%, transparent 43%),
            #0b192d;
        border-bottom: 1px solid #24364d;
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    .eyebrow {
        color: #83b6f7;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2.2px;
        line-height: 1.8;
    }

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        margin-right: 8px;
        border-radius: 50%;
        background: #83b6f7;
        vertical-align: middle;
    }

    .hero h1 {
        margin: 30px 0 22px;
        font-size: clamp(46px, 6vw, 80px);
        line-height: 0.99;
        font-weight: 900;
        letter-spacing: -4px;
    }

    .hero h1 span {
        color: #82b5f6;
    }

    .hero-description {
        max-width: 430px;
        color: #b1bfd0;
        font-size: 14px;
        line-height: 1.9;
    }

    .hero-actions,
    .closing-actions {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 13px;
        margin-top: 32px;
    }

    .button-primary,
    .button-secondary {
        min-height: 48px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 0 18px;
        font-size: 11px;
        font-weight: 700;
        transition: transform 0.2s, background 0.2s;
    }

    .button-primary {
        background: #82b5f6;
        color: #081426;
    }

    .button-primary:hover {
        background: #b0d1ff;
        transform: translateY(-2px);
    }

    .button-secondary {
        border: 1px solid #364d68;
        color: #f2f5fa;
    }

    .button-secondary:hover {
        background: #142a45;
    }

    .hero-footnote {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 53px;
        color: #8b9bb0;
        font-size: 9px;
        letter-spacing: 1.5px;
    }

    .footnote-line {
        width: 30px;
        height: 1px;
        background: #82b5f6;
    }

    .court-art {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 0;
        min-height: 360px;
    }

    .court-label,
    .art-caption {
        position: absolute;
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        gap: 12px;
        color: #8ba3c0;
        font-size: 8px;
        letter-spacing: 1.7px;
    }

    .court-label {
        top: 12px;
    }

    .art-caption {
        bottom: 7px;
    }

    .court {
        position: relative;
        width: 100%;
        max-width: 390px;
        aspect-ratio: 1.08 / 1;
        overflow: hidden;
        border: 1px solid #59799f;
        background:
            linear-gradient(90deg, transparent 49.8%, #496b91 50%, transparent 50.2%),
            #0d2038;
        transform: rotate(-5deg);
        box-shadow: 0 30px 80px #03091455;
    }

    .court::before {
        position: absolute;
        inset: 9%;
        border: 1px solid #496b91;
        content: '';
    }

    .court-center {
        position: absolute;
        top: 9%;
        bottom: 9%;
        left: 50%;
        width: 1px;
        background: #496b91;
    }

    .center-circle {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 30%;
        aspect-ratio: 1;
        border: 1px solid #6387b0;
        border-radius: 50%;
        transform: translate(-50%, -50%);
    }

    .center-dot {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #82b5f6;
        transform: translate(-50%, -50%);
    }

    .area {
        position: absolute;
        top: 29%;
        width: 17%;
        height: 42%;
        border: 1px solid #496b91;
    }

    .area-left {
        left: 9%;
        border-left: 0;
    }

    .area-right {
        right: 9%;
        border-right: 0;
    }

    .goal {
        position: absolute;
        top: 41%;
        width: 4%;
        height: 18%;
        border: 1px solid #82b5f6;
    }

    .goal-left {
        left: 5%;
        border-left: 0;
    }

    .goal-right {
        right: 5%;
        border-right: 0;
    }

    .court-mark {
        position: absolute;
        width: 9px;
        height: 9px;
        border: 1px solid #82b5f6;
        border-radius: 50%;
    }

    .mark-one {
        top: 38%;
        left: 23%;
    }

    .mark-two {
        right: 23%;
        bottom: 38%;
    }

    .art-number {
        position: absolute;
        right: 1%;
        bottom: 3%;
        z-index: 0;
        color: #29476b;
        font-size: 105px;
        font-weight: 900;
        opacity: 0.23;
    }

    .hero-index {
        position: absolute;
        right: 3%;
        bottom: 28px;
        color: #7c8da3;
        font-size: 9px;
        letter-spacing: 2px;
    }

    .principles {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 25px;
        padding: 25px 9%;
        border-bottom: 1px solid #24364d;
        background: #0a1729;
    }

    .principle-intro,
    .principle-note {
        color: #8295ad;
        font-size: 9px;
        letter-spacing: 1.5px;
    }

    .principle-item {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .principle-item span {
        color: #82b5f6;
        font-size: 10px;
    }

    .principle-item strong {
        font-size: 12px;
        font-weight: 500;
    }

    .section-wrap {
        padding: 100px 12%;
    }

    .about {
        display: grid;
        grid-template-columns: 1fr 0.85fr;
        align-items: start;
        gap: 80px;
        background: #0b192d;
    }

    .section-heading h2,
    .values-heading h2 {
        margin: 20px 0 0;
        font-size: clamp(35px, 4.4vw, 54px);
        line-height: 1.08;
        letter-spacing: -2px;
    }

    .section-heading h2 span,
    .values-heading h2 span {
        color: #82b5f6;
    }

    .about-copy p {
        margin: 0 0 20px;
        color: #aab8ca;
        font-size: 13px;
        line-height: 2;
    }

    .text-link {
        display: inline-flex;
        align-items: center;
        gap: 20px;
        margin-top: 10px;
        padding-bottom: 9px;
        border-bottom: 1px solid #82b5f6;
        font-size: 11px;
        font-weight: 700;
    }

    .text-link span {
        color: #82b5f6;
    }

    .features {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px;
        padding: 0 12% 100px;
        background: #0b192d;
    }

    .feature-card {
        min-height: 245px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 25px;
        border: 1px solid #2b415c;
        background:
            linear-gradient(140deg, #142a45, #0b192d 70%);
        transition: border-color 0.2s, transform 0.2s;
    }

    .feature-card:hover {
        border-color: #82b5f6;
        transform: translateY(-3px);
    }

    .feature-top,
    .feature-bottom {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }

    .feature-top {
        color: #8ca3bf;
        font-size: 9px;
        letter-spacing: 1.5px;
    }

    .feature-arrow {
        color: #82b5f6;
        font-size: 20px;
    }

    .feature-content h3 {
        margin: 0 0 10px;
        font-size: 27px;
        letter-spacing: -0.7px;
    }

    .feature-content p {
        max-width: 300px;
        margin: 0;
        color: #aab8ca;
        font-size: 12px;
        line-height: 1.8;
    }

    .feature-bottom {
        padding-top: 18px;
        border-top: 1px solid #2b415c;
        color: #c7d8ec;
        font-size: 10px;
    }

    .feature-bottom span:last-child {
        color: #82b5f6;
        font-size: 17px;
    }

    .values {
        display: grid;
        grid-template-columns: 0.8fr 1fr;
        gap: 80px;
        background: #081426;
    }

    .values-list {
        border-top: 1px solid #293b52;
    }

    .value-item {
        display: grid;
        grid-template-columns: 34px 1fr 20px;
        align-items: center;
        gap: 16px;
        padding: 22px 0;
        border-bottom: 1px solid #293b52;
    }

    .value-number {
        align-self: start;
        padding-top: 3px;
        color: #82b5f6;
        font-size: 10px;
    }

    .value-item h3 {
        margin: 0 0 7px;
        font-size: 16px;
    }

    .value-item p {
        margin: 0;
        color: #9eafc3;
        font-size: 11px;
        line-height: 1.7;
    }

    .value-symbol {
        color: #82b5f6;
    }

    .closing {
        position: relative;
        overflow: hidden;
        padding: 80px 12%;
        border-top: 1px solid #2b415c;
        border-bottom: 1px solid #2b415c;
        background:
            radial-gradient(ellipse at 80% 50%, #1b3a5f 0%, transparent 50%),
            #10213a;
    }

    .closing h2 {
        position: relative;
        z-index: 1;
        margin: 22px 0 16px;
        font-size: clamp(35px, 5vw, 60px);
        line-height: 1.06;
        letter-spacing: -2px;
    }

    .closing h2 span {
        color: #82b5f6;
    }

    .closing > p {
        position: relative;
        z-index: 1;
        color: #afc0d5;
        font-size: 13px;
        line-height: 1.8;
    }

    .closing-actions {
        position: relative;
        z-index: 1;
    }

    .closing-decoration {
        position: absolute;
        top: -100px;
        right: 4%;
        color: #42648d;
        font-size: 360px;
        line-height: 1;
        font-weight: 900;
        opacity: 0.12;
        pointer-events: none;
    }

    .footer {
        display: grid;
        grid-template-columns: 1fr 1.4fr 1fr;
        align-items: center;
        gap: 25px;
        padding: 35px 7%;
        background: #081426;
    }

    .footer > p {
        color: #8fa2ba;
        font-size: 11px;
        text-align: center;
    }

    .footer-links {
        display: flex;
        justify-content: flex-end;
        gap: 18px;
    }

    .footer-links a {
        color: #aab8ca;
        font-size: 10px;
    }

    .footer-links a:hover {
        color: #82b5f6;
    }

    .copyright {
        grid-column: 1 / -1;
        padding-top: 20px;
        border-top: 1px solid #23334a;
        color: #71849c;
        font-size: 8px;
        letter-spacing: 1.3px;
    }

    @media (min-width: 1500px) {
        .hero {
            padding-right: 13%;
            padding-left: 13%;
        }
    }

    @media (max-width: 1000px) {
        .topbar {
            padding-right: 5%;
            padding-left: 5%;
            gap: 18px;
        }

        nav {
            gap: 18px;
        }

        .hero {
            padding-right: 6%;
            padding-left: 6%;
        }

        .section-wrap {
            padding-right: 8%;
            padding-left: 8%;
        }

        .features {
            padding-right: 8%;
            padding-left: 8%;
        }

        .about,
        .values {
            gap: 45px;
        }

        .principles {
            padding-right: 6%;
            padding-left: 6%;
        }

        .principle-note {
            display: none;
        }
    }

    @media (max-width: 720px) {
        .topbar {
            padding: 20px 6%;
            flex-wrap: wrap;
        }

        nav {
            order: 3;
            width: 100%;
            justify-content: space-between;
            gap: 10px;
        }

        .header-cta {
            margin-left: auto;
        }

        .hero {
            grid-template-columns: 1fr;
            gap: 25px;
            padding: 65px 7% 60px;
        }

        .hero h1 {
            font-size: clamp(47px, 10vw, 70px);
            letter-spacing: -2.5px;
        }

        .hero-footnote {
            margin-top: 35px;
        }

        .court-art {
            min-height: 320px;
            margin-top: 10px;
        }

        .court {
            max-width: 340px;
        }

        .hero-index {
            right: 7%;
            bottom: 15px;
        }

        .principles {
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
            padding: 24px 7%;
        }

        .principle-intro {
            width: 100%;
        }

        .principle-item {
            gap: 7px;
        }

        .principle-item strong {
            font-size: 11px;
        }

        .section-wrap {
            padding: 70px 7%;
        }

        .about,
        .values {
            grid-template-columns: 1fr;
            gap: 35px;
        }

        .features {
            grid-template-columns: 1fr;
            padding: 0 7% 70px;
        }

        .feature-card {
            min-height: 220px;
        }

        .closing {
            padding: 65px 7%;
        }

        .closing-decoration {
            right: -10%;
            font-size: 240px;
        }

        .footer {
            grid-template-columns: 1fr;
            padding: 30px 7%;
            gap: 18px;
        }

        .footer > p {
            text-align: left;
        }

        .footer-links {
            justify-content: flex-start;
        }

        .copyright {
            grid-column: auto;
        }
    }

    @media (max-width: 420px) {
        .brand-copy strong {
            font-size: 13px;
        }

        .brand-copy small {
            font-size: 8px;
        }

        .header-cta {
            padding: 11px;
            font-size: 10px;
        }

        .hero-actions,
        .closing-actions {
            align-items: stretch;
            flex-direction: column;
        }

        .button-primary,
        .button-secondary {
            justify-content: space-between;
        }

        .court-art {
            min-height: 270px;
        }

        .art-caption {
            font-size: 7px;
        }

        .section-heading h2,
        .values-heading h2 {
            font-size: 36px;
        }

        .closing h2 {
            font-size: 35px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        :global(html) {
            scroll-behavior: auto;
        }

        *,
        *::before,
        *::after {
            transition-duration: 0.01ms !important;
        }
    }
</style>
