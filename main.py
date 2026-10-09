import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver"
    page.bgcolor = ft.Colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    url_input = ft.TextField(
        label="Paste Link",
        width=350,
        border_radius=10,
        prefix_icon=ft.Icons.LINK
    )
    
    status = ft.Text("Ready", color=ft.Colors.GREY)
    
    def download_click(e):
        if not url_input.value:
            status.value = "Paste link first!"
            status.color = ft.Colors.RED
        else:
            status.value = "Downloading..."
            status.color = ft.Colors.BLUE
        page.update()
    
    download_btn = ft.ElevatedButton(
        "DOWNLOAD",
        icon=ft.Icons.DOWNLOAD,
        on_click=download_click,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        width=350
    )
    
    marketplace = ft.Column([
        ft.Text("Marketplace", size=22, weight="bold"),
        ft.Text("R100 Templates - Coming Soon", color=ft.Colors.GREEN)
    ])
    
    page.add(
        ft.Column([
            ft.Icon(ft.Icons.VIDEO_LIBRARY, size=60, color=ft.Colors.BLUE),
            ft.Text("FastSaver", size=30, weight="bold"),
            url_input,
            download_btn,
            status,
            ft.Divider(),
            marketplace
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )
