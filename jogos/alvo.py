import random
import time
import flet as ft

LARGURA_AREA = 620
ALTURA_AREA = 380
TAMANHO_ALVO = 70
TOTAL_ACERTOS = 10

def main (page: ft.Page):
    page.title = "Caça ao Alvo"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLUE_900
    page.padding = 24
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    estado = {
        "jogando": False,
        "pontos": 0,
        "inicio": 0.0,
    }
    
    placar = ft.Text (
        value=f"Pontos : 0 / {TOTAL_ACERTOS}",
        size = 22,
        weight= ft.FontWeight.BOLD,
    )
    mensagem = ft.Text(
        value="Clique em INICIAR e encontre o alvo !",
        size = 16,
        color=ft.Colors.BLUE_100,
    )
    def mover_alvo():
        alvo.left = random.randint(0, LARGURA_AREA - TAMANHO_ALVO)
        alvo.top = random.randint(0, ALTURA_AREA - TAMANHO_ALVO)
        
    def acertar_alvo(e):
        if not estado["jogando"]:
            return
        estado["pontos"] += 1
        placar.value = f"Pontos : {estado['pontos']} / {TOTAL_ACERTOS}"
        
        if estado["pontos"] == TOTAL_ACERTOS:
            estado["jogando"] = False
            alvo.visible = False
            botao_iniciar.disabled = False
            tempo_total = time.monotonic() - estado["inicio"]
            mensagem.value = f"Parabéns! Você terminou em {tempo_total:.2f} segundos."
            mensagem.color = ft.Colors.GREEN_300
        else:
            mover_alvo()
            mensagem.value = "Boa! Continue procurando."
        
        page.update()
        
    def iniciar_jogo(e):
        estado["jogando"]= True
        estado["pontos"] = 0
        estado["inicio"] = time.monotonic()
        
        placar.value=f"Pontos : 0 / {TOTAL_ACERTOS}"
        mensagem.value = "Valendo !!"
        mensagem.color = ft.Colors.AMBER_300
        alvo.visible = True
        botao_iniciar.disabled = True
        mover_alvo()
        page.update()
        
    alvo = ft.Button(
        content= "🎯",
        width=TAMANHO_ALVO,
        height=TAMANHO_ALVO,
        left=20,
        top=20,
        visible=False,
        bgcolor=ft.Colors.RED_700,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.CircleBorder()),
        on_click=acertar_alvo,
    )
    area_jogo = ft.Container(
        width=LARGURA_AREA,
        height=ALTURA_AREA,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border=ft.Border.all(2,ft.Colors.BLUE_300),
        border_radius=ft.BorderRadius.all(16),
        content=ft.Stack(
            width=LARGURA_AREA,
            height=ALTURA_AREA,
            controls=[alvo],
        ),
    )
    botao_iniciar = ft.Button(
        content="INICIAR JOGO",
        icon=ft.Icons.PLAY_ARROW,
        bgcolor= ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        on_click=iniciar_jogo,
    )
    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                controls=[
                    ft.Text(
                        "CAÇA AO ALVO",
                        size = 32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.AMBER_300,
                    ),
                    ft.Text("Clique 10 vezes no alvo no menor tempo possível"),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        width=LARGURA_AREA,
                        controls=[placar,botao_iniciar],
                    ),
                    area_jogo,
                    mensagem,
                ],
            )
        )
    )
        
if __name__ == "__main__":
    ft.run(main)