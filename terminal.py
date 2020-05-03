import Pesquisador

"""
Comandos do Terminal:

iniciar (referente ao arquivo "Pesquisador.py");
pesquisar <palavra> (referente ao arquivo "Pesquisador.py"), podendo <palavra> conter espaços;
sair (referente ao arquivo "Pesquisador.py");
/? OU ? OU -? invocam o comando de ajuda.

"""

iniciado: bool = False  # Se o Pesquisador está iniciado

while True:
    cmd: str = input(">: ")  # Para o usuário digitar um comando

    # Comandos
    if cmd == "iniciar":
        if not iniciado:
            Pesquisador.iniciar()
            iniciado = True
        else:
            print("O Pesquisador já está iniciado.")
    elif cmd.split()[0] == "pesquisar":
        if iniciado and len(cmd.split()) > 1:
            palavra: str = ""  # Variável da palavra a ser pesquisada

            for c in range(1, len(cmd.split())):
                palavra = palavra + (cmd.split())[c]

            resultado = Pesquisador.pesquisar(palavra)

            if resultado:
                print(f"\"{palavra}\" consta no vocabulário da ABL.")
            else:
                print(f"\"{palavra}\" não consta no vocabulário da ABL.")

        elif not iniciado:
            print("O Pesquisador precisa ser iniciado. Para iniciá-lo, digite \"iniciar\".")
        else:
            print("O comando \"pesquisar <palavra>\" precisa de pelo menos uma palavra.")
    elif cmd == "sair":
        Pesquisador.sair()
        break
    elif cmd == "/?" or cmd == "/?" or cmd == "-?":
        print("""Comandos do Terminal:
        iniciar | Inicia o 'Pesquisador';
        pesquisar <palavra> | Pesquisa a <palavra> para dizer se conta ou não no vocabulário da ABL;
        sair | Fecha o 'Pesquisador' e o Terminal;
        /? OU ? OU -? | Abrem a ajuda do Terminal.""")
