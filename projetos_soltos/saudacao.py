import flet as ft
import re

def main (page: ft.Page):
    page.title = "Sistema de Saudação"
    page.padding = 30
    
    def validar_nome(e):
        # Remove qualquer caractere que não seja letra ou espaço
        e.control.value = re.sub(r"[^a-zA-ZÀ-ÿ\s]","",e.control.value)
        e.control.update()
        
    
    campo_nome = ft.TextField(
        label="Digite o seu nome",
        hint_text="Exemplo: Érico",
        autofocus=True,
        width=400,
        on_change=validar_nome
    )
    resultado = ft.Text(value="", size=22)
    
    def saudar(e):
        nome = campo_nome.value.strip()
        if nome == "":
            resultado.value = "Digite um nome antes de continuar."
            resultado.color = ft.Colors.RED
        else:
            resultado.value = f"Olá, {nome}! Seja bem vindo a essa bagaça"
            resultado.color = ft.Colors.GREEN
            campo_nome.value = ""
    
    def limpar(e):
        campo_nome.value = ""
    
    botao = ft.FilledButton(content="Saudar",on_click=saudar)  
    botao_limpar = ft.FilledButton(content="Limpar",on_click=limpar)          
    
    page.add(
        ft.Text(
            "Saudaçao com Flet",
            size=30,
            weight=ft.FontWeight.BOLD),
        campo_nome,
        botao,
        botao_limpar,
        resultado
    )
    
if __name__ == "__main__":
    ft.run(main)