import smtplib
import os
from email.message import EmailMessage

class ValidadorDeFormato:
    """Classe de utilidades com métodos estáticos para validar o formato de dados."""
    DOMINIOS_VALIDOS = ("@gmail.com", "@hotmail.com", "@yahoo.com.br", "@outlook.com")

    @staticmethod
    def email_tem_dominio_valido(email: str) -> bool:
        if isinstance(email, str):
            return email.lower().endswith(ValidadorDeFormato.DOMINIOS_VALIDOS)
        return False

    @staticmethod
    def validacao_senha(senha: str) -> tuple[bool, str]:
        """Faz as veirifcações para saber se a senha está de acordo com os parâmetros especificados"""
        if not isinstance(senha, str): 
            return (False, "Senha em formato inválido.")
        if len(senha) < 8: 
            return (False, "A senha precisa ter no mínimo 8 caracteres.")
        if not any(c.isalpha() for c in senha): 
            return (False, "A senha deve conter pelo menos uma letra.")
        if not any(c.isdigit() for c in senha): 
            return (False, "A senha precisa ter pelo menos um número.")
        return (True, "Senha forte.")

    @staticmethod
    def validacao_de_valor_monetario(valor) -> bool:
        """Verifica se um valor monetario é maior que 0 e está em float"""
        try:
            return float(valor) >= 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validacao_preferencias_gastos(valor) -> bool:
        """Verifica se o número da preferencia de gastos está entre 1 e 5 e se está em int"""
        try:
            return 1 <= int(valor) <= 5
        except (ValueError, TypeError):
            return False

def enviar_email(destinatario: str, assunto: str, corpo: str) -> bool:
    """Envia um email usando as credenciais das variáveis de ambiente."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("SENHA_APP_EMAIL")

    if not remetente or not senha_app:
        print("[ERRO DE SISTEMA] Variáveis de ambiente para envio de e-mail não configuradas.")
        return False

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha_app)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"[ERRO DE SISTEMA] Falha ao enviar o email: {e}")
        return False