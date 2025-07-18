import flet as ft
import time

def botao_animado(e):
        e.control.bgcolor = "#143622" if e.data == "true" else "#06d675"
        e.control.update()

def criar_linha_info(icone: str, titulo: str, valor: str) -> ft.Row:
    """Cria uma linha padronizada para exibição de informações no perfil."""
    return ft.Row(
        controls=[
            ft.Icon(name=icone, color="#06d675", size=24),
            ft.Text(titulo, weight=ft.FontWeight.BOLD, size=16, width=150),
            ft.Text(valor, size=16)
        ],
        alignment=ft.MainAxisAlignment.START
    )

class PopupFeedback(ft.Container):
    """Classe que permite criar pop-ups customizados"""
    
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close = on_close

        # --- O Card do Pop-up ---
        self.message_text = ft.Text(
            value="",
            size=16,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )

        self.card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(name=ft.Icons.CHECK_CIRCLE, color="#06d675", size=50),
                    ft.Text("Tudo certo!", size=22, weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE),
                    self.message_text,
                    ft.ElevatedButton(
                        "Entendi", 
                        on_click=self._close,
                        bgcolor="#06d675",
                        color=ft.Colors.WHITE,
                        width=200,
                        on_hover=botao_animado
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            width=350,
            height=400,
            padding=30,
            bgcolor="#081318",
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color="#06d675", offset=ft.Offset(0, 4))
        )

       
        self.content = ft.Stack(
            controls=[
                
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.6, "black"),
                    expand=True,
                    on_click=self._close 
                ),
                
                ft.Container(
                    content=self.card,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )

        # Propriedades do Container principal (o Popup)
        self.visible = False
        self.opacity = 0
        self.expand = True
        self.animate_opacity = ft.Animation(300, "easeInOut")

    def show(self, message: str):
        self.message_text.value = message
        self.visible = True
        self.opacity = 1
        self.update()

    def _close(self, e=None):
        self.opacity = 0
        self.update()
        time.sleep(0.3) 
        self.visible = False
        self.update()
        if self.on_close:
            self.on_close()

texto_feedback_geral = ft.Text(
            value="",           
            color=ft.Colors.RED, 
            weight=ft.FontWeight.BOLD,
            visible=False       
        )


class PopupDeConfirmacao(ft.Container):
    """
    Classe que cria um pop-up de confirmação customizado com opções de "Sim" e "Não".
    """
    def __init__(self, on_confirm):
        super().__init__()
        self.on_confirm_callback = on_confirm
        self.visible = False
        self.opacity = 0
        self.expand = True
        self.animate_opacity = ft.Animation(300, "easeInOut")

        self.title = ft.Text(size=22, weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE)
        self.content_text = ft.Text(size=16, text_align=ft.TextAlign.CENTER,color=ft.Colors.WHITE)

        self.card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=50),
                    self.title,
                    self.content_text,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Não, cancelar",
                                on_click=self._close,
                                bgcolor=ft.Colors.GREY_700,
                                color=ft.Colors.WHITE,
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                "Sim, deletar",
                                on_click=self._handle_confirm,
                                bgcolor=ft.Colors.RED_700,
                                color=ft.Colors.WHITE,
                                expand=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            height=350,
            width=400,
            padding=30,
            bgcolor="#081318",
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.RED_900, offset=ft.Offset(0, 4))
        )

        self.content = ft.Stack(
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.6, "black"),
                    expand=True,
                    on_click=self._close
                ),
                ft.Container(
                    content=self.card,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )

    def show(self, title: str, content: str):
        self.title.value = title
        self.content_text.value = content
        self.visible = True
        self.opacity = 1
        if self.page:
            self.page.update()

    def _close(self, e=None):
        self.opacity = 0
        self.update()
        time.sleep(0.3)
        self.visible = False
        self.update()

    def _handle_confirm(self, e):
        self._close()
        if self.on_confirm_callback:
            self.on_confirm_callback(e)

class PopupInput(ft.Container):
    """
    Cria um pop-up customizado com um campo de texto para entrada de dados.
    """
    def __init__(self, on_save):
        super().__init__()
        self.on_save_callback = on_save
        self.visible = False
        self.opacity = 0
        self.expand = True
        self.animate_opacity = ft.Animation(300, "easeInOut")

        self.title = ft.Text(size=22, weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE)
        self.input_field = ft.TextField(
            label="Valor",
            prefix_text="R$",
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True,
            color=ft.Colors.WHITE
        )

        self.card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(name=ft.Icons.EDIT_NOTE, color="#06d675", size=50),
                    self.title,
                    self.input_field,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Cancelar", on_click=self.close,
                                bgcolor=ft.Colors.GREY_700, color=ft.Colors.WHITE, expand=True
                            ),
                            ft.ElevatedButton(
                                "Salvar", on_click=self._handle_save,
                                bgcolor="#06d675", color=ft.Colors.WHITE, expand=True
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            height=350,
            width=400,
            padding=30,
            bgcolor="#081318",
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color="#06d675", offset=ft.Offset(0, 4))
        )

        self.content = ft.Stack(
            controls=[
                ft.Container(bgcolor=ft.Colors.with_opacity(0.6, "black"), expand=True, on_click=self.close),
                ft.Container(content=self.card, alignment=ft.alignment.center, expand=True)
            ]
        )

    def show(self, title: str, label: str = "Valor"):
        """Mostra o pop-up, limpando os campos anteriores."""
        self.title.value = title
        self.input_field.label = label
        self.input_field.value = ""
        self.input_field.error_text = None
        self.visible = True
        self.opacity = 1
        self.update()
        self.input_field.focus()

    def close(self, e=None):
        """Fecha o pop-up com uma animação."""
        self.opacity = 0
        self.update()
        time.sleep(0.3)
        self.visible = False
        self.update()

    def _handle_save(self, e):
        """Chama o callback de salvamento, passando a si mesmo como argumento."""
        if self.on_save_callback:
            self.on_save_callback(self)