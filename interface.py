import flet as ft
import time
from utils import botao_animado, Popup

class Interface_Inicial:
    def __init__(self):
        self.page = None
        self.main_view_container = ft.Container(expand=True)
        self.popup=Popup(on_close=self.menu_login)
        self.main_content_area = None
        self.theme_button = None
        self.nav_container = None
        self.nav_bar_title = None
        self.perfil_button = None
        self.metas_button = None
        self.calendario_button = None

     # --- MÉTODOS HELPERS --- #

    def login_click(self, e):
        """Ação ao clicar no botão de login. Navega para o dashboard."""
       
        print("Login bem-sucedido! Navegando para o Dashboard.")
        self.menu_dashboard()

    def cadastrar_click(self, e):
        """Ação ao clicar no botão de cadastro. Abre o pop-up customizado."""
        
        print("Lógica de cadastro executada!")
        self.popup.show("Cadastro realizado com sucesso!")

    def mudar_tema(self, e):
        """Alterna o tema da página entre claro e escuro."""
        
        self.page.theme_mode = ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.theme_button.icon = ft.Icons.WB_SUNNY if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.BRIGHTNESS_2
        self.page.update()
        self.theme_button.update()

    def expand_nav_rail(self, e):

        self.nav_rail.extended= True if e.data == "true" else False

        self.nav_rail.update()

    def navigate(self, view_name: str):
        """Navega para a tela selecionada."""
        self.main_content_area.controls.clear()

        if view_name == "perfil":
            self.main_content_area.controls.append(ft.Text("Perfil do Usuário", size=30))
        elif view_name == "metas":
            self.main_content_area.controls.append(ft.Text("Metas Financeiras", size=30))
        elif view_name == "calendario":
            self.main_content_area.controls.append(ft.Text("Calendário de Gastos", size=30))
        
        self.page.update()

    # --- MÉTODOS DE CONSTRUÇÃO DE TELA ---

    def main(self, page: ft.Page):
        """Método principal que inicializa a página e a estrutura do layout."""

        self.page = page
        page.title = "Metacash - Organizador Financeiro"
        page.window.width = 1200
        page.window.height = 1000
        page.bgcolor = ft.LinearGradient(
            begin=ft.alignment.top_center, 
            end=ft.alignment.bottom_center,
            colors=["#081318", "#4a717e", "#81b5cc"]
        )
        
        page.theme_mode = ft.ThemeMode.DARK
        
        main_layout = ft.Stack(
            [
                self.main_view_container,     
                self.popup,       
            ],
            expand=True
        )
        page.add(main_layout)
        self.menu_login()

    # --- MÉTODOS DE CONSTRUÇÃO DE TELA(Login)---#
    
    def menu_login(self, e=None):
        """Constrói e exibe a tela de login dentro do container principal."""
        
        self.main_view_container.content = None
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
        logo = ft.Row(
            controls=[
                ft.Text(
                    spans=[
                        ft.TextSpan("Meta", style=ft.TextStyle(size=38, weight=ft.FontWeight.BOLD)),
                        ft.TextSpan("Cash", style=ft.TextStyle(size=42, weight=ft.FontWeight.BOLD, color="#00ff88"))
                    ],
                )
            ], alignment=ft.MainAxisAlignment.CENTER
        )

        campo_login = ft.Card(
            elevation=20, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
                        ft.TextField(label="Usuário", width=300, autofocus=True, icon=ft.Icons.PERSON),
                        ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300, icon=ft.Icons.LOCK),
                        ft.ElevatedButton(
                            "Entrar", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE),
                            on_click=self.login_click, on_hover= botao_animado
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=25, width=400, height=300, border_radius=15,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )
        
        campo_cadastro = ft.Card(
            elevation=25, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Ainda não tem uma conta?"),
                        ft.ElevatedButton(
                            "Cadastre-se", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE),
                            on_click=self.menu_cadastro, on_hover=botao_animado
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20, width=400, height=100, border_radius=15,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )

        layout = ft.Column(
            [logo, campo_login, campo_cadastro],
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=40
        )
        
        self.main_view_container.alignment = ft.alignment.center
        self.main_view_container.content = layout
        self.page.update()
        
    # --- MÉTODOS DE CONSTRUÇÃO DE TELA(Cadastro)---#
   
    def menu_cadastro(self, e=None): 
        """Constrói e exibe a tela de cadastro."""

        self.main_view_container.content = None
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, bgcolor="#06d675", icon_size=30,
            on_click=self.menu_login,
            on_hover=botao_animado
        )

        titulo = ft.Text("Criar Conta no MetaCash", size=24, weight=ft.FontWeight.BOLD)

        container_esquerda = ft.Card(
            elevation=25, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Dados da Conta", size=20, weight=ft.FontWeight.BOLD),
                        ft.Divider( thickness=1),
                        ft.TextField(label="Usuário", width=300, icon=ft.Icons.PERSON),
                        ft.TextField(label="E-mail", width=300, icon=ft.Icons.EMAIL),
                        ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300, icon=ft.Icons.LOCK),
                        ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=False, width=300, icon=ft.Icons.LOCK),
                    ],
                    spacing=15
                ),
                padding=20, width=350, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )

        container_direita = ft.Card(
            elevation=25, shadow_color="#c47ebbff",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Dados Financeiros", size=20, weight=ft.FontWeight.BOLD),
                        ft.Divider(thickness=1),
                        ft.TextField(label="Salário", width=300, prefix_text="R$"),
                        ft.TextField(label="Gastos Fixos", width=300, prefix_text="R$"),
                        ft.TextField(label="Gastos com Alimentação", width=300, prefix_text="R$"),
                        ft.TextField(label="Gastos com Transporte", width=300, prefix_text="R$"),
                        ft.TextField(label="Gastos com Lazer", width=300, prefix_text="R$"),
                        ft.Text("Preferências de Gasto (1 a 5)", size=16, weight=ft.FontWeight.BOLD),
                        ft.Divider(thickness=1),
                        ft.Row([ft.Text("Alimentação", width=120), ft.Slider(min=1, max=5, divisions=4, value=3, width=150)]),
                        ft.Row([ft.Text("Transporte", width=120), ft.Slider(min=1, max=5, divisions=4, value=3, width=150)]),
                        ft.Row([ft.Text("Lazer", width=120), ft.Slider(min=1, max=5, divisions=4, value=3, width=150)])
                    ],
                    spacing=10
                ),
                padding=20, width=350, border_radius=15, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
            )
        )
        
        botao_cadastrar = ft.ElevatedButton(
            "Cadastrar", width=300, style=ft.ButtonStyle(bgcolor="#06d675", color=ft.Colors.WHITE),
            on_click= self.cadastrar_click, on_hover=botao_animado
        )

        layout_central = ft.Row(
            controls=[container_esquerda, container_direita],
            alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, spacing=50
        )

        layout = ft.Column(
            controls=[back_button, titulo, layout_central, botao_cadastrar],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, scroll=ft.ScrollMode.AUTO
        )

        self.main_view_container.content = layout
        self.main_view_container.alignment = ft.alignment.center
        self.main_view_container.content = layout
        self.page.update()

    # --- MÉTODOS DE CONSTRUÇÃO DE TELA(Dashboard)---#
    
    def menu_dashboard(self, e=None):
        """Constrói a tela principal do Dashboard."""
        self.main_view_container.content = None
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START

        # Botão de tema é criado e armazenado na instância
        self.theme_button = ft.IconButton(
            icon=ft.Icons.BRIGHTNESS_2,
            tooltip="Mudar tema",
            on_click=self.mudar_tema
        )

        logout_button = ft.IconButton(
            icon=ft.Icons.LOGOUT,
            tooltip="Logout",
            on_click=self.menu_login
        )

        # Controles da parte inferior da barra de navegação
        trailing_controls = ft.Column(
            [self.theme_button, logout_button],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=False,
            min_width=100,
            min_extended_width=200,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            on_change=self.navigate,
            # A propriedade 'trailing' recebe os controles da parte inferior
            trailing=trailing_controls,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.PERSON_OUTLINE, 
                    selected_icon=ft.Icons.PERSON, 
                    label="Perfil"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.STAR_BORDER,
                    selected_icon=ft.Icons.STAR,
                    label="Metas",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
                    selected_icon=ft.Icons.CALENDAR_MONTH,
                    label="Calendário",
                ),
            ],
        )
        
        nav_rail_container = ft.Container(
            content=self.nav_rail,
            on_hover=self.expand_nav_rail,
            height=self.page.window.height - 50
        )
        
        self.main_content_area = ft.Column(
            [ft.Text("Bem-vindo ao MetaCash!", size=30)],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        layout = ft.Row(
            controls=[
                nav_rail_container,
                ft.VerticalDivider(width=1),
                self.main_content_area
            ],
            expand=True
        )
        
        self.main_view_container.content = layout
        self.main_view_container.alignment = ft.alignment.center
        self.main_view_container.content = layout
        self.page.update()

if __name__ == "__main__":
    app = Interface_Inicial()
    ft.app(target=app.main)