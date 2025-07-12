import flet as ft

def botao_animado(e):
        e.control.bgcolor = "#143622" if e.data == "true" else "#06d675"
        e.control.update()

