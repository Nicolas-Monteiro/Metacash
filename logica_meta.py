import random
from datetime import datetime, timedelta
from gerenciador_dados import GerenciadorDeDados
from usuario import Usuario, Meta
from validadores import ValidadorDeFormato, enviar_email

class MetacashLogica:
    def __init__(self):
        
        self.gerenciador = GerenciadorDeDados()
        self.usuario_logado: Usuario | None = None
        self.usuario_pendente_2fa: Usuario | None = None

    def processar_login(self, nome_usuario: str, senha_texto_plano: str) -> tuple[bool, str, bool]:
       
        usuario = self.gerenciador.encontrar_usuario(nome_usuario)
        if usuario and usuario.verificar_senha(senha_texto_plano):
            if usuario.verificado:
                self.usuario_logado = usuario
                return (True, "Login bem-sucedido!", False)
            else:
                sucesso_envio, mensagem_envio = self._iniciar_verificacao_2fa(usuario)
                if sucesso_envio:
                    self.usuario_pendente_2fa = usuario
                    return (True, mensagem_envio, True)
                else:
                    return (False, mensagem_envio, False)
        return (False, "Utilizador ou senha incorretos.", False)

    def verificar_codigo_2fa(self, codigo_fornecido: str) -> tuple[bool, str]:
       
        usuario_a_verificar = self.usuario_pendente_2fa
        if not usuario_a_verificar or not usuario_a_verificar.codigo_2fa or datetime.now() > usuario_a_verificar.codigo_2fa_expiracao:
            self.usuario_pendente_2fa = None
            return (False, "Código expirado ou inválido. Tente o processo novamente.")
        if usuario_a_verificar.codigo_2fa == codigo_fornecido:
            usuario_a_verificar.codigo_2fa = None
            usuario_a_verificar.codigo_2fa_expiracao = None
            if not usuario_a_verificar.verificado:
                usuario_a_verificar.verificado = True
                self.gerenciador.salvar_usuario(usuario_a_verificar)
            self.usuario_logado = usuario_a_verificar
            self.usuario_pendente_2fa = None
            return (True, "Verificação bem-sucedida!")
        else:
            return (False, "Código de verificação incorreto.")

    def iniciar_2fa_para_edicao(self):
       
        if not self.usuario_logado:
            return False, "Nenhum usuário logado."
        self.usuario_pendente_2fa = self.usuario_logado
        return self._iniciar_verificacao_2fa(self.usuario_logado)

    def deletar_conta_logado(self) -> tuple[bool, str]:
        
        if not self.usuario_logado:
            return (False, "Nenhum usuário logado para deletar.")
        nome_usuario_para_deletar = self.usuario_logado.nome_usuario
        sucesso_delecao = self.gerenciador.deletar_usuario(nome_usuario_para_deletar)
        if sucesso_delecao:
            self.usuario_logado = None
            return (True, "Conta deletada com sucesso.")
        else:
            return (False, "Ocorreu um erro ao tentar deletar a conta.")

    def atualizar_dados_usuario(self, novos_dados: dict) -> tuple[bool, str]:
       
        if not self.usuario_logado:
            return False, "Nenhum usuário logado."
        novo_nome = novos_dados.get("nome_usuario")
        novo_email = novos_dados.get("email")
        if self.usuario_logado.nome_usuario.lower() != novo_nome.lower() and self.gerenciador.encontrar_usuario(novo_nome):
            return False, "Este nome de usuário já está em uso."
        if self.usuario_logado.email.lower() != novo_email.lower() and self.gerenciador.email_existe(novo_email):
            return False, "Este e-mail já está em uso."
        if not ValidadorDeFormato.email_tem_dominio_valido(novo_email):
            return False, "O novo e-mail possui um domínio inválido."
        nome_antigo = self.usuario_logado.nome_usuario
        self.usuario_logado.nome_usuario = novo_nome
        self.usuario_logado.email = novo_email
        self.usuario_logado.salario = float(str(novos_dados.get("salario", 0.0)).replace(",", "."))
        self.usuario_logado.gastos_fixos = float(str(novos_dados.get("gastos_fixos", 0.0)).replace(",", "."))
        self.usuario_logado.gastos_alimentacao = float(str(novos_dados.get("gastos_alimentacao", 0.0)).replace(",", "."))
        self.usuario_logado.gastos_transporte = float(str(novos_dados.get("gastos_transporte", 0.0)).replace(",", "."))
        self.usuario_logado.gastos_lazer = float(str(novos_dados.get("gastos_lazer", 0.0)).replace(",", "."))
        self.gerenciador.salvar_usuario(self.usuario_logado)
        if nome_antigo.lower() != novo_nome.lower():
            self.gerenciador.deletar_usuario(nome_antigo)
        return True, "Dados atualizados com sucesso!"
    
    def _iniciar_verificacao_2fa(self, usuario: Usuario) -> tuple[bool, str]:
       
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
            
    def processar_cadastro(self, nome_usuario: str, email: str, senha: str, confirmacao_senha: str) -> tuple[bool, str | Usuario]:
        
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
        
    def salvar_preferencias_financeiras(self, salario: float, gastos_fixos: float, gastos_alimentacao: float, gastos_transporte: float, gastos_lazer: float, preferencias: dict) -> tuple[bool, str]:
       
        if not self.usuario_logado: 
            return (False, "Nenhum usuário logado.")
        valores_a_validar = [salario, gastos_fixos, gastos_alimentacao, gastos_transporte, gastos_lazer]
        if not all(ValidadorDeFormato.validacao_de_valor_monetario(v) for v in valores_a_validar):
            return (False, "Todos os campos financeiros devem ser valores numéricos positivos.")
        for categoria, valor in preferencias.items():
            if not ValidadorDeFormato.validacao_preferencias_gastos(valor): 
                return (False, f"Valor de prioridade para '{categoria}' é inválido. Deve ser um inteiro de 1 a 5.")
        self.usuario_logado.salario = float(salario)
        self.usuario_logado.gastos_fixos = float(gastos_fixos)
        self.usuario_logado.gastos_alimentacao = float(gastos_alimentacao)
        self.usuario_logado.gastos_transporte = float(gastos_transporte)
        self.usuario_logado.gastos_lazer = float(gastos_lazer)
        self.usuario_logado.preferencias_gastos = preferencias
        self.gerenciador.salvar_usuario(self.usuario_logado)
        return (True, "Dados e preferências financeiras salvos com sucesso!")

    def alterar_senha(self, nova_senha: str, confirmacao_senha: str) -> tuple[bool, str]:
       
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
   
    def analisar_realismo_meta(self, valor_meta: float, prazo_dias: int) -> tuple[bool, str]:
        """Verifica se a meta é realista com base na renda disponível mensal."""
        if not self.usuario_logado or prazo_dias <= 0:
            return False, "Dados insuficientes para análise."
        
        gastos_variaveis = self.usuario_logado.gastos_alimentacao + self.usuario_logado.gastos_transporte + self.usuario_logado.gastos_lazer
        renda_disponivel_mensal = self.usuario_logado.salario - self.usuario_logado.gastos_fixos - gastos_variaveis
        
        if renda_disponivel_mensal <= 0:
            return False, "Seus gastos atuais excedem seu salário. A meta não é realista."
        
        meses_necessarios = prazo_dias / 30.0
        poupanca_mensal_necessaria = valor_meta / meses_necessarios

        if poupanca_mensal_necessaria > renda_disponivel_mensal:
            return False, f"Não realista. Você precisa guardar R$ {poupanca_mensal_necessaria:.2f}/mês, mas sua renda disponível é de R$ {renda_disponivel_mensal:.2f}/mês."
        
        return True, f"Meta realista! Você precisa guardar R$ {poupanca_mensal_necessaria:.2f} por mês."

    def definir_meta(self, nome: str, valor_total: float, prazo_dias: int) -> tuple[bool, str]:
        """Define ou atualiza a meta do usuário."""
        if not self.usuario_logado:
            return False, "Nenhum usuário logado."
        
        self.usuario_logado.meta = Meta(
            nome=nome,
            valor_total=valor_total,
            prazo_dias=prazo_dias,
            data_inicio=datetime.now().isoformat()
        )
        self.gerenciador.salvar_usuario(self.usuario_logado)
        return True, "Meta definida com sucesso!"

    def registrar_progresso_meta(self, valor_economizado: float) -> tuple[bool, str, int | None]:
        """Registra um novo progresso na meta e verifica marcos."""
        if not self.usuario_logado or self.usuario_logado.meta.valor_total == 0:
            return False, "Nenhuma meta ativa para registrar progresso.", None

        meta = self.usuario_logado.meta
        porcentagem_antiga = meta.calcular_porcentagem()
        
        meta.progresso_atual += valor_economizado
        meta.historico.append({
            "data": datetime.now().strftime("%d/%m/%Y"),
            "valor": valor_economizado
        })
        
        porcentagem_nova = meta.calcular_porcentagem()
        
        marco_atingido = None
        marcos = [50, 75, 100]
        for marco in marcos:
            if porcentagem_antiga < marco <= porcentagem_nova and marco not in meta.marcos_atingidos:
                marco_atingido = marco
                meta.marcos_atingidos.append(marco)
                break 

        self.gerenciador.salvar_usuario(self.usuario_logado)
        return True, "Progresso registrado!", marco_atingido

    def apagar_meta(self) -> tuple[bool, str]:
        """Apaga a meta atual do usuário."""
        if not self.usuario_logado:
            return False, "Nenhum usuário logado."
        
        self.usuario_logado.meta = Meta() 
        self.gerenciador.salvar_usuario(self.usuario_logado)
        return True, "Meta apagada com sucesso."
   
    def editar_meta(self, nome: str, valor_total: float, prazo_dias: int) -> tuple[bool, str]:
        """Edita a meta existente sem apagar o progresso."""
        if not self.usuario_logado or self.usuario_logado.meta.valor_total == 0:
            return False, "Nenhuma meta para editar."

        
        self.usuario_logado.meta.nome = nome
        self.usuario_logado.meta.valor_total = valor_total
        self.usuario_logado.meta.prazo_dias = prazo_dias
        
        porcentagem_atual = self.usuario_logado.meta.calcular_porcentagem()
        novos_marcos = []
        for marco in [50, 75, 100]:
            if porcentagem_atual >= marco:
                novos_marcos.append(marco)
        self.usuario_logado.meta.marcos_atingidos = novos_marcos

        self.gerenciador.salvar_usuario(self.usuario_logado)
        return True, "Meta atualizada com sucesso!"
    
    def verificar_prazo_meta(self) -> tuple[int, str | None]:
        """Calcula os dias restantes e retorna um aviso se o prazo estiver próximo."""
        if not self.usuario_logado or not self.usuario_logado.meta.data_inicio:
            return 0, None

        from datetime import datetime, timedelta
        
        meta = self.usuario_logado.meta
        data_inicio = datetime.fromisoformat(meta.data_inicio)
        data_final = data_inicio + timedelta(days=meta.prazo_dias)
        dias_restantes = (data_final - datetime.now()).days

        if dias_restantes < 0:
            return 0, "Prazo encerrado!"
        
        if dias_restantes <= 7:
            return dias_restantes, f"Atenção! Faltam apenas {dias_restantes} dias para o fim do prazo."
            
        return dias_restantes, None