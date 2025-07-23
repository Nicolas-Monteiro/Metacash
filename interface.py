from dotenv import load_dotenv
load_dotenv()
import flet as ft
import time
from utils import *
from logica_meta import MetacashLogica
from servicos import ValidadorDeFormato
from telas import TelaSemMeta, TelaCriarEditarMeta, TelaPrincipalMeta, TelaRelatorios



class Interface_Inicial:
    def __init__(self):
        self.page = None
        self.main_view_container = ft.Container(expand=True)
        self.popup_celebratorio = PopupFeedback()
        self.popup_confirmacao_apagar_meta = PopupDeConfirmacao(on_confirm=self._executar_delecao_meta)
        self.popup_confirmacao_apagar_conta = PopupDeConfirmacao(on_confirm=self._executar_delecao_conta)
        self.popup_input_progresso = PopupInput(on_save=self._executar_salvar_progresso)
        self.main_content_area = None
        self.logica = MetacashLogica()
        self.theme_button = None
        self.texto_feedback_geral = ft.Text(value="", color=ft.Colors.RED, weight=ft.FontWeight.BOLD, visible=False)
        self.cadastro_usuario, self.cadastro_email, self.cadastro_senha, self.cadastro_confirma_senha = None, None, None, None
        self.cadastro_salario, self.cadastro_gastos_fixos = None, None
        self.cadastro_gastos_alimentacao, self.cadastro_gastos_transporte, self.cadastro_gastos_lazer = None, None, None
        self.slider_alimentacao, self.slider_transporte, self.slider_lazer = None, None, None
        self.login_usuario, self.login_senha = None, None
        self.login_feedback = ft.Text(value="", color=ft.Colors.RED, weight=ft.FontWeight.BOLD, visible=False, text_align=ft.TextAlign.CENTER)
        self.codigo_2fa_input, self.feedback_2fa = None, None
        self.nav_rail = None
        self.campos_edicao = {}
        self.dados_edicao_pendentes = None
    # SEÇÃO DE MÉTODOS PARA GERENCIAR METAS
    
    def _executar_edicao_meta(self, nome, valor, prazo):
        """Chama a lógica para EDITAR a meta e atualiza a UI."""
        sucesso, msg = self.logica.editar_meta(nome, valor, prazo)
        if sucesso:
            self.page.snack_bar = ft.SnackBar(ft.Text("Meta atualizada com sucesso!", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN)
            self.page.snack_bar.open = True
            self._exibir_tela_de_metas()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
        self.page.update()

    def _exibir_tela_de_metas(self):
        self.main_content_area.controls.clear()
        usuario = self.logica.usuario_logado
        
        if usuario.meta.valor_total == 0:
            construtor_view = TelaSemMeta(on_criar_meta=lambda e: self._exibir_tela_criar_editar_meta())
        else:
           
            dias_restantes, aviso_prazo = self.logica.verificar_prazo_meta()
            
            construtor_view = TelaPrincipalMeta(
                meta=usuario.meta,
                dias_restantes=dias_restantes,
                aviso_prazo=aviso_prazo,
                on_registrar_progresso=self._dialogo_registrar_progresso,
                on_editar=lambda e: self._exibir_tela_criar_editar_meta(meta_existente=usuario.meta),
                on_apagar=self._confirmar_apagar_meta
            )
        
        self.main_content_area.controls.append(construtor_view.build())
        self.page.update()

    def _exibir_tela_criar_editar_meta(self, meta_existente=None):
        self.main_content_area.controls.clear()
        
        funcao_salvar = self._executar_edicao_meta if meta_existente else self._salvar_meta

        construtor_view = TelaCriarEditarMeta(
            logica_app=self.logica,
            on_save=funcao_salvar,
            on_cancel=self._exibir_tela_de_metas, 
            meta_existente=meta_existente
        )
        self.main_content_area.controls.append(construtor_view.build())
        self.page.update()

    def _salvar_meta(self, nome, valor, prazo):
        sucesso, msg = self.logica.definir_meta(nome, valor, prazo)
        if sucesso:
            self.page.snack_bar = ft.SnackBar(ft.Text("Meta salva com sucesso!", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN)
            self.page.snack_bar.open = True
            self._exibir_tela_de_metas()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
        self.page.update()

    def _dialogo_registrar_progresso(self, e):
        """Abre o pop-up customizado para registrar progresso."""
        self.popup_input_progresso.show(
            title="Registrar Progresso",
            label="Valor economizado"
        )

    def _executar_salvar_progresso(self, popup: PopupInput):
        """
        Executa a lógica de salvamento quando o botão 'Salvar' do PopupInput é clicado.
        """
        valor_input_control = popup.input_field
        try:
            valor = float(valor_input_control.value)
            if valor <= 0:
                valor_input_control.error_text = "O valor deve ser positivo."
                popup.update()
                return

            sucesso, msg, marco = self.logica.registrar_progresso_meta(valor)

            if sucesso:
                popup.close()
                self.page.snack_bar = ft.SnackBar(ft.Text("Progresso salvo!"), bgcolor=ft.Colors.GREEN)
                self.page.snack_bar.open = True
                self._exibir_tela_de_metas()
                
                if marco:
                    self.popup_celebratorio.show(f"Parabéns! Você alcançou {marco}% da sua meta!")
            else:
                valor_input_control.error_text = msg
                popup.update()

        except (ValueError, TypeError):
            valor_input_control.error_text = "Valor inválido. Use apenas números."
            popup.update()

    def _dialogo_ver_historico(self, e):
        historico = self.logica.usuario_logado.meta.historico
        if not historico:
            conteudo = ft.Text("Nenhum progresso registrado ainda.")
        else:
            entradas_lista = [ft.DataRow(cells=[ft.DataCell(ft.Text(item['data'])), ft.DataCell(ft.Text(f"R$ {item['valor']:.2f}"))]) for item in reversed(historico)]
            conteudo = ft.DataTable(columns=[ft.DataColumn(ft.Text("Data")), ft.DataColumn(ft.Text("Valor"), numeric=True)], rows=entradas_lista)
        self.page.dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Histórico de Progresso"),
            content=ft.Container(content=conteudo, height=300, width=400),
            actions=[ft.TextButton("Fechar", on_click=lambda e: setattr(self.page.dialog, 'open', False) or self.page.update())]
        )
        self.page.dialog.open = True
        self.page.update()

    def _confirmar_apagar_meta(self, e):
        self.popup_confirmacao_apagar_meta.show("Apagar Meta", "Você tem certeza que deseja apagar sua meta e todo o seu progresso? Esta ação não pode ser desfeita.")
    
    def _executar_delecao_meta(self, e):
        self.logica.apagar_meta()
        self.page.snack_bar = ft.SnackBar(ft.Text("Sua meta foi apagada."), bgcolor=ft.Colors.GREEN)
        self.page.snack_bar.open = True
        self._exibir_tela_de_metas()


    # MÉTODOS DE RELATÓRIO

    def _exibir_tela_relatorios(self):
        self.main_content_area.controls.clear()
        
        dados_relatorio = self.logica.get_dados_relatorio()
        
        if not dados_relatorio:
            self.main_content_area.controls.append(ft.Text("Não foi possível carregar os dados do relatório."))
        else:
            construtor_view = TelaRelatorios(dados_relatorio)
            self.main_content_area.controls.append(construtor_view.build())
            
        self.page.update()


    # MÉTODOS DE ESTRUTURA E NAVEGAÇÃO
    def main(self, page: ft.Page):
        self.page = page
        page.title = "Metacash - Organizador Financeiro"
        page.window.width = 1200
        page.window.height = 1000
        page.bgcolor = ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=["#081318", "#4a717e", "#81b5cc"])
        page.theme_mode = ft.ThemeMode.DARK
        main_layout = ft.Stack([
            self.main_view_container, self.popup_celebratorio,
            self.popup_confirmacao_apagar_conta, self.popup_confirmacao_apagar_meta,self.popup_input_progresso
        ], expand=True)
        page.add(main_layout)
        self.menu_login()

    def navigate(self, e):
        self._carregar_view_dashboard(e.control.selected_index)

    def _carregar_view_dashboard(self, index: int):
        """Roteia a navegação para a tela correta."""
        self.main_content_area.controls.clear()
        if index == 0:
            self.menu_perfil()
        elif index == 1:
            self._exibir_tela_de_metas()
        elif index == 2:
            self._exibir_tela_relatorios()
        self.page.update()

    def menu_dashboard(self, e=None):
        self.main_view_container.content = None
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.theme_button = ft.IconButton(icon=ft.Icons.BRIGHTNESS_2, tooltip="Mudar tema", on_click=self.mudar_tema)
        logout_button = ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=self.menu_login)
        trailing_controls = ft.Column([self.theme_button, logout_button], spacing=5, alignment=ft.MainAxisAlignment.CENTER)
        self.nav_rail = ft.NavigationRail(
            selected_index=0, label_type=ft.NavigationRailLabelType.ALL, extended=False, min_width=100,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE), on_change=self.navigate, trailing=trailing_controls,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil"),
                ft.NavigationRailDestination(icon=ft.Icons.STAR_BORDER, selected_icon=ft.Icons.STAR, label="Metas"),
                ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, selected_icon=ft.Icons.CALENDAR_MONTH, label="Calendário"),
            ]
        )
        self.main_content_area = ft.Column(expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        layout = ft.Row([ft.Container(content=self.nav_rail, on_hover=self.expand_nav_rail, height=self.page.window.height if self.page else 1000), ft.VerticalDivider(width=1), self.main_content_area], expand=True)
        self.main_view_container.content = layout
        self._carregar_view_dashboard(0)
        self.page.update()

    # MÉTODOS DAS TELAS  (LOGIN, CADASTRO, PERFIL, ETC.)
    def voltar_para_perfil(self, e=None):
        """Volta para a tela de perfil, recarregando a view."""
        self._carregar_view_dashboard(0)

    def handle_salvar_edicao_click(self, e):
        """Lida com o clique no botão 'Salvar', agora com validações de campo."""
        # Limpa erros anteriores
        for campo in self.campos_edicao.values():
            campo.error_text = None

        formulario_valido = True
        
        # Validação do Nome de Usuário
        novo_nome = self.campos_edicao['nome_usuario'].value
        if not novo_nome:
            self.campos_edicao['nome_usuario'].error_text = "O nome de usuário não pode ser vazio."
            formulario_valido = False
        elif self.logica.usuario_logado.nome_usuario.lower() != novo_nome.lower() and self.logica.gerenciador.encontrar_usuario(novo_nome):
            self.campos_edicao['nome_usuario'].error_text = "Este nome de usuário já está em uso."
            formulario_valido = False

        # Validação do Email
        novo_email = self.campos_edicao['email'].value
        if not novo_email:
            self.campos_edicao['email'].error_text = "O e-mail não pode ser vazio."
            formulario_valido = False
        elif not ValidadorDeFormato.email_tem_dominio_valido(novo_email):
            self.campos_edicao['email'].error_text = "O domínio do e-mail é inválido."
            formulario_valido = False
        elif self.logica.usuario_logado.email.lower() != novo_email.lower() and self.logica.gerenciador.email_existe(novo_email):
            self.campos_edicao['email'].error_text = "Este e-mail já está em uso."
            formulario_valido = False

        # Validação de campos financeiros
        campos_financeiros = ['salario', 'gastos_fixos', 'gastos_alimentacao', 'gastos_transporte', 'gastos_lazer']
        for nome_campo in campos_financeiros:
            campo = self.campos_edicao[nome_campo]
            if not ValidadorDeFormato.validacao_de_valor_monetario(campo.value):
                campo.error_text = "Valor inválido. Use apenas números positivos."
                formulario_valido = False

        # Se houver qualquer erro de validação, atualiza a tela e para a execução
        if not formulario_valido:
            self.page.update()
            return
            
        self.dados_edicao_pendentes = {
            "nome_usuario": self.campos_edicao['nome_usuario'].value,
            "email": self.campos_edicao['email'].value,
            "salario": self.campos_edicao['salario'].value,
            "gastos_fixos": self.campos_edicao['gastos_fixos'].value,
            "gastos_alimentacao": self.campos_edicao['gastos_alimentacao'].value,
            "gastos_transporte": self.campos_edicao['gastos_transporte'].value,
            "gastos_lazer": self.campos_edicao['gastos_lazer'].value,
        }
        
        nova_senha_campo = self.campos_edicao['nova_senha']
        confirma_senha_campo = self.campos_edicao['confirma_senha']
        
        # Se o usuário preencheu o campo de nova senha
        if nova_senha_campo.value:
            valida_sucesso, valida_msg = ValidadorDeFormato.validacao_senha(nova_senha_campo.value)
            if not valida_sucesso:
                nova_senha_campo.error_text = valida_msg
                self.page.update()
                return
            if nova_senha_campo.value != confirma_senha_campo.value:
                confirma_senha_campo.error_text = "As senhas não correspondem."
                self.page.update()
                return
            
            # Se a senha for válida, procede com a verificação 2FA
            self.dados_edicao_pendentes['nova_senha'] = nova_senha_campo.value
            self.dados_edicao_pendentes['confirma_senha'] = confirma_senha_campo.value
            sucesso_2fa, mensagem_2fa = self.logica.iniciar_2fa_para_edicao()
            if sucesso_2fa:
                self.menu_2fa_para_edicao(mensagem_2fa)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(mensagem_2fa, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
                self.page.snack_bar.open = True
                self.page.update()
        else:
            # Se não houver mudança de senha, salva os dados diretamente
            sucesso, mensagem = self.logica.atualizar_dados_usuario(self.dados_edicao_pendentes)
            self.page.snack_bar = ft.SnackBar(ft.Text(mensagem, color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN if sucesso else ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            if sucesso:
                self.voltar_para_perfil()

    def handle_verificar_2fa_e_salvar(self, e, codigo_input, feedback_text):
        """Verifica o código 2FA e, se correto, salva todas as alterações."""
        codigo = codigo_input.value
        if not codigo:
            feedback_text.value = "Por favor, insira o código."
            feedback_text.visible = True
            self.page.update()
            return
        sucesso_2fa, msg_2fa = self.logica.verificar_codigo_2fa(codigo)
        if not sucesso_2fa:
            feedback_text.value = msg_2fa
            feedback_text.visible = True
            self.page.update()
            return
        
        sucesso_senha, msg_senha = self.logica.alterar_senha(
            self.dados_edicao_pendentes['nova_senha'],
            self.dados_edicao_pendentes['confirma_senha']
        )
        if not sucesso_senha:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao alterar senha: {msg_senha}", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            self.voltar_para_perfil()
            return
        
        sucesso_dados, msg_dados = self.logica.atualizar_dados_usuario(self.dados_edicao_pendentes)
        self.page.snack_bar = ft.SnackBar(ft.Text("Todas as alterações foram salvas com sucesso!"))
        self.page.snack_bar.open = True
        self.page.update()
        self.voltar_para_perfil()

    def menu_2fa_para_edicao(self, mensagem_info: str):
        """Constrói a tela de verificação 2FA para edição de perfil."""
        self.main_content_area.controls.clear()
        codigo_input = ft.TextField(label="Código de 6 dígitos", width=300, autofocus=True, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
        feedback_text = ft.Text(value="", color=ft.Colors.RED, weight=ft.FontWeight.BOLD, visible=False, text_align=ft.TextAlign.CENTER)
        verificar_btn = ft.ElevatedButton("Verificar e Salvar", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE), on_click=lambda e: self.handle_verificar_2fa_e_salvar(e, codigo_input, feedback_text))
        cancelar_btn = ft.TextButton("Cancelar Alteração", on_click=self.voltar_para_perfil)
        card_2fa = ft.Card(elevation=20, shadow_color="#c47ebbff", content=ft.Container(content=ft.Column(controls=[ft.Icon(name=ft.Icons.SECURITY, size=40, color="#06d675"), ft.Text("Verificação de Segurança", size=22, weight=ft.FontWeight.BOLD), ft.Text(mensagem_info, size=14, text_align=ft.TextAlign.CENTER), codigo_input, feedback_text, verificar_btn, cancelar_btn], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15), padding=30, width=400, height=400, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)))
        container_centralizado = ft.Container(content=card_2fa, alignment=ft.alignment.center, expand=True)
        self.main_content_area.controls.append(container_centralizado)
        self.page.update()

    def handle_alterar_info_click(self, e): self.menu_editar_perfil()
    def handle_deletar_conta_click(self, e): self.popup_confirmacao_apagar_conta.show("Confirmar Deleção de Conta", "Tem a certeza que deseja deletar a sua CONTA? Esta ação é irreversível.")
    def _executar_delecao_conta(self, e):
        sucesso, mensagem = self.logica.deletar_conta_logado()
        if sucesso:
            self.page.snack_bar = ft.SnackBar(ft.Text("Conta deletada com sucesso."))
            self.page.snack_bar.open = True; self.page.update(); time.sleep(1.5)
            self.menu_login()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text(mensagem, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True; self.page.update()
    
    def menu_perfil(self):
       
        self.main_content_area.controls.clear()
        usuario = self.logica.usuario_logado
        card_conta = ft.Card(
            elevation=10, 
            content=ft.Container(
                padding=20, 
                border_radius=10, 
                content=ft.Column(
                    controls=[
                        ft.Text("Dados da Conta", size=20, weight=ft.FontWeight.BOLD), 
                        ft.Divider(), 
                        criar_linha_info(ft.Icons.PERSON, "Nome de Usuário:", usuario.nome_usuario), 
                        criar_linha_info(ft.Icons.EMAIL, "E-mail:", usuario.email)])))
        card_financeiro = ft.Card(
            elevation=10, 
            content=ft.Container(
                padding=20, 
                border_radius=10, 
                content=ft.Column(
                    controls=[
                        ft.Text("Resumo Financeiro", size=20, weight=ft.FontWeight.BOLD), 
                        ft.Divider(), 
                        criar_linha_info(ft.Icons.MONETIZATION_ON, "Salário Mensal:", f"R$ {usuario.salario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), 
                        criar_linha_info(ft.Icons.PAYMENT, "Gastos Fixos:", f"R$ {usuario.gastos_fixos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), 
                        criar_linha_info(ft.Icons.FASTFOOD, "Gastos Alimentação:", f"R$ {usuario.gastos_alimentacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), 
                        criar_linha_info(ft.Icons.DIRECTIONS_CAR, "Gastos Transporte:", f"R$ {usuario.gastos_transporte:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), 
                        criar_linha_info(ft.Icons.SPORTS_ESPORTS, "Gastos Lazer:", f"R$ {usuario.gastos_lazer:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")) ])))
        alterar_btn = ft.ElevatedButton("Alterar Informações", icon=ft.Icons.EDIT, on_click=self.handle_alterar_info_click, style=ft.ButtonStyle(bgcolor="#2a7a9e", color=ft.Colors.WHITE))
        deletar_btn = ft.ElevatedButton("Deletar Conta", icon=ft.Icons.DELETE_FOREVER, on_click=self.handle_deletar_conta_click, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE))
        botoes_acao = ft.Row(controls=[alterar_btn, deletar_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        layout_perfil = ft.Column(controls=[ft.Text("Meu Perfil", size=30, weight=ft.FontWeight.BOLD), card_conta, card_financeiro, botoes_acao], spacing=25, expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.main_content_area.controls.append(layout_perfil)
        self.page.update()

    def menu_editar_perfil(self):
        usuario = self.logica.usuario_logado
        self.campos_edicao = {
            'nome_usuario': ft.TextField(label="Nome de Usuário", value=usuario.nome_usuario),
            'email': ft.TextField(label="E-mail", value=usuario.email),
            'salario': ft.TextField(label="Salário", value=str(usuario.salario), prefix_text="R$"),
            'gastos_fixos': ft.TextField(label="Gastos Fixos", value=str(usuario.gastos_fixos), prefix_text="R$"),
            'gastos_alimentacao': ft.TextField(label="Gastos com Alimentação", value=str(usuario.gastos_alimentacao), prefix_text="R$"),
            'gastos_transporte': ft.TextField(label="Gastos com Transporte", value=str(usuario.gastos_transporte), prefix_text="R$"),
            'gastos_lazer': ft.TextField(label="Gastos com Lazer", value=str(usuario.gastos_lazer), prefix_text="R$"),
            'nova_senha': ft.TextField(label="Nova Senha", password=True, can_reveal_password=True, hint_text="Deixe em branco para não alterar"),
            'confirma_senha': ft.TextField(label="Confirmar Nova Senha", password=True)
        }
        card_edicao_conta = ft.Card(elevation=10, 
                                    content=ft.Container(
                                        padding=20, 
                                        border_radius=10, 
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("Editar Dados da Conta", size=20, weight=ft.FontWeight.BOLD), 
                                                ft.Divider(), self.campos_edicao['nome_usuario'], self.campos_edicao['email']])))
        card_edicao_financeiro = ft.Card(
            elevation=10, content=ft.Container(
                padding=20, 
                border_radius=10, 
                content=ft.Column(controls=[ft.Text("Editar Dados Financeiros", size=20, weight=ft.FontWeight.BOLD), 
                                            ft.Divider(), self.campos_edicao['salario'], 
                                            self.campos_edicao['gastos_fixos'], 
                                            self.campos_edicao['gastos_alimentacao'], 
                                            self.campos_edicao['gastos_transporte'], 
                                            self.campos_edicao['gastos_lazer']])))
        card_edicao_senha = ft.Card(elevation=10, 
                                    content=ft.Container(
                                        padding=20, 
                                        border_radius=10, 
                                        content=ft.Column(controls=[
                                            ft.Text("Alterar Senha", size=20, weight=ft.FontWeight.BOLD), 
                                            ft.Text("Preencha apenas se desejar alterar a senha.", size=12, italic=True), 
                                            ft.Divider(), self.campos_edicao['nova_senha'], self.campos_edicao['confirma_senha']])))
        salvar_btn = ft.ElevatedButton("Salvar Alterações", icon=ft.Icons.SAVE, on_click=self.handle_salvar_edicao_click, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE))
        cancelar_btn = ft.ElevatedButton("Cancelar", icon=ft.Icons.CANCEL, on_click=self.voltar_para_perfil, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE))
        botoes_acao = ft.Row(controls=[salvar_btn, cancelar_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        layout_edicao = ft.Column(
            controls=[
                ft.Text("Editar Perfil", size=30, weight=ft.FontWeight.BOLD), 
                card_edicao_conta, card_edicao_financeiro, card_edicao_senha, botoes_acao], 
                spacing=25, expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(layout_edicao)
        self.page.update()

    def menu_2fa_para_edicao(self, mensagem_info: str):
        self.main_content_area.controls.clear()
        codigo_input = ft.TextField(label="Código de 6 dígitos", width=300, autofocus=True, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
        feedback_text = ft.Text(value="", color=ft.Colors.RED, weight=ft.FontWeight.BOLD, visible=False, text_align=ft.TextAlign.CENTER)
        verificar_btn = ft.ElevatedButton("Verificar e Salvar", width=300, 
                                          style=ft.ButtonStyle(bgcolor="#06d675", 
                                         color=ft.Colors.WHITE), 
                                         on_click=lambda e: self.handle_verificar_2fa_e_salvar(e, codigo_input, feedback_text))
        cancelar_btn = ft.TextButton("Cancelar Alteração", on_click=self.voltar_para_perfil)
        card_2fa = ft.Card(
            elevation=20, 
            shadow_color="#c47ebbff", 
            content=ft.Container(
                content=ft.Column(
                    controls=[ft.Icon(name=ft.Icons.SECURITY, size=40, color="#06d675"), ft.Text("Verificação de Segurança", 
                                                            size=22, weight=ft.FontWeight.BOLD),
                                                            ft.Text(mensagem_info, size=14, text_align=ft.TextAlign.CENTER), codigo_input, feedback_text, verificar_btn, cancelar_btn], 
                                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15), 
                                                            padding=30, width=400, height=400, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)))
        container_centralizado = ft.Container(content=card_2fa, alignment=ft.alignment.center, expand=True)
        self.main_content_area.controls.append(container_centralizado)
        self.page.update()

    def menu_dashboard(self, e=None):
        self.main_view_container.content = None
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.theme_button = ft.IconButton(icon=ft.Icons.BRIGHTNESS_2, tooltip="Mudar tema", on_click=self.mudar_tema)
        logout_button = ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=self.menu_login)
        trailing_controls = ft.Column([self.theme_button, logout_button], spacing=5, alignment=ft.MainAxisAlignment.CENTER)
        self.nav_rail = ft.NavigationRail(
            selected_index=0, label_type=ft.NavigationRailLabelType.ALL,
            extended=False, min_width=100, min_extended_width=200,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            on_change=self.navigate, trailing=trailing_controls,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil"),
                ft.NavigationRailDestination(icon=ft.Icons.STAR_BORDER, selected_icon=ft.Icons.STAR, label="Metas"),
                ft.NavigationRailDestination(icon=ft.Icons.PIE_CHART_OUTLINE, selected_icon=ft.Icons.PIE_CHART, label="Relatórios"),
            ],
        )
        nav_rail_container = ft.Container(content=self.nav_rail, on_hover=self.expand_nav_rail, height=self.page.window.height - 50)
        self.main_content_area = ft.Column(expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        layout = ft.Row([nav_rail_container, ft.VerticalDivider(width=1), self.main_content_area], expand=True)
        self.main_view_container.content = layout
        self._carregar_view_dashboard(0)
        self.page.update()
    
    def login_click(self, e):
        self.login_feedback.visible = False
        self.page.update()
        usuario = self.login_usuario.value
        senha = self.login_senha.value
        if not usuario or not senha:
            self.login_feedback.value = "Utilizador e senha são obrigatórios."
            self.login_feedback.visible = True
            self.page.update()
            return
        sucesso, mensagem, requer_2fa = self.logica.processar_login(usuario, senha)
        if sucesso:
            if requer_2fa:
                self.menu_2fa(mensagem)
            else:
                self.menu_dashboard()
        else:
            self.login_feedback.value = mensagem
            self.login_feedback.visible = True
            self.page.update()

    def verificar_2fa_click(self, e):
        self.feedback_2fa.visible = False
        self.page.update()
        codigo = self.codigo_2fa_input.value
        if not codigo:
            self.feedback_2fa.value = "Por favor, insira o código."
            self.feedback_2fa.visible = True
            self.page.update()
            return
        sucesso, mensagem = self.logica.verificar_codigo_2fa(codigo)
        if sucesso:
            self.menu_dashboard()
        else:
            self.feedback_2fa.value = mensagem
            self.feedback_2fa.visible = True
            self.page.update()

    def cadastrar_click(self, e):
        self.texto_feedback_geral.visible = False
        self.page.update()
        if not self.validar_campos_cadastro():
            return
        nome_usuario = self.cadastro_usuario.value
        email = self.cadastro_email.value
        senha = self.cadastro_senha.value
        confirmacao_senha = self.cadastro_confirma_senha.value
        sucesso_cadastro, mensagem_ou_usuario = self.logica.processar_cadastro(
            nome_usuario=nome_usuario, email=email, senha=senha, confirmacao_senha=confirmacao_senha
        )
        if not sucesso_cadastro:
            self.texto_feedback_geral.value = mensagem_ou_usuario
            self.texto_feedback_geral.color = ft.Colors.RED
            self.texto_feedback_geral.visible = True
            self.page.update()
            return
        salario_str = self.cadastro_salario.value
        gastos_fixos_str = self.cadastro_gastos_fixos.value
        gastos_alimentacao_str = self.cadastro_gastos_alimentacao.value
        gastos_transporte_str = self.cadastro_gastos_transporte.value
        gastos_lazer_str = self.cadastro_gastos_lazer.value
        preferencias = {
            "alimentacao": int(self.slider_alimentacao.value),
            "transporte": int(self.slider_transporte.value),
            "lazer": int(self.slider_lazer.value)
        }
        self.logica.usuario_logado = mensagem_ou_usuario
        sucesso_prefs, msg_prefs = self.logica.salvar_preferencias_financeiras(
            salario=float(salario_str.replace(",", ".")),
            gastos_fixos=float(gastos_fixos_str.replace(",", ".")),
            gastos_alimentacao=float(gastos_alimentacao_str.replace(",", ".")),
            gastos_transporte=float(gastos_transporte_str.replace(",", ".")),
            gastos_lazer=float(gastos_lazer_str.replace(",", ".")),
            preferencias=preferencias
        )
        if not sucesso_prefs:
            self.texto_feedback_geral.value = f"Usuário criado, mas erro nos dados: {msg_prefs}"
            self.texto_feedback_geral.color = ft.Colors.RED
            self.texto_feedback_geral.visible = True
        else:
            self.popup_celebratorio.show("Cadastro realizado com sucesso! Redirecionando...")
            
        self.page.update()
        if sucesso_prefs:
            time.sleep(2)
            self.menu_login()
        self.logica.usuario_logado = None

    def mudar_tema(self, e):
        self.page.theme_mode = ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.theme_button.icon = ft.Icons.WB_SUNNY if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.BRIGHTNESS_2
        self.page.update()
        self.theme_button.update()

    def expand_nav_rail(self, e):
        if self.nav_rail:
            self.nav_rail.extended = True if e.data == "true" else False
            self.nav_rail.update()

    def validar_campos_cadastro(self) -> bool:
        formulario_ok = True
        gerenciador = self.logica.gerenciador
        todos_os_campos = [
            self.cadastro_usuario, self.cadastro_email, self.cadastro_senha,
            self.cadastro_confirma_senha, self.cadastro_salario, self.cadastro_gastos_fixos,
            self.cadastro_gastos_alimentacao, self.cadastro_gastos_transporte, self.cadastro_gastos_lazer
        ]
        for campo in todos_os_campos:
            if campo:
                campo.error_text = None
        if not self.cadastro_usuario.value:
            self.cadastro_usuario.error_text = "O nome de usuário é obrigatório."
            formulario_ok = False
        elif gerenciador.encontrar_usuario(self.cadastro_usuario.value):
            self.cadastro_usuario.error_text = "Este nome de usuário já está em uso."
            formulario_ok = False
        if not self.cadastro_email.value:
            self.cadastro_email.error_text = "O e-mail é obrigatório."
            formulario_ok = False
        elif not ValidadorDeFormato.email_tem_dominio_valido(self.cadastro_email.value):
            self.cadastro_email.error_text = "Domínio de e-mail inválido."
            formulario_ok = False
        elif gerenciador.email_existe(self.cadastro_email.value):
            self.cadastro_email.error_text = "Já existe uma conta com este e-mail."
            formulario_ok = False
        if not self.cadastro_senha.value:
            self.cadastro_senha.error_text = "A senha é obrigatória."
            formulario_ok = False
        else:
            sucesso, msg = ValidadorDeFormato.validacao_senha(self.cadastro_senha.value)
            if not sucesso:
                self.cadastro_senha.error_text = msg
                formulario_ok = False
        if not self.cadastro_confirma_senha.value:
            self.cadastro_confirma_senha.error_text = "Confirme sua senha."
            formulario_ok = False
        elif self.cadastro_senha.value != self.cadastro_confirma_senha.value:
            self.cadastro_confirma_senha.error_text = "As senhas não são iguais."
            formulario_ok = False
        campos_financeiros = {
            self.cadastro_salario: "Salário", self.cadastro_gastos_fixos: "Gastos Fixos",
            self.cadastro_gastos_alimentacao: "Alimentação", self.cadastro_gastos_transporte: "Transporte",
            self.cadastro_gastos_lazer: "Lazer"
        }
        for campo, nome in campos_financeiros.items():
            valor = campo.value
            if not valor:
                campo.error_text = f"O campo de gastos com '{nome}' é obrigatório."
                formulario_ok = False
            else:
                valor_limpo = valor.replace(",", ".")
                if not ValidadorDeFormato.validacao_de_valor_monetario(valor_limpo):
                    campo.error_text = "Valor inválido. Use apenas números."
                    formulario_ok = False
        self.page.update()
        return formulario_ok

    def menu_login(self, e=None):
        self.main_view_container.content = None
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.login_usuario = ft.TextField(label="Utilizador", width=300, autofocus=True, icon=ft.Icons.PERSON)
        self.login_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300, icon=ft.Icons.LOCK)
        logo = ft.Row(
            controls=[ft.Text(spans=[
                ft.TextSpan("Meta", style=ft.TextStyle(size=38, weight=ft.FontWeight.BOLD)),
                ft.TextSpan("Cash", style=ft.TextStyle(size=42, weight=ft.FontWeight.BOLD, color="#00ff88"))
            ])], alignment=ft.MainAxisAlignment.CENTER
        )
        campo_login = ft.Card(
            elevation=20, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
                        self.login_usuario,
                        self.login_senha,
                        self.login_feedback,
                        ft.ElevatedButton("Entrar", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE), on_click=self.login_click, on_hover=botao_animado)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
                ), padding=25, width=400, height=350, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )
        campo_cadastro = ft.Card(
            elevation=25, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Ainda não tem uma conta?"),
                        ft.ElevatedButton("Cadastre-se", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE), on_click=self.menu_cadastro, on_hover=botao_animado)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ), padding=20, width=400, height=100, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )
        layout = ft.Column([logo, campo_login, campo_cadastro], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=40)
        self.main_view_container.content = layout
        self.page.update()

    def menu_2fa(self, mensagem_info: str):
        self.main_view_container.content = None
        self.codigo_2fa_input = ft.TextField(
            label="Código de 6 dígitos",
            width=300,
            autofocus=True,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        self.feedback_2fa = ft.Text(value="", color=ft.Colors.RED, weight=ft.FontWeight.BOLD, visible=False, text_align=ft.TextAlign.CENTER)
        card_2fa = ft.Card(
            elevation=20, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.SECURITY, size=40, color="#06d675"),
                        ft.Text("Verificação de Segurança", size=22, weight=ft.FontWeight.BOLD),
                        ft.Text(mensagem_info, size=14, text_align=ft.TextAlign.CENTER),
                        self.codigo_2fa_input,
                        self.feedback_2fa,
                        ft.ElevatedButton("Verificar Código", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE), on_click=self.verificar_2fa_click, on_hover=botao_animado),
                        ft.TextButton("Voltar para o Login", on_click=self.menu_login)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                padding=30, width=400, height=400, border_radius=15,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )
        self.main_view_container.content = card_2fa
        self.page.update()

    def menu_cadastro(self, e=None):
        self.main_view_container.content = None
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.cadastro_usuario = ft.TextField(label="Usuário", width=350, icon=ft.Icons.PERSON)
        self.cadastro_email = ft.TextField(label="E-mail", width=350, icon=ft.Icons.EMAIL)
        self.cadastro_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=350, icon=ft.Icons.LOCK)
        self.cadastro_confirma_senha = ft.TextField(label="Confirmar Senha", password=True, width=350, icon=ft.Icons.LOCK)
        self.cadastro_salario = ft.TextField(label="Salário", width=350, prefix_text="R$")
        self.cadastro_gastos_fixos = ft.TextField(label="Gastos Fixos Mensais", width=350, prefix_text="R$")
        self.cadastro_gastos_alimentacao = ft.TextField(label="Gastos com Alimentação", width=350, prefix_text="R$")
        self.cadastro_gastos_transporte = ft.TextField(label="Gastos com Transporte", width=350, prefix_text="R$")
        self.cadastro_gastos_lazer = ft.TextField(label="Gastos com Lazer", width=350, prefix_text="R$")
        self.slider_alimentacao = ft.Slider(min=1, max=5, divisions=4, value=3, width=150)
        self.slider_transporte = ft.Slider(min=1, max=5, divisions=4, value=3, width=150)
        self.slider_lazer = ft.Slider(min=1, max=5, divisions=4, value=3, width=150)
        back_button = ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, bgcolor="#06d675", icon_size=30, on_click=self.menu_login, on_hover=botao_animado)
        titulo = ft.Text("Criar Conta no MetaCash", size=24, weight=ft.FontWeight.BOLD)
        container_esquerda = ft.Card(
            elevation=25, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Dados da Conta", size=20, weight=ft.FontWeight.BOLD), ft.Divider(thickness=1),
                        self.cadastro_usuario, self.cadastro_email, self.cadastro_senha, self.cadastro_confirma_senha,
                    ], spacing=15
                ), padding=20, width=400, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )
        container_direita = ft.Card(
            elevation=25, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Dados Financeiros", size=20, weight=ft.FontWeight.BOLD), ft.Divider(thickness=1),
                        self.cadastro_salario, self.cadastro_gastos_fixos,
                        self.cadastro_gastos_alimentacao, self.cadastro_gastos_transporte, self.cadastro_gastos_lazer,
                        ft.Text("Preferências de Gasto (1 a 5)", size=16, weight=ft.FontWeight.BOLD), ft.Divider(thickness=1),
                        ft.Row([ft.Text("Alimentação", width=150), self.slider_alimentacao]),
                        ft.Row([ft.Text("Transporte", width=150), self.slider_transporte]),
                        ft.Row([ft.Text("Lazer", width=150), self.slider_lazer]),
                    ], spacing=10
                ), padding=20, width=400, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )
        botao_cadastrar = ft.ElevatedButton("Cadastrar", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE), on_click=self.cadastrar_click, on_hover=botao_animado)
        layout_central = ft.Row([container_esquerda, container_direita], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, spacing=50)
        layout = ft.Column([back_button, titulo, layout_central, self.texto_feedback_geral, botao_cadastrar], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, scroll=ft.ScrollMode.AUTO)
        self.main_view_container.content = layout
        self.page.update()

if __name__ == "__main__":
    app = Interface_Inicial()
    ft.app(target=app.main)