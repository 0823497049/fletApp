import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver"
    page.bgcolor = "#f5f5f5"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    def make_card(title, sub, price):
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SHOPPING_BAG, size=40, color="grey"),
                ft.Text(title, weight=ft.FontWeight.BOLD, size=14, color="black"),
                ft.Text(sub, size=12, color="grey"),
                ft.Text(price, weight=ft.FontWeight.BOLD, color="green", size=14),
            ], spacing=5),
            padding=12,
            bgcolor="white",
            border_radius=12,
            width=170,
        )

    top = ft.Container(
        content=ft.Text("Durban Hustle Marketplace", size=20, weight=ft.FontWeight.BOLD, color="white"),
        bgcolor="#00C853",
        padding=20,
        border_radius=12,
    )

    page.add(
        ft.Column([
            top,
            ft.Text("Today's Deals", size=18, weight=ft.FontWeight.BOLD, color="black"),
            ft.Row([make_card("Toiletries","Soap & Lotion","R49"), make_card("Cereal","Food","R35")], scroll=ft.ScrollMode.AUTO),
            ft.Row([make_card("Sofa","Comfortable","R2500"), make_card("Maize","10kg","R120")], scroll=ft.ScrollMode.AUTO),
        ], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
    )