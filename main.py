import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver"
    page.add(ft.Text("HELLO FASTSAVER WORKS", size=30))

ft.app(target=main)
