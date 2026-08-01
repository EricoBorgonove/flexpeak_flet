import flet as ft

def main(page: ft.Page):
    page.title = "Hello Flet"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.spacing = 20
    
    mensagem = ft.Text("O Botão ainda não foi clicado.")

    def clicou(e):
        print("Cliquei!")
    def clicou_mensagem(e):
        mensagem.value = "Você clicou no botão"

    page.add(
        mensagem,
        ft.Text("Curso Flet", size=30, weight=ft.FontWeight.BOLD),
        ft.Button(content="Clique",on_click=clicou ),
        ft.FilledButton(content="Clique aqui", on_click=clicou_mensagem)
    )
#ft.app(target=main)

if __name__ == "__main__":
    ft.run(main)
    
