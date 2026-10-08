import flet as ft
def main(page: ft.Page):
    page.title = "FastSaver"
    page.bgcolor = "#f5f5f5"
    def make_card(t,s,p):
        return ft.Container(content=ft.Column([ft.Icon(ft.icons.SHOPPING_BAG,size=40),ft.Text(t,weight="bold",color="black"),ft.Text(s,size=12,color="grey"),ft.Text(p,weight="bold",color="green")]),padding=12,bgcolor="white",border_radius=12,width=170)
    top=ft.Container(content=ft.Text("Durban Hustle",size=20,weight="bold",color="white"),bgcolor="#00c853",padding=20,border_radius=12)
    row1=ft.Row([make_card("Toiletries","Soap & Lotion","R49"),make_card("Cereal","Food","R35")],scroll="auto")
    row2=ft.Row([make_card("Sofa","Comfortable","R2500"),make_card("Maize","10kg","R120")],scroll="auto")
    col=ft.Column([top,ft.Text("Today's Deals",size=18,weight="bold",color="black"),row1,row2],spacing=15,scroll="auto",expand=True)
    page.add(col)
ft.app(target=main)