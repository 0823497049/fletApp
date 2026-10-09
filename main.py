import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver"
    page.bgcolor = ft.Colors.WHITE
    page.scroll = "auto"
    
    page.appbar = ft.AppBar(
        title=ft.Text("FastSaver Marketplace", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.BLUE_700,
    )
    
    url_input = ft.TextField(
        label="Paste Instagram/TikTok Link",
        border_radius=10,
        prefix_icon=ft.Icons.LINK,
    )
    
    status = ft.Text("Ready to download", color=ft.Colors.GREY)
    
    def download_click(e):
        if not url_input.value:
            status.value = "Please paste a link!"
            status.color = ft.Colors.RED
            page.update()
            return
        status.value = f"Downloading: {url_input.value[:30]}..."
        status.color = ft.Colors.BLUE
        page.update()
        # Add your download logic here
    
    download_btn = ft.ElevatedButton(
        "DOWNLOAD NOW",
        icon=ft.Icons.DOWNLOAD,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        on_click=download_click,
        width=300,
        height=50,
    )
    
    marketplace = ft.Column([
        ft.Text("🔥 Trending Templates", size=20, weight="bold"),
        ft.Row([
            ft.Card(content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.VIDEO_LIBRARY, size=40, color=ft.Colors.BLUE),
                    ft.Text("Viral Template 1"),
                    ft.Text("R100", weight="bold", color=ft.Colors.GREEN),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=20, width=150, height=150
            )),
            ft.Card(content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.VIDEO_LIBRARY, size=40, color=ft.Colors.PURPLE),
                    ft.Text("Viral Template 2"),
                    ft.Text("R250", weight="bold", color=ft.Colors.GREEN),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=20, width=150, height=150
            )),
        ], scroll="auto")
    ])
    
    page.add(
        ft.Column([
            url_input,
            download_btn,
            status,
            ft.Divider(),
            marketplace,
        ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
