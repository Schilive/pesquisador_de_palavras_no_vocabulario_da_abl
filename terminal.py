import Pesquisador
import time
from selenium.common.exceptions import WebDriverException
import texto_progresso
import os

"""
Comandos do Terminal:

iniciar | Inicia o 'Pesquisador';
pesquisar OU p <palavra> | Pesquisa a <palavra> para dizer se conta ou não no vocabulário da ABL;
pesquisa-multipla OU pm <palavra1>, <palavra2> | Pesquisa 1 ou mais palavras;
erro OU erro | Mostra a última mensagem de erro levantada, se houver;
cls OU clear OU limpar | Limpa a tela
sair | Fecha o 'Pesquisador' e o Terminal;
teste | Testa o Pesquisador;
/? OU ? OU -? OU ajuda OU help | Abrem a ajuda do Terminal.

Exemplos:
    p queijo
    iniciar && pm queijo, açafrão
    p santo & p mario
"""


class PesquisadorTerminal:
    def __init__(self):
        self.terminal_laco = False
        self.pesquisador_iniciado = False

        self.pesquisador: Pesquisador.PesquisadorPalavraABL | None = Pesquisador.PesquisadorPalavraABL()
        self.max_tempo: int = 10

        self.msg_erro = "Um erro foi levantado (Use o comando \"erro\" para ver a mensagem)."
        self.ultima_excecao: Exception | None = None

    # Funções internas

    def comecar_terminal(self):
        self.terminal_laco = True

        while self.terminal_laco:
            entrada: str = input(">: ")  # Para o usuário digitar um comando

            self.interpretar_entrada(entrada)

    def interpretar_entrada(self, entrada: str):
        def contem_ampersand_unica(texto: str) -> bool:
            """Retorna se o texto contém ampersand única sem ser dupla; por exemplo, "e & e" retorna verdadeiro, mas
            "e && e" retorna falso."""

            if len(entrada) == 0:
                return False
            elif len(entrada) == 1:
                if texto[0] == "&":
                    return True
                return False
            elif len(entrada) == 2:
                if texto.count("&") == 1:
                    return True
                return False

            ultimo_char = texto[0]
            penultimo_char = texto[1]
            for char in texto[2:]:
                if char != "&" and ultimo_char == "&" and penultimo_char != "&":
                    return True

                penultimo_char = ultimo_char
                ultimo_char = char

            return False

        def separar_ampersand_unica(texto) -> list[str]:
            """Separa textos com ampersand sem confusão com ampersand duplo; por exemplo,
            "eu & sei && ele sabe" -> ["eu ", " sei && ele sabe"]. """

            if len(texto) < 1:
                return []
            elif len(texto) == 2:
                if texto.count("&") == 1:
                    if texto[0] == "&":
                        return [texto[1]]
                    return [texto[0]]
                return []

            resultado: list[str] = []

            primeiro_char: int = 0
            ultimo_char = texto[0]
            penultimo_char = texto[1]
            for index in range(0, len(entrada)):
                if entrada[index] != "&" and ultimo_char == "&" and penultimo_char != "&":
                    resultado.append(entrada[primeiro_char: index - 2])
                    primeiro_char = index

                penultimo_char = ultimo_char
                ultimo_char = entrada[index]

            resultado.append(entrada[primeiro_char:len(entrada)])

            return resultado

        if "&&&" in entrada:
            print("O trio de ampersands \"&&&\" não é permitido.")
            return
        elif contem_ampersand_unica(entrada):
            print("a")
            comandos_continuos: list[str] = separar_ampersand_unica(entrada)
            for comando in comandos_continuos:
                self.interpretar_entrada(comando)

            return
        elif "&&" in entrada:
            comandos_certos: list[str] = entrada.split("&&")

            cache_erro: Exception = self.ultima_excecao
            self.ultima_excecao = None

            for comando in comandos_certos:
                self.executar_comando(comando)

                if self.ultima_excecao is not None:
                    return

            self.ultima_excecao = cache_erro

            return

        self.executar_comando(entrada)

    def executar_comando(self, comando_str: str):
        if len(comando_str.split()) == 0:
            print("Comando não identificado. Para ver os comandos disponíveis, digitar \"ajuda\".")
            return

        comando_str = comando_str.strip()
        comando = comando_str.split()[0]
        argumentos = "".join(comando_str.split()[1:])

        if comando == "iniciar":
            self.iniciar_pesquisador()
        elif comando in {"pesquisar", "p"}:
            self.pesquisar(argumentos)
        elif comando in {"pesquisa-multipla", "pm"}:
            self.pesquisar_multipla(argumentos)
        elif comando == "teste":
            self.teste()
        elif comando in {"erro", "error"}:
            self.mostrar_msg_erro()
        elif comando in {"clear", "cls", "limpar"}:
            self.limpar_terminal()
        elif comando == "sair":
            self.sair()
        elif comando in {"/?", "-?", "ajuda", "help"}:
            print("""Comandos do Terminal:
            iniciar | Inicia o 'Pesquisador';
            pesquisar OU p <palavra> | Pesquisa a <palavra> para dizer se conta ou não no vocabulário da ABL;
            pesquisa-multipla OU pm <palavra1>, <palavra2> | Pesquisa 1 ou mais palavras;
            erro OU erro | Mostra a última mensagem de erro levantada, se houver;
            cls OU clear OU limpar | Limpa a tela
            sair | Fecha o 'Pesquisador' e o Terminal;
            teste | Testa o Pesquisador;
            /? OU ? OU -? OU ajuda OU help | Abrem a ajuda do Terminal.
            
            Exemplos:
                p queijo
                iniciar && pm queijo, açafrão
                p santo & p mario""")
        else:
            print("Comando não identificado. Para ver os comandos disponíveis, digitar \"ajuda\"")

    # Funções para o pesquisador, com o terminal

    def iniciar_pesquisador(self):
        """Iniciar o pesquisador."""

        if self.pesquisador_iniciado:
            print("O Pesquisador já está iniciado.")
            return

        texto_carregamento = texto_progresso.TextoCarregamento()
        texto_carregamento.comecar("Iniciando pesquisador")

        try:
            self.pesquisador.iniciar()
            self.pesquisador_iniciado = True

            texto_carregamento.terminar()
        except WebDriverException as e:
            texto_carregamento.terminar()

            self.ultima_excecao = e
            print()
            print(self.msg_erro)

            print("O pesquisador não pôde ser iniciado. O chrome driver não pôde ser encontrado.")
        except Exception as e:
            texto_carregamento.terminar()

            self.ultima_excecao = e
            print()
            print(self.msg_erro)

            print("O pesquisador não pôde ser iniciado.")

    def pesquisar(self, palavra: str):
        if not self.pesquisador_iniciado:
            print("O Pesquisador deve ser iniciado. Para iniciá-lo, digitar \"iniciar\".")
            return
        elif len(palavra.split()) == 0:
            print("O comando \"pesquisar <palavra>\" precisa de uma palavra.")
            return

        try:
            resultado = self.pesquisador.pesquisar(palavra, max_tempo=self.max_tempo)
        except Exception as e:
            self.ultima_excecao = e

            print()
            print(self.msg_erro)
            return

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
            try:
                resultado = self.pesquisador.pesquisar(palavras[indice])
                resultados.append(resultado)
                texto_progresso.print_barra_de_progresso(indice + 1, len(palavras))
            except Exception as e:
                self.ultima_excecao = e
                print()
                print(self.msg_erro)
                return

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
        self.pesquisador.sair()
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
            try:
                resultado: bool = self.pesquisador.pesquisar(palavras[indice])
                resultados.append(resultado)
            except Exception as e:
                self.ultima_excecao = e
                erro = True

                print()
                print(self.msg_erro)
                break

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

    # Funções para o terminal

    @staticmethod
    def limpar_terminal():
        comando_limpar = "cls" if os.name == "nt" else "clear"
        os.system(comando_limpar)

    def mostrar_msg_erro(self):
        if self.ultima_excecao is None:
            print("Nenhum erro foi levantado nesta sessão.")
            return

        print()
        print(str(self.ultima_excecao))
        print()


terminal = PesquisadorTerminal()
terminal.comecar_terminal()
