import flet as ft
import webbrowser

def main(page: ft.Page):
    page.title = "Sandile App"
    page.bgcolor = "#1A202C"
    page.padding = 0
    page.scroll = "auto"

    def whatsapp_082(e):
        webbrowser.open("https://wa.me/27823497049?text=Hello%20Sandile%20I%20want%20to%20buy%20from%20Durban%20Cheap%20Finds")

    def whatsapp_083(e):
        # THIS IS BAYANDA XIMBA NUMBER - NOW ACTIVATED!
        webbrowser.open("https://wa.me/27832927584?text=Hello%20Bayanda%20Ximba%20I%20want%20XIMBA%20CULTURAL%20WEAR%20R300")

    def close_big(e):
        overlay.visible = False
        page.update()

    def view_big(e):
        overlay.visible = True
        page.update()

    top_banner = ft.Container(
        bgcolor="#FFD700",
        padding=10,
        content=ft.Text("082 349 7049 | Pinetown | Durban | PMB", color="black", weight="bold", size=14)
    )

    clicked_banner = ft.Container(
        bgcolor="#1A202C",
        padding=12,
        content=ft.Column([
            ft.Text("YOU CLICKED: XIMBA CULTURAL WEAR", color="#68D391", weight="bold", size=15),
            ft.Text("Call: 082 349 7049", color="#68D391", weight="bold", size=13),
            ft.Text("From R10 - Less than R1000", color="#68D391", weight="bold", size=13),
        ], spacing=3)
    )

    big_img = ft.Image(src="ximba.jpg", width=380, height=600)
    overlay = ft.Container(
        visible=False,
        bgcolor="black",
        padding=10,
        content=ft.Column([
            ft.TextButton("X CLOSE - Click to go back", on_click=close_big),
            big_img,
            ft.Text("XIMBA CULTURAL WEAR - R300", color="white", weight="bold", size=18),
            ft.TextButton("WHATSAPP BAYANDA 083 292 7584 - ORDER NOW", on_click=whatsapp_083),
        ], scroll="auto")
    )

    def card1():
        return ft.Container(
            bgcolor="#2D3748",
            padding=12,
            on_click=view_big,
            content=ft.Row([
                ft.Image(src="ximba.jpg", width=50, height=50),
                ft.Column([
                    ft.Text("Male & Female Clothes - All Sizes", color="white", weight="bold", size=12),
                    ft.Text("Men, Women, Kids - All sizes", color="white", size=10),
                    ft.Text("New Germany | Pinetown | Durban | PMB", color="#ECC94B", size=9),
                    ft.TextButton("From R10 - 082 349 7049 - TAP TO VIEW", on_click=view_big),
                ], spacing=2)
            ])
        )

    def card2():
        return ft.Container(
            bgcolor="#2D3748",
            padding=12,
            content=ft.Row([
                ft.Image(src="ximba.jpg", width=50, height=50),
                ft.Column([
                    ft.Text("XIMBA CULTURAL WEAR", color="white", weight="bold", size=12),
                    ft.Text("T-SHIRTS - Wear Your Heritage | PAXI | By Bayanda", color="white", size=9),
                    ft.Text("New Germany | Pinetown | Durban | PMB", color="#ECC94B", size=9),
                    # NOW BOTH NUMBERS ARE BUTTONS!
                    ft.Row([
                        ft.TextButton("R300 - 083 292 7584 WHATSAPP", on_click=whatsapp_083),
                    ]),
                    ft.Row([
                        ft.TextButton("VIEW BIG IMAGE", on_click=view_big),
                        ft.TextButton("082 349 7049", on_click=whatsapp_082),
                    ])
                ], spacing=2)
            ])
        )

    def card_other(title, sub, price, whatsapp_func):
        return ft.Container(
            bgcolor="#2D3748",
            padding=10,
            content=ft.Column([
                ft.Text(title, color="white", weight="bold", size=11),
                ft.Text(sub, color="white", size=9),
                ft.Text("New Germany | Pinetown | Durban | PMB", color="#ECC94B", size=9),
                ft.TextButton(price, on_click=whatsapp_func),
            ], spacing=2)
        )

    main_col = ft.Column([
        top_banner,
        clicked_banner,
        card1(),
        card2(),
        card_other("Toiletries - Soap & Lotion", "New, unopened", "From R15 - 082 349 7049", whatsapp_082),
        card_other("All Kinds of Cereal & Food", "Groceries", "From R20 - 082 349 7049", whatsapp_082),
        card_other("Sofa 2 seater", "Good condition", "R1200 - 082 349 7049", whatsapp_082),
    ], spacing=8)

    page.add(ft.Stack([main_col, overlay]))

ft.run(main, assets_dir="assets")