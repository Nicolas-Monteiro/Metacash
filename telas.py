import flet as ft
from utils import botao_animado

class TelaSemMeta:
    def __init__(self, on_criar_meta):
        self.on_criar_meta = on_criar_meta

    def build(self):
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.FLAG_OUTLINED, size=80, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                ft.Text("Você ainda não tem uma meta.", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Crie uma meta para começar a acompanhar seus objetivos financeiros!", text_align=ft.TextAlign.CENTER, width=400),
                ft.ElevatedButton("Criar Minha Primeira Meta", icon=ft.Icons.ADD, on_click=self.on_criar_meta, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE))
            ],
            spacing=20, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
        )

class TelaCriarEditarMeta:
    def __init__(self, logica_app, on_save, on_cancel, meta_existente=None):
        self.logica = logica_app
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.meta = meta_existente

        self.nome_meta = ft.TextField(label="Nome da Meta", value=self.meta.nome if self.meta else "", text_size=16)
        self.valor_meta = ft.TextField(label="Valor Total", value=str(self.meta.valor_total) if self.meta else "", prefix_text="R$", keyboard_type=ft.KeyboardType.NUMBER)
        self.prazo_meta = ft.TextField(label="Prazo em Dias", value=str(self.meta.prazo_dias) if self.meta else "", suffix_text="dias", keyboard_type=ft.KeyboardType.NUMBER)
        self.feedback_realismo = ft.Text(value="", size=14, weight=ft.FontWeight.BOLD)

    def _analisar_click(self, e):
        try:
            valor = float(self.valor_meta.value)
            prazo = int(self.prazo_meta.value)
            sucesso, msg = self.logica.analisar_realismo_meta(valor, prazo)
            self.feedback_realismo.value = msg
            self.feedback_realismo.color = ft.Colors.GREEN_ACCENT_700 if sucesso else ft.Colors.AMBER
            self.feedback_realismo.update()
        except (ValueError, TypeError):
            self.feedback_realismo.value = "Por favor, insira valores numéricos válidos."
            self.feedback_realismo.color = ft.Colors.RED
            self.feedback_realismo.update()
            
    def _salvar_click(self, e):
        # Limpa erros anteriores
        self.nome_meta.error_text = None
        self.valor_meta.error_text = None
        self.prazo_meta.error_text = None
        
        formulario_valido = True

        # Validação do nome
        if not self.nome_meta.value:
            self.nome_meta.error_text = "O nome da meta é obrigatório."
            formulario_valido = False
        
        # Validação do valor
        try:
            valor = float(self.valor_meta.value)
            if valor <= 0:
                self.valor_meta.error_text = "O valor deve ser um número positivo."
                formulario_valido = False
        except (ValueError, TypeError):
            self.valor_meta.error_text = "Valor inválido. Use apenas números."
            formulario_valido = False

        # Validação do prazo
        try:
            prazo = int(self.prazo_meta.value)
            if prazo <= 0:
                self.prazo_meta.error_text = "O prazo deve ser maior que zero."
                formulario_valido = False
        except (ValueError, TypeError):
            self.prazo_meta.error_text = "Prazo inválido. Use apenas números inteiros."
            formulario_valido = False
            
        # Se o formulário não for válido, atualiza os campos com os erros e para
        if not formulario_valido:
            self.nome_meta.update()
            self.valor_meta.update()
            self.prazo_meta.update()
            return

        # Se tudo estiver correto, chama a função de salvar
        self.on_save(
            self.nome_meta.value,
            float(self.valor_meta.value),
            int(self.prazo_meta.value)
        )

    def build(self):
        titulo = "Editar Meta" if self.meta and self.meta.valor_total > 0 else "Criar Nova Meta"
        card_meta = ft.Card(
            elevation=10,
            content=ft.Container(
                padding=25, width=500,
                content=ft.Column(
                    controls=[
                        ft.Text(titulo, size=24, weight=ft.FontWeight.BOLD),
                        self.nome_meta, self.valor_meta, self.prazo_meta,
                        ft.ElevatedButton("Analisar Realismo da Meta", icon=ft.Icons.INSIGHTS, on_click=self._analisar_click),
                        self.feedback_realismo,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton("Cancelar", on_click=self.on_cancel, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE)),
                                ft.ElevatedButton("Salvar Meta", on_click=self._salvar_click, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE))
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ], spacing=15
                )
            )
        )
        return ft.Column([card_meta], expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

class TelaPrincipalMeta:
    """Construtor para a tela principal que exibe a meta ativa."""
    def __init__(self, meta, dias_restantes, aviso_prazo, on_registrar_progresso, on_editar, on_apagar):
        self.meta = meta
        self.dias_restantes = dias_restantes
        self.aviso_prazo = aviso_prazo
        self.on_registrar_progresso = on_registrar_progresso
        self.on_editar = on_editar
        self.on_apagar = on_apagar

    def build(self):
        porcentagem = self.meta.calcular_porcentagem()
        valor_restante = max(0, self.meta.valor_total - self.meta.progresso_atual)
        
        poupanca_diaria = (valor_restante / self.dias_restantes) if self.dias_restantes > 0 else 0
        poupanca_semanal = poupanca_diaria * 7
        poupanca_mensal = poupanca_diaria * 30


        progresso_circular = ft.Stack(
            [
                ft.ProgressRing(value=porcentagem / 100, width=200, height=200, stroke_width=18, bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), color="#00ff88"),
                ft.Container(content=ft.Text(f"{porcentagem:.1f}%", size=32, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center)
            ], width=200, height=200
        )

        info_prazo = ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_TODAY, size=16),
                ft.Text(f"Prazo: {self.dias_restantes} dias restantes", size=14, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        aviso_widget = ft.Container()
        if self.aviso_prazo:
            aviso_widget = ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER), ft.Text(self.aviso_prazo, color=ft.Colors.AMBER)]),
                padding=5, border_radius=5, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER)
            )

        card_economia = ft.Card(elevation=4, content=ft.Container(padding=15, content=ft.Row(
            controls=[
                ft.Column([ft.Text("DIÁRIA", weight=ft.FontWeight.BOLD), ft.Text(f"R$ {poupanca_diaria:.2f}")]),
                ft.VerticalDivider(),
                ft.Column([ft.Text("SEMANAL", weight=ft.FontWeight.BOLD), ft.Text(f"R$ {poupanca_semanal:.2f}")]),
                ft.VerticalDivider(),
                ft.Column([ft.Text("MENSAL", weight=ft.FontWeight.BOLD), ft.Text(f"R$ {poupanca_mensal:.2f}")]),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.CENTER
        )))

        #Tabela de histórico
        historico_rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(item['data'])),
                ft.DataCell(ft.Text(f"R$ {item['valor']:.2f}", color="#00ff88")),
            ]) for item in reversed(self.meta.historico)
        ]
        tabela_historico = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Data do Registro")),
                ft.DataColumn(ft.Text("Valor Guardado"), numeric=True),
            ],
            rows=historico_rows,
        ) if historico_rows else ft.Text("Nenhum progresso registrado ainda.", text_align=ft.TextAlign.CENTER)

        # Layout Final
        return ft.Column(
            controls=[
                ft.Text(self.meta.nome, size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Objetivo: R$ {self.meta.valor_total:,.2f}", size=18),
                info_prazo,
                aviso_widget,
                progresso_circular,
                ft.Divider(height=25),
                ft.Row(
                    [
                        ft.ElevatedButton("Registrar Progresso", icon=ft.Icons.ADD_TASK, on_click=self.on_registrar_progresso, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE)),
                        ft.ElevatedButton("Editar Meta", icon=ft.Icons.EDIT, on_click=self.on_editar),
                        ft.ElevatedButton("Apagar Meta", icon=ft.Icons.DELETE_FOREVER, on_click=self.on_apagar, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                ft.Divider(height=25),
                ft.Text("Para alcançar sua meta, você precisa economizar:", weight=ft.FontWeight.BOLD),
                card_economia,
                ft.Divider(height=25),
                ft.Text("Histórico de Progresso", size=20, weight=ft.FontWeight.BOLD),
                ft.Column([tabela_historico], scroll=ft.ScrollMode.AUTO, expand=True) 
            ],
            expand=True, spacing=10, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
#Classe para fazer a tela do relatório

class TelaRelatorios:
    def __init__(self, dados_relatorio):
        self.dados_grafico = dados_relatorio.get("dados_grafico", {})
        self.recomendacao = dados_relatorio.get("recomendacao", "")
        self.dica_diaria = dados_relatorio.get("dica_diaria", "")
        self.pie_chart = None

        # --- ESTILOS E TAMANHOS DEFINIDOS EXATAMENTE COMO NO SEU EXEMPLO ---
        self.normal_radius = 160
        self.hover_radius = 180
        self.normal_title_style = ft.TextStyle(size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
        self.hover_title_style = ft.TextStyle(
            size=26,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
        )
        self.normal_badge_size = 50
        self.hover_badge_size = 65

    def _badge(self, icon, size):
        """Função auxiliar para criar o ícone (badge), como no seu exemplo."""
        return ft.Container(
            ft.Icon(icon, color=ft.Colors.with_opacity(0.7, ft.Colors.BLACK)),
            width=size,
            height=size,
            border=ft.border.all(1, ft.Colors.BROWN),
            border_radius=size / 2,
            bgcolor=ft.Colors.WHITE,
        )

    def _on_chart_event(self, e: ft.PieChartEvent):
       
        for idx, section in enumerate(self.pie_chart.sections):
            if idx == e.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
                section.badge.width = self.hover_badge_size
                section.badge.height = self.hover_badge_size
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
                section.badge.width = self.normal_badge_size
                section.badge.height = self.normal_badge_size
        
        # A única chamada de atualização necessária, como no seu exemplo.
        self.pie_chart.update()

    def build(self):
        total_valor = sum(item['valor'] for item in self.dados_grafico.values() if item['valor'] > 0)
        if total_valor == 0: total_valor = 1

        secoes_grafico = []
        for categoria, dados in self.dados_grafico.items():
            if dados['valor'] > 0:
                percentual_atual = (dados['valor'] / total_valor) * 100
                secoes_grafico.append(
                    ft.PieChartSection(
                        dados['valor'],
                        title=f"{percentual_atual:.1f}%",
                        title_style=self.normal_title_style,
                        color=dados['cor'],
                        radius=self.normal_radius,
                        badge=self._badge(dados['icone'], self.normal_badge_size),
                        badge_position=0.98,
                    )
                )

        self.pie_chart = ft.PieChart(
            sections=secoes_grafico,
            sections_space=0,
            center_space_radius=0,
            on_chart_event=self._on_chart_event, 
            height=600,
            expand=True
        )

        legenda = ft.Row(
            controls=[
                ft.Row([
                    ft.Container(width=18, height=18, bgcolor=dados['cor'], border_radius=4),
                    ft.Icon(name=dados['icone'], size=18),
                    ft.Text(categoria, size=14)
                ], spacing=8) for categoria, dados in self.dados_grafico.items() if dados['valor'] > 0
            ],
            wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=25
        )

        grafico_container = ft.Card(elevation=10, content=ft.Container(
            padding=ft.padding.symmetric(vertical=30, horizontal=20),
            content=ft.Column(
                [
                    ft.Text("Distribuição de Gastos Mensais", size=24, weight=ft.FontWeight.BOLD),
                    self.pie_chart,
                    legenda,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20
            )
        ))
        
        dica_container = ft.Card(elevation=10, content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.LIGHTBULB_CIRCLE, color=ft.Colors.AMBER), ft.Text("Dica de Economia do Dia", size=18, weight=ft.FontWeight.BOLD)]),
                ft.Divider(),
                ft.Text(self.dica_diaria, size=16, italic=True)
            ])
        ))
        
        recomendacao_container = ft.Card(elevation=10, content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.INSIGHTS, color=ft.Colors.CYAN), ft.Text("Diagnóstico Financeiro", size=18, weight=ft.FontWeight.BOLD)]),
                ft.Divider(),
                ft.Text(self.recomendacao, size=16, selectable=True)
            ])
        ))

        return ft.Column(
            controls=[grafico_container, dica_container, recomendacao_container],
            scroll=ft.ScrollMode.AUTO, spacing=25, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )