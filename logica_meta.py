import random
from datetime import datetime, timedelta
from gerenciador_dados import GerenciadorDeDados
from usuario import Usuario
from validadores import ValidadorDeFormato, enviar_email

class MetacashLogica:
    """Contém toda a lógica de negócio do Metacash."""
    def __init__(self):
        self.gerenciador = GerenciadorDeDados()
        self.usuario_logado: Usuario | None = None
        self.usuario_pendente_2fa: Usuario | None = None

    def processar_login(self, nome_usuario: str, senha_texto_plano: str) -> tuple[bool, str]:
        """Valida credenciais e dispara o envio do código 2FA."""
        usuario = self.gerenciador.encontrar_usuario(nome_usuario)
        if usuario and usuario.verificar_senha(senha_texto_plano):
            sucesso_envio, mensagem_envio = self._iniciar_verificacao_2fa(usuario)
            if sucesso_envio:
                self.usuario_pendente_2fa = usuario
                return (True, mensagem_envio)
            else:
                return (False, mensagem_envio)
        return (False, "Usuário ou senha incorretos.")

    def _iniciar_verificacao_2fa(self, usuario: Usuario) -> tuple[bool, str]:
        """Gera, armazena e envia o código 2FA."""
        codigo = str(random.randint(100000, 999999))
        usuario.codigo_2fa = codigo
        usuario.codigo_2fa_expiracao = datetime.now() + timedelta(minutes=5)
        assunto = "Seu Código de Verificação Metacash"
        corpo = f"Olá!\n\nSeu código de verificação é: {codigo}\n\nEle expira em 5 minutos."
        print(f"[DEBUG] Gerando código {codigo} para {usuario.email}")
        if enviar_email(usuario.email, assunto, corpo):
            return (True, f"Código de verificação enviado para {usuario.email}.")
        else:
            return (False, "Houve um erro ao enviar o email de verificação.")
            
    def verificar_codigo_2fa(self, codigo_fornecido: str) -> tuple[bool, str]:
        """Valida o código 2FA fornecido."""
        usuario = self.usuario_pendente_2fa
        if not usuario or not usuario.codigo_2fa or datetime.now() > usuario.codigo_2fa_expiracao:
            return (False, "Código expirado ou inválido. Tente fazer o login novamente.")
        if usuario.codigo_2fa == codigo_fornecido:
            usuario.codigo_2fa = None
            usuario.codigo_2fa_expiracao = None
            self.usuario_logado = usuario
            self.usuario_pendente_2fa = None
            return (True, "Login realizado com sucesso!")
        else:
            return (False, "Código de verificação incorreto.")
    
    def processar_cadastro(self, nome_usuario: str, email: str, senha: str, confirmacao_senha: str) -> tuple[bool, str | Usuario]:
        """Valida e cria um novo usuário, incluindo validações de formato."""
        if not all([nome_usuario, email, senha, confirmacao_senha]): 
            return (False, "Todos os campos são obrigatórios.")
        sucesso_senha, msg_senha = ValidadorDeFormato.validacao_senha(senha)
        if not sucesso_senha: 
            return (False, msg_senha)
        if senha != confirmacao_senha: 
            return (False, "As senhas não correspondem.")
        if not ValidadorDeFormato.email_tem_dominio_valido(email): 
            return (False, "O domínio do email é inválido ou não é permitido.")
        if self.gerenciador.encontrar_usuario(nome_usuario): 
            return (False, "Este nome de usuário já está em uso.")
        if self.gerenciador.email_existe(email): 
            return (False, "Este email já está cadastrado.")
        
        novo_usuario = Usuario(nome_usuario, senha, email)
        self.gerenciador.salvar_usuario(novo_usuario)
        return (True, novo_usuario)
        
    def salvar_preferencias_financeiras(self, salario: float, gastos_fixos: float, preferencias: dict) -> tuple[bool, str]:
        """Valida e armazena o perfil financeiro do usuário logado."""
        if not self.usuario_logado: 
            return (False, "Nenhum usuário logado.")
        if not ValidadorDeFormato.validacao_de_valor_monetario(salario) or not ValidadorDeFormato.validacao_de_valor_monetario(gastos_fixos): 
            return (False, "Salário e gastos fixos devem ser valores numéricos positivos.")
        for categoria, valor in preferencias.items():
            if not ValidadorDeFormato.validacao_preferencias_gastos(valor): 
                return (False, f"Valor de prioridade para '{categoria}' é inválido. Deve ser um inteiro de 1 a 5.")
        
        self.usuario_logado.salario = float(salario)
        self.usuario_logado.gastos_fixos = float(gastos_fixos)
        self.usuario_logado.preferencias_gastos = preferencias
        self.gerenciador.salvar_usuario(self.usuario_logado)
        return (True, "Dados e preferências financeiras salvos com sucesso!")
        
    def alterar_dado_usuario(self, tipo_dado: str, novo_valor: str) -> tuple[bool, str]:
        """Altera um dado do usuário logado (nome de usuário ou email)."""
        if not self.usuario_logado:
            return (False, "Nenhum usuário logado.")
        if tipo_dado == "email":
            if self.gerenciador.email_existe(novo_valor): 
                return (False, "Este email já está em uso por outra conta.")
            if not ValidadorDeFormato.email_tem_dominio_valido(novo_valor): 
                return (False, "O novo email possui um domínio inválido.")
            self.usuario_logado.email = novo_valor
            self.gerenciador.salvar_usuario(self.usuario_logado)
            return (True, "Email alterado com sucesso!")
        elif tipo_dado == "nome_usuario":
            if self.gerenciador.encontrar_usuario(novo_valor): 
                return (False, "Este nome de usuário já está em uso.")
            nome_antigo = self.usuario_logado.nome_usuario
            self.usuario_logado.nome_usuario = novo_valor
            self.gerenciador.salvar_usuario(self.usuario_logado)
            self.gerenciador.deletar_usuario(nome_antigo)
            return (True, "Nome de usuário alterado com sucesso!")
        else:
            return (False, "Este tipo de dado não pode ser alterado por esta função.")

    def alterar_senha(self, nova_senha: str, confirmacao_senha: str) -> tuple[bool, str]:
        """Altera a senha do usuário logado após validação."""
        if not self.usuario_logado: 
            return (False, "Nenhum usuário logado.")
        sucesso, msg = ValidadorDeFormato.validacao_senha(nova_senha)
        if not sucesso: 
            return (False, msg)
        if nova_senha != confirmacao_senha: 
            return (False, "As senhas não correspondem.")
        self.usuario_logado.senha = nova_senha
        self.gerenciador.salvar_usuario(self.usuario_logado)
        return (True, "Senha alterada com sucesso!")
         