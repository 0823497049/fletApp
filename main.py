import flet as ft

def main(page: ft.Page):
    page.title = "FastSaver - Durban Hustle"
    page.bgcolor = "#f5f5f5"
    page.theme_mode = ft.ThemeMode.LIGHT

    def make_card(title, sub, price):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    height=100,
                    bgcolor="#e0e0e0",
                    content=ft.Icon(ft.icons.SHOPPING_BAG, size=40, color="grey"),
                    alignment=ft.alignment.center,
                    border_radius=8
                ),
                ft.Text(title, weight="bold", size=14, color="black"),
                ft.Text(sub, size=12, color="grey"),
                ft.Text(price, weight="bold", color="green", size=14),
                ft.ElevatedButton("View", bgcolor="#00c853", color="white")
            ], spacing=6),
            padding=12,
            bgcolor="white",
            border_radius=12,
            width=170,
            shadow=ft.BoxShadow(blur_radius=4, color="#33000000")
        )

    top_banner = ft.Container(
        content=ft.Text("Durban Hustle Marketplace", size=20, weight="bold", color="white"),
        bgcolor="#00c853",
        padding=20,
        border_radius=12
    )

    row1 = ft.Row([make_card("Toiletries", "Soap & Lotion", "R49"), make_card("Cereal", "All Kinds Food", "R35")], scroll="auto")
    row2 = ft.Row([make_card("Sofa 2 seater", "Comfortable", "R2500"), make_card("Maize Meal", "10kg Bag", "R120")], scroll="auto")

    main_col = ft.Column([
        top_banner,
        ft.Text("Today's Deals", size=18, weight="bold", color="black"),
        row1,
        row2,
        ft.Text("App fixed! No more black screen", color="black")
    ], spacing=15, scroll="auto", expand=True)

    page.add(main_col)

ft.app(target=main)