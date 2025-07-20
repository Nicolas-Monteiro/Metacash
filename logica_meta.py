import flet as ft
import random
from datetime import datetime, timedelta
from gerenciador_dados import GerenciadorDeDados
from modelos import Usuario, Meta
from servicos import ValidadorDeFormato, enviar_email

class MetacashLogica:
    def __init__(self):
        
        self.gerenciador = GerenciadorDeDados()
        self.usuario_logado: Usuario | None = None
        self.usuario_pendente_2fa: Usuario | None = None

    #Lógicas de Perfil e usuário
    
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
   
   
   #Lógicas de Metas
   
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
    
    
    #Lógicas de Relatíorio

    def get_dados_relatorio(self) -> dict:
        """Prepara todos os dados para a tela de relatórios, incluindo emojis e percentuais para o tooltip."""
        if not self.usuario_logado:
            return {}

        u = self.usuario_logado
        orcamento_ideal = self._get_orcamento_ideal()
        
        gastos_variaveis = u.gastos_alimentacao + u.gastos_transporte + u.gastos_lazer
        total_gastos = u.gastos_fixos + gastos_variaveis
        sobra = u.salario - total_gastos

        # Calcula o total para encontrar o percentual de cada fatia
        total_geral = total_gastos + max(0, sobra)
        if total_geral == 0: total_geral = 1 

        dados_grafico = {
            "Gastos Fixos": {"valor": u.gastos_fixos, "icone": ft.Icons.HOUSE_ROUNDED, "cor": ft.Colors.BLUE_GREY, "ideal_percent": None, "emoji": "🏠"},
            "Alimentação": {"valor": u.gastos_alimentacao, "icone": ft.Icons.FASTFOOD, "cor": ft.Colors.ORANGE, "ideal_percent": orcamento_ideal.get("Alimentação"), "emoji": "🍔"},
            "Transporte": {"valor": u.gastos_transporte, "icone": ft.Icons.DIRECTIONS_BUS, "cor": ft.Colors.GREEN, "ideal_percent": orcamento_ideal.get("Transporte"), "emoji": "🚗"},
            "Lazer": {"valor": u.gastos_lazer, "icone": ft.Icons.SPORTS_ESPORTS, "cor": ft.Colors.PURPLE, "ideal_percent": orcamento_ideal.get("Lazer"), "emoji": "🎮"},
            "Sobra/Economia": {"valor": max(0, sobra), "icone": ft.Icons.SAVINGS, "cor": ft.Colors.TEAL, "ideal_percent": None, "emoji": "💰"}
        }

        # Adiciona o percentual atual a cada item para usar no tooltip
        for categoria, dados in dados_grafico.items():
            dados['percentual_atual'] = (dados['valor'] / total_geral) * 100

        maior_gasto_variavel = max(
            ("Alimentação", u.gastos_alimentacao),
            ("Transporte", u.gastos_transporte),
            ("Lazer", u.gastos_lazer),
            key=lambda item: item[1]
        )[0]

        return {
            "dados_grafico": dados_grafico,
            "recomendacao": self._gerar_recomendacao_gastos(),
            "dica_diaria": self._get_dica_diaria(maior_gasto_variavel)
        }
    
    def _get_orcamento_ideal(self) -> dict:
        """Calcula o percentual ideal para cada categoria de gasto variável."""
        u = self.usuario_logado
        prefs = u.preferencias_gastos
        total_pesos = sum(prefs.values())
        
        if total_pesos == 0:
            return {}

        orcamento = {}
        for categoria, peso in prefs.items():
            percentual = (peso / total_pesos) * 100
            # A chave aqui deve corresponder às chaves em dados_grafico
            if categoria == 'alimentacao': orcamento['Alimentação'] = percentual
            if categoria == 'transporte': orcamento['Transporte'] = percentual
            if categoria == 'lazer': orcamento['Lazer'] = percentual
        
        return orcamento
    
    def _get_dica_diaria(self, maior_gasto: str) -> str:
        """Retorna uma dica de economia diária com emojis e mais opções."""
        dicas = {
            "Alimentação": [
                "🍲 Planeje suas refeições da semana para evitar compras por impulso.",
                "🧊 Cozinhe em maior quantidade e congele porções para os dias corridos.",
                "🍎 Leve lanches de casa para o trabalho ou estudo.",
                "🛒 Compare preços e aproveite promoções em diferentes supermercados.",
                "💧 Beba mais água. Muitas vezes confundimos sede com fome.",
                "☕ Faça seu próprio café em casa em vez de comprar todos os dias."
            ],
            "Transporte": [
                "🚌 Considere usar transporte público um ou dois dias na semana.",
                "🚗 Combine caronas com colegas de trabalho ou amigos.",
                "🔧 Faça a manutenção do seu veículo. Pneus calibrados economizam combustível.",
                "🚲 Para distâncias curtas, experimente caminhar ou usar uma bicicleta.",
                "⛽ Pesquise postos com combustível mais barato na sua rota.",
                "🗺️ Planeje suas rotas para evitar trânsito e pedágios desnecessários."
            ],
            "Lazer": [
                "🌳 Procure por eventos gratuitos na sua cidade, como parques e shows ao ar livre.",
                "🏡 Reúna amigos em casa em vez de sempre sair para bares e restaurantes.",
                "🎟️ Aproveite promoções de cinema ou dias com ingressos mais baratos.",
                "📺 Cancele serviços de streaming que você não está utilizando com frequência.",
                "📚 Use bibliotecas públicas para ler livros e revistas sem custo.",
                "💪 Cancele a academia se não estiver indo e opte por exercícios ao ar livre."
            ]
        }
        
        lista_de_dicas = dicas.get(maior_gasto, ["💰 Planeje seu orçamento e acompanhe seus gastos de perto."])
        dia_do_ano = datetime.now().timetuple().tm_yday
        indice_dica = dia_do_ano % len(lista_de_dicas)
        
        return lista_de_dicas[indice_dica]
    
    def _gerar_recomendacao_gastos(self) -> str:
        """Gera uma recomendação de orçamento baseada nas prioridades do usuário."""
        u = self.usuario_logado
        prefs = u.preferencias_gastos
        total_pesos = sum(prefs.values())
        
        if total_pesos == 0:
            return "Defina suas prioridades de gastos no seu perfil para receber recomendações."

        renda_para_variaveis = u.salario - u.gastos_fixos
        if renda_para_variaveis < 0:
            return "Atenção: Seus gastos fixos já ultrapassam seu salário. Reveja seu orçamento com urgência."

        recomendacoes = []
        
        mapa_categorias = {
            'alimentacao': ('Alimentação', u.gastos_alimentacao),
            'transporte': ('Transporte', u.gastos_transporte),
            'lazer': ('Lazer', u.gastos_lazer)
        }
        
        for chave_pref, peso in prefs.items():
            nome_categoria, gasto_atual = mapa_categorias[chave_pref]
            orcamento_ideal = (peso / total_pesos) * renda_para_variaveis
            
            diferenca = gasto_atual - orcamento_ideal
            # Alerta se o gasto estiver 10% acima do ideal para aquela prioridade
            if diferenca > (orcamento_ideal * 0.1):
                recomendacoes.append(f"Seu gasto com {nome_categoria.lower()} (R$ {gasto_atual:.2f}) está acima do ideal de R$ {orcamento_ideal:.2f} para suas prioridades.")

        if not recomendacoes:
            return "Seus gastos estão bem alinhados com suas prioridades. Ótimo trabalho!"
        
        return " ".join(recomendacoes)