import asyncio
import random

import flet as ft


LINHAS = 20
COLUNAS = 20
VELOCIDADE_INICIAL = 0.18
VELOCIDADE_MINIMA = 0.07

DIRECOES = {
    "arrowup": (-1, 0),
    "w": (-1, 0),
    "arrowdown": (1, 0),
    "s": (1, 0),
    "arrowleft": (0, -1),
    "a": (0, -1),
    "arrowright": (0, 1),
    "d": (0, 1),
}


def main(page: ft.Page):
    page.title = "Snake com Python e Flet"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 18
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {
        "cobra": [],
        "direcao": (0, 1),
        "proxima_direcao": (0, 1),
        "comida": (8, 14),
        "pontos": 0,
        "recorde": 0,
        "rodando": False,
        "sessao": 0,
    }

    texto_pontos = ft.Text("Pontos: 0", size=20, weight=ft.FontWeight.BOLD)
    texto_recorde = ft.Text("Recorde: 0", size=20)
    texto_status = ft.Text(
        "Pressione INICIAR. Use as setas ou W, A, S, D.",
        color=ft.Colors.BLUE_100,
    )

    celulas = [
        ft.Container(
            bgcolor=ft.Colors.BLUE_GREY_800,
            border_radius=ft.BorderRadius.all(3),
            alignment=ft.Alignment.CENTER,
        )
        for _ in range(LINHAS * COLUNAS)
    ]

    tabuleiro = ft.GridView(
        width=421,
        height=421,
        runs_count=COLUNAS,
        child_aspect_ratio=1.0,
        spacing=1,
        run_spacing=1,
        padding=0,
        controls=celulas,
    )

    def indice(posicao):
        linha, coluna = posicao
        return linha * COLUNAS + coluna

    def desenhar():
        """Transforma o estado lógico em cores no tabuleiro."""
        for celula in celulas:
            celula.bgcolor = ft.Colors.BLUE_GREY_800
            celula.content = None

        if estado["comida"] is not None:
            celula_comida = celulas[indice(estado["comida"])]
            celula_comida.bgcolor = ft.Colors.RED_600
            celula_comida.content = ft.Text(
                "●",
                size=12,
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
            )

        for parte in estado["cobra"][1:]:
            celulas[indice(parte)].bgcolor = ft.Colors.GREEN_600

        if estado["cobra"]:
            celulas[indice(estado["cobra"][0])].bgcolor = ft.Colors.LIGHT_GREEN_300

        texto_pontos.value = f"Pontos: {estado['pontos']}"
        texto_recorde.value = f"Recorde: {estado['recorde']}"
        page.update()

    def sortear_comida():
        """Sorteia uma coordenada que não esteja ocupada pela cobra."""
        ocupadas = set(estado["cobra"])
        livres = [
            (linha, coluna)
            for linha in range(LINHAS)
            for coluna in range(COLUNAS)
            if (linha, coluna) not in ocupadas
        ]
        return random.choice(livres) if livres else None

    def direcao_oposta(direcao_a, direcao_b):
        return direcao_a[0] + direcao_b[0] == 0 and direcao_a[1] + direcao_b[1] == 0

    def mudar_direcao(nova_direcao):
        """Impede a cobra de inverter diretamente sobre o próprio corpo."""
        if estado["rodando"] and not direcao_oposta(nova_direcao, estado["direcao"]):
            estado["proxima_direcao"] = nova_direcao

    def tratar_tecla(e):
        tecla = str(e.key).replace(" ", "").lower()
        if tecla in DIRECOES:
            mudar_direcao(DIRECOES[tecla])

    def encerrar(mensagem):
        estado["rodando"] = False
        estado["recorde"] = max(estado["recorde"], estado["pontos"])
        texto_status.value = mensagem
        texto_status.color = ft.Colors.RED_300
        botao_iniciar.content = "JOGAR NOVAMENTE"
        botao_iniciar.icon = ft.Icons.REPLAY
        botao_iniciar.disabled = False
        desenhar()

    def mover_cobra():
        """Executa um passo e devolve False quando a rodada terminar."""
        estado["direcao"] = estado["proxima_direcao"]
        cabeca_linha, cabeca_coluna = estado["cobra"][0]
        delta_linha, delta_coluna = estado["direcao"]
        nova_cabeca = (
            (cabeca_linha + delta_linha) % LINHAS,
            (cabeca_coluna + delta_coluna) % COLUNAS,
        )

        vai_comer = nova_cabeca == estado["comida"]
        corpo_que_permanece = estado["cobra"] if vai_comer else estado["cobra"][:-1]

        if nova_cabeca in corpo_que_permanece:
            encerrar("Fim de jogo: a cobra bateu no próprio corpo.")
            return False

        estado["cobra"].insert(0, nova_cabeca)

        if vai_comer:
            estado["pontos"] += 10
            estado["recorde"] = max(estado["recorde"], estado["pontos"])
            estado["comida"] = sortear_comida()

            if estado["comida"] is None:
                encerrar("Você venceu: todo o tabuleiro foi ocupado!")
                return False
        else:
            estado["cobra"].pop()

        desenhar()
        return True

    async def loop_do_jogo(sessao_atual):
        """Mantém o jogo avançando sem bloquear a interface."""
        while estado["rodando"] and estado["sessao"] == sessao_atual:
            velocidade = max(
                VELOCIDADE_MINIMA,
                VELOCIDADE_INICIAL - estado["pontos"] * 0.0015,
            )
            await asyncio.sleep(velocidade)

            if estado["rodando"] and estado["sessao"] == sessao_atual:
                if not mover_cobra():
                    break

    async def iniciar_jogo(e):
        estado["sessao"] += 1
        estado["cobra"] = [(10, 8), (10, 7), (10, 6)]
        estado["direcao"] = (0, 1)
        estado["proxima_direcao"] = (0, 1)
        estado["pontos"] = 0
        estado["comida"] = sortear_comida()
        estado["rodando"] = True

        texto_status.value = "Jogo em andamento!"
        texto_status.color = ft.Colors.GREEN_300
        botao_iniciar.disabled = True
        desenhar()

        await teclado.focus()
        page.run_task(loop_do_jogo, estado["sessao"])

    def botao_direcao(direcao, icone):
        return ft.IconButton(
            icon=icone,
            icon_size=26,
            on_click=lambda e: mudar_direcao(direcao),
        )

    botao_iniciar = ft.Button(
        content="INICIAR",
        icon=ft.Icons.PLAY_ARROW,
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        on_click=iniciar_jogo,
    )

    controles_direcao = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        controls=[
            botao_direcao((-1, 0), ft.Icons.KEYBOARD_ARROW_UP),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=26,
                controls=[
                    botao_direcao((0, -1), ft.Icons.KEYBOARD_ARROW_LEFT),
                    botao_direcao((1, 0), ft.Icons.KEYBOARD_ARROW_DOWN),
                    botao_direcao((0, 1), ft.Icons.KEYBOARD_ARROW_RIGHT),
                ],
            ),
        ],
    )

    conteudo = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Text(
                "SNAKE",
                size=34,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.LIGHT_GREEN_300,
            ),
            ft.Row(
                width=421,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[texto_pontos, texto_recorde],
            ),
            ft.Container(
                bgcolor=ft.Colors.BLACK,
                border=ft.Border.all(3, ft.Colors.GREEN_400),
                border_radius=ft.BorderRadius.all(8),
                padding=4,
                content=tabuleiro,
            ),
            texto_status,
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=24,
                controls=[botao_iniciar, controles_direcao],
            ),
        ],
    )

    teclado = ft.KeyboardListener(
        autofocus=True,
        on_key_down=tratar_tecla,
        content=conteudo,
    )

    page.add(ft.SafeArea(content=teclado))
    desenhar()


if __name__ == "__main__":
    ft.run(main)
