import flet as ft
import time

def botao_animado(e):
        e.control.bgcolor = "#143622" if e.data == "true" else "#06d675"
        e.control.update()


class Popup(ft.Container):
    """Classe que permite criar pop-ups customizados"""
    
    def __init__(self, on_close=None):
        super().__init__()
        self.on_close = on_close

        # --- O Card do Pop-up ---
        self.message_text = ft.Text(
            value="",
            size=16,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD
        )

        self.card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(name=ft.Icons.CHECK_CIRCLE, color="#06d675", size=50),
                    ft.Text("Tudo certo!", size=22, weight=ft.FontWeight.BOLD),
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
            width=300,
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
