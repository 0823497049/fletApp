import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver"
    page.add(
        ft.Column([
            ft.Text("FastSaver WORKS!", size=30, weight="bold", color="blue"),
            ft.Text("Build #25 is alive!", size=20),
            ft.ElevatedButton("Test Button", on_click=lambda e: print("Clicked!")),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
