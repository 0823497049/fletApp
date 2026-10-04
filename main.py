import flet as ft

def main(page: ft.Page):
    page.bgcolor = "#0A0A0A"
    page.scroll = ft.ScrollMode.AUTO
    
    status = ft.Text("", size=16, color="#00FF00", weight="bold")

    def get_item(e, title):
        status.value = f"✅ YOU CLICKED: {title}\n📞 Call: 082 349 7049\n💰 From R10 - Less than R1000"
        page.update()

    def cheap_card(title, desc, price, icon):
        return ft.Container(
            bgcolor="#1A1A1A",
            padding=15,
            margin=ft.Margin(15, 0, 15, 10),
            border_radius=10,
            on_click=lambda e: get_item(e, title),
            content=ft.Row([
                ft.Text(icon, size=30),
                ft.Column([
                    ft.Text(title, weight="bold", color="white"),
                    ft.Text(desc, size=12, color="grey"),
                    ft.Text("📍 New Germany | Pinetown | Durban | PMB", size=11, color="#FFD700"),
                    ft.Text(f"{price} 📞 082 349 7049", size=12, color="#00FF00", weight="bold"),
                ], expand=True)
            ])
        )

    header = ft.Container(
        bgcolor="#FFD700",
        padding=20,
        content=ft.Text("CHEAP KASI\n💰 From R10 - Less than R1000\nNew Germany | Pinetown | Durban | PMB\n📞 082 349 7049", size=18, weight="bold", color="black")
    )

    page.add(
        header,
        ft.Container(padding=10, content=status, bgcolor="black"),
        cheap_card("Male & Female Clothes - All Sizes", "Men, Women, Kids - All sizes", "From R10", "👕"),
        cheap_card("Toiletries - Soap & Lotion", "New, unopened", "From R15", "🧴"),
        cheap_card("All Kinds of Cereal & Food", "Rice, Maize, Cereal, Tinned food", "From R20", "🥣"),
        cheap_card("Sofa 2 seater", "Good condition", "R800 - Less than R1000", "🛋️"),
        cheap_card("Kids School Shoes", "All sizes", "From R50", "👟"),
        cheap_card("Haircuts for Kids", "Sunday special", "From R30", "💈"),
        cheap_card("Plastic Chairs x4", "Party chairs", "From R100", "🪑"),
    )

ft.run(main)