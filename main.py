import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    link_input = ft.TextField(
        label="Paste TikTok / Instagram Link",
        width=320,
        autofocus=True
    )
    
    status = ft.Text("", size=16, color=ft.Colors.GREEN)

    def download_click(e):
        if link_input.value == "":
            status.value = "Please paste a link first!"
            status.color = ft.Colors.RED
        else:
            status.value = f"Link received: {link_input.value[:30]}... Ready to download!"
            status.color = ft.Colors.GREEN
        page.update()

    page.add(
        ft.Text("FastSaver", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Download videos fast", size=16, color=ft.Colors.GREY),
        ft.Container(height=20),
        link_input,
        ft.Container(height=10),
        ft.ElevatedButton("DOWNLOAD", width=320, height=50, on_click=download_click),
        ft.Container(height=20),
        status
    )

ft.app(target=main)
