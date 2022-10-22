import Pesquisador
import time
from selenium.common.exceptions import WebDriverException
import texto_progresso
import os

"""
Comandos do Terminal:

iniciar (referente ao arquivo "Pesquisador.py");
pesquisar <palavra> (referente ao arquivo "Pesquisador.py"), podendo <palavra> conter espaços;
sair (referente ao arquivo "Pesquisador.py");
pesquisa múltipla | pesquisa mais duma palavra;
teste (referente ao arquivo "Pesquisador.py") | Testa o Pesquisador;
/? OU ? OU -? OU ajuda OU help | invocam o comando de ajuda.

"""


class PesquisadorTerminal:
    def __init__(self):
        self.terminal_laco = False
        self.pesquisador_iniciado = False

    def comecar_terminal(self):
        self.terminal_laco = True

        while self.terminal_laco:
            entrada: str = input(">: ")  # Para o usuário digitar um comando

            self.interpretar_entrada(entrada)

    def interpretar_entrada(self, entrada: str):
        if len(entrada.split()) == 0:
            print("Comando não identificado. Para ver os comandos disponíveis, digitar \"ajuda\".")
            return

        comando = entrada.split()[0]
        argumentos = "".join(entrada.split()[1:])

        if comando == "iniciar":
            self.iniciar_pesquisador()
        elif comando in {"pesquisar", "p"}:
            self.pesquisar(argumentos)
        elif comando in {"pesquisa-multipla", "pm"}:
            self.pesquisar_multipla(argumentos)
        elif comando == "teste":
            self.teste()
        elif comando in {"clear", "cls", "limpar"}:
            self.limpar_terminal()
        elif comando == "sair":
            self.sair()
        elif comando in {"/?", "-?", "ajuda", "help"}:
            print("""Comandos do Terminal:
            iniciar | Inicia o 'Pesquisador';
            pesquisar OU p <palavra> | Pesquisa a <palavra> para dizer se conta ou não no vocabulário da ABL;
            pesquisa-multipla OU pm <palavra1>, <palavra2> | Pesquisa 1 ou mais palavras;
            sair | Fecha o 'Pesquisador' e o Terminal;
            teste | Testa o Pesquisador
            /? OU ? OU -? OU ajuda OU help | Abrem a ajuda do Terminal.""")
        else:
            print("Comando não identificado. Para ver os comandos disponíveis, digitar \"ajuda\"")

    def iniciar_pesquisador(self):
        """Iniciar o pesquisador."""

        texto_carregamento = texto_progresso.TextoCarregamento()
        texto_carregamento.comecar("Iniciando pesquisador")

        if not self.pesquisador_iniciado:
            try:
                Pesquisador.iniciar()
                texto_carregamento.terminar()
            except WebDriverException:
                texto_carregamento.terminar()
                print("O pesquisador não pôde ser iniciado. O chrome driver não pôde ser encontrado.")

            self.pesquisador_iniciado = True
        else:
            print("O Pesquisador já está iniciado.")

    def pesquisar(self, palavra: str):
        if not self.pesquisador_iniciado:
            print("O Pesquisador deve ser iniciado. Para iniciá-lo, digitar \"iniciar\".")
            return
        elif len(palavra.split()) == 0:
            print("O comando \"pesquisar <palavra>\" precisa de uma palavra.")
            return

        resultado = Pesquisador.pesquisar(palavra)

        if resultado:
            print(f"\"{palavra}\" consta no vocabulário da ABL.")
        else:
            print(f"\"{palavra}\" não consta no vocabulário da ABL.")

    def pesquisar_multipla(self, palavras_str: str):
        if not self.pesquisador_iniciado:
            print("O Pesquisador precisa ser iniciado. Para iniciá-lo, digitar \"iniciar\".")
            return
        elif len(palavras_str.split()) == 0:
            print("O comando \"pm <palavra1>; <palavra2>\" precisa de pelo menos uma palavra.")
            return

        palavras: list[str] = palavras_str.split(",")
        # Remove espaços desnecessários terminais: " eu sei   " -> "eu sei", mas "eu  sei" -> "eu  sei".
        for indice in range(0, len(palavras)):
            palavras[indice] = palavras[indice].strip()

        # A pesquisa

        resultados: list[bool] = []

        texto_progresso.print_barra_de_progresso(0, len(palavras))
        for indice in range(0, len(palavras)):
            resultado = Pesquisador.pesquisar(palavras[indice])
            resultados.append(resultado)
            texto_progresso.print_barra_de_progresso(indice + 1, len(palavras))
        print("\n")

        # Informando dos resultados

        for indice in range(0, len(palavras)):
            resultado = resultados[indice]
            palavra = palavras[indice]

            if resultado:
                print(f"\"{palavra}\" consta no vocabulário da ABL;")
            else:
                print(f"\"{palavra}\" não consta no vocabulário da ABL;")

    def sair(self):
        texto_carregamento = texto_progresso.TextoCarregamento()

        texto_carregamento.comecar("Fechando o pesquisador")
        Pesquisador.sair()
        texto_carregamento.terminar()
        self.terminal_laco = False

    def teste(self):
        if not self.pesquisador_iniciado:
            print("O Pesquisador deve ser iniciado. Para iniciá-lo, digitar \"iniciar\".")
            return

        palavras: list[str] = ["salada", "anticonstitucional", "constitucional", "anticonstitucional", "antigo",
                               "artigo", "queij", "queijo", "batata", "queijo", "queij", "batata", "órfão", "órfã",
                               "àquilo", "atômico", "salds", "atómico", "salsa", "salça", "salsa", "salça"]
        resultados: list[bool] = []
        resultados_esperados: list[bool] = [True, True, True, True, True, True, False, True, True, True, False, True,
                                            True, True, True, True, False, False, True, False, True, False]

        erro: bool = False
        inicio_tempo: float = time.time_ns()

        texto_progresso.print_barra_de_progresso(0, len(palavras))
        for indice in range(0, len(palavras)):
            resultado: bool = Pesquisador.pesquisar(palavras[indice])
            resultados.append(resultado)

            if resultado != resultados_esperados[indice]:
                erro = True
                print(f"ERRO: \"{palavras[indice]}\" retornou '{resultados}'.\nO Pesquisador pode não funcionar "
                      f"corretamente.")

            texto_progresso.print_barra_de_progresso(indice + 1, len(palavras))
        print("\n")

        tempo_teste = time.time_ns() - inicio_tempo

        tempo_s = tempo_teste / 1_000_000_000
        tempo_medio = len(palavras) / tempo_s

        if erro:
            print(f"Teste completo e mal-sucedido. Em {tempo_s}s. Média de palavras por segundo: {tempo_medio}s.")

        if not erro:
            print(f"Teste completo e bem-sucedido. Em {tempo_s}s. Média de palavras por segundo: {tempo_medio}s.")

    @staticmethod
    def limpar_terminal():
        comando_limpar = "cls" if os.name == "nt" else "clear"
        os.system(comando_limpar)


terminal = PesquisadorTerminal()
terminal.comecar_terminal()
