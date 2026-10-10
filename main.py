import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver"
    page.bgcolor = "#FFFFFF"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    page.add(
        ft.Column([
            ft.Icon(ft.Icons.DOWNLOAD_ROUNDED, size=60, color="blue"),
            ft.Text("FastSaver", size=32, weight="bold"),
            ft.Text("App Works! Build is Fixed", size=16, color="grey"),
            ft.ElevatedButton(
                "CLICK ME - APP WORKS!",
                bgcolor="blue",
                color="white",
                width=250,
                height=50
            ),
        ], 
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
