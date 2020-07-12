import Pesquisador
import time


def print_barra_de_progresso(iteration, total):
    """
    Call in a loop to create terminal progress bar

    PARÂMETROS:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
    """
    percent = ("{0:." + str(2) + "f}").format(100 * (iteration / float(total)))
    filledlength = int(50 * iteration // total)
    bar = '█' * filledlength + '-' * (50 - filledlength)
    print(f'\rProgresso: |{bar}| {percent}% Completo', end="")
    # Print New Line on Complete
    if iteration == total:
        print("\n")


"""
Comandos do Terminal:

iniciar (referente ao arquivo "Pesquisador.py");
pesquisar <palavra> (referente ao arquivo "Pesquisador.py"), podendo <palavra> conter espaços;
sair (referente ao arquivo "Pesquisador.py");
pesquisa múltipla | pesquisa mais duma palavra;
/? OU ? OU -? OU ajuda OU help | invocam o comando de ajuda.

"""


if __name__ == '__main__':
    iniciado: bool = False  # Se o Pesquisador está iniciado
    maxtempo: int = 5  # Tempo máximo para o pesquisador perceber que a palavra não consta

    while True:
        cmd: str = input(">: ")  # Para o usuário digitar um comando
        # Comandos
        if cmd.isspace() or cmd == "":
            print("Comando não identificado. Para ver os comandos disponíveis, digitar \"ajuda\".")
        elif cmd == "iniciar":
            if not iniciado:
                Pesquisador.iniciar()
                iniciado = True
            else:
                print("O Pesquisador já está iniciado.")
        elif cmd.split()[0] == "pesquisar" or cmd.split()[0] == "p":
            if iniciado and len(cmd.split()) > 1:
                palavra: str = ""  # Variável que contem a palavra a ser pesquisada

                for c in range(1, len(cmd.split())):  # Faz "p joão da cruz" e "p joão" em "joão da cruz" e "joão"
                    if c != 1:
                        palavra = palavra + " " + (cmd.split())[c]
                    else:
                        palavra = palavra + (cmd.split())[c]

                resultado = Pesquisador.pesquisar(palavra)

                if resultado:
                    print(f"\"{palavra}\" consta no vocabulário da ABL.")
                else:
                    print(f"\"{palavra}\" não consta no vocabulário da ABL.")

            elif not iniciado:
                print("O Pesquisador precisa ser iniciado. Para iniciá-lo, digitar \"iniciar\".")
            else:
                print("O comando \"pesquisar <palavra>\" precisa de uma palavra.")
        elif cmd.split()[0] == "pesquisa múltipla" or cmd.split()[0] == "pesquisa multipla" or cmd.split()[0] == "pm":
            if iniciado and len(cmd.split()) > 1:
                palavras: list = [""]

                e: int = 0
                for f in range(1, len(cmd.split())):
                    if cmd.split()[f][-1] == ",":
                        palavras[e] = palavras[e] + cmd.split()[f][:-1]
                        e = e + 1
                        palavras.append("")
                    else:
                        if f == len(cmd.split()) - 1:
                            palavras[e] = palavras[e] + cmd.split()[f]
                        else:
                            palavras[e] = palavras[e] + cmd.split()[f] + " "

                resultados: list = []

                print()
                for f in range(0, len(palavras)):
                    palavralocal = palavras[f]
                    resultados.append(Pesquisador.pesquisar(palavralocal))
                    print_barra_de_progresso(f + 1, len(palavras))

                for g in range(0, len(palavras)):  # dá "print" de "<palavra> <consta/não está contido> no vocabulário
                    # da ABL"
                    if g != len(palavras) - 1:  # não for o último
                        if resultados[g]:
                            print(f"\"{palavras[g]}\" consta no vocabulário da ABL;")
                        else:
                            print(f"\"{palavras[g]}\" não está contido no vocabulário da ABL;")
                    else:
                        if resultados[g]:
                            print(f"\"{palavras[g]}\" consta no vocabulário da ABL.\n")
                        else:
                            print(f"\"{palavras[g]}\" não está contido no vocabulário da ABL.\n")

            elif not iniciado:
                print("O Pesquisador precisa ser iniciado. Para iniciá-lo, digitar \"iniciar\".")
            else:
                print("O comando \"pm <palavra1>; <palavra2>\" precisa de pelo menos uma palavra.")
        elif cmd == "sair":
            Pesquisador.sair()
            break
        elif cmd == "/?" or cmd == "/?" or cmd == "-?" or cmd == "ajuda" or cmd == "help":
            print("""Comandos do Terminal:
            iniciar | Inicia o 'Pesquisador';
            pesquisar OU p <palavra> | Pesquisa a <palavra> para dizer se conta ou não no vocabulário da ABL;
            pesquisa múltipla OU pesquisa multipla OU pm <palavra1>, <palavra2> | Pesquisa 1 ou mais palavras;
            sair | Fecha o 'Pesquisador' e o Terminal;
            /? OU ? OU -? OU ajuda OU help | Abrem a ajuda do Terminal.""")
        else:
            print("Comando não identificado. Para ver os comandos disponíveis, digitar \"ajuda\"")
