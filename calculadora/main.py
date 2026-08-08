import flet as ft


def main (page: ft.Page):
    #Configurações da página
    page.title = "Calculadora"
    page.padding = 5
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    #Visor da Calculadora
    visor = ft.TextField(
        value = "",
        width = 320,
        height = 70,
        text_align = ft.TextAlign.RIGHT,
        text_size= 28,
        read_only= True,
    )
    # Função executada ao clicar em numeros ou operaçoes
    def clicar (e):
        valor = e.control.content
        
        #se estiver mostrando erro, limpa antes de continuar
        if visor.value == "Erro":
            visor.value = ""
            
        visor.value += valor
        page.update()

    #limpa todo o visor
    def limpar(e):
        visor.value = ""
        page.update()
        
    #Apaga o ultimo caractere
    def apagar (e):
        visor.value = visor.value[:-1]
        page.update()
        
    #Calcular o resultado
    def calcular(e):
        try:
            expressao = visor.value
        
            #Converte os simbulos visuais
            expressao = expressao.replace ("x", "*")
            expressao = expressao.replace ("÷", "/")
            
            resultado = eval(expressao)

            #evita mostrar 10.0 quando é 10
            if isinstance(resultado,float) and resultado.is_integer():
                resultado = int(resultado)
                
            visor.value = str(resultado)
        except:
            visor.value = "Error"
            
        page.update()
        
        #Função para criar botoes
    def criar_botao (texto, funcao=clicar):
        return ft.ElevatedButton(
            content = texto,
            width= 70,
            height= 60,
            on_click= funcao
        )
    
    #Primerira linha
    linha1 = ft.Row(
        controls =[
            criar_botao("C", limpar),
            criar_botao("←", apagar),
            criar_botao("÷"),
            criar_botao("x"),
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )
    #Segunda linha
    linha2 = ft.Row(
        controls =[
            criar_botao("7"),
            criar_botao("8"),
            criar_botao("9"),
            criar_botao("-"),
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )        
    #Terceira linha
    linha3 = ft.Row(
        controls =[
            criar_botao("4"),
            criar_botao("5"),
            criar_botao("6"),
            criar_botao("+"),
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )           
    #Quarta linha
    linha4 = ft.Row(
        controls =[
            criar_botao("1"),
            criar_botao("2"),
            criar_botao("3"),
            criar_botao("=", calcular),
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )   
    #Quinta linha
    linha5 = ft.Row(
        controls =[
            criar_botao("0"),
            criar_botao("."),
            criar_botao("("),
            criar_botao(")"),
        ],
        alignment = ft.MainAxisAlignment.CENTER
    )   
        # Adiciona tudo a página
    page.add(visor,linha1,linha2,linha3,linha4,linha5)
        
if __name__ == "__main__":
    ft.run(main)       