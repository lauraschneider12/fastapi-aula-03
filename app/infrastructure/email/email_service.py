
import os
import aiosmtplib

from email.message import EmailMessage


async def enviar_credenciais(
    email_destinatario: str,
    senha: str,
):
    remetente = os.getenv("GMAIL_EMAIL")
    senha_app = os.getenv("GMAIL_APP_PASSWORD")

    if not remetente or not senha_app:
        raise RuntimeError(
            "Configurações do Gmail não encontradas."
        )

    mensagem = EmailMessage()
    mensagem["From"] = remetente
    mensagem["To"] = email_destinatario
    mensagem["Subject"] = "Seu acesso ao sistema"

    mensagem.set_content(
        f"""
Olá!

Seu cadastro como atleta foi realizado com sucesso.

Seus dados de acesso são:

E-mail: {email_destinatario}
Senha: {senha}

Recomendamos alterar sua senha após o primeiro acesso.

Atenciosamente,
Equipe do sistema.
"""
    )

    await aiosmtplib.send(
        mensagem,
        hostname="smtp.gmail.com",
        port=465,
        username=remetente,
        password=senha_app,
        use_tls=True,
    )