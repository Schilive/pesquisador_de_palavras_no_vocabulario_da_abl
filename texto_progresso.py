""" Oferece funções e classes para expressar por texto (print()) um carregamento """

import time
import threading


def print_barra_de_progresso(interacao, total):
    """Imprime uma barra de progresso com (interacao / total)% feito. A cada chamada desta função, a barra de
    progresso é reposta."""

    porcento: float = 100 * (interacao / float(total))
    porcento_msg: str = "{0:.2f}".format(porcento)

    comprimento_barra = 50
    comprimento_cheio: int = comprimento_barra * interacao // total  # a // b = floor(a / b)
    comprimento_cheio: int = max(min(comprimento_cheio, comprimento_barra), 0)

    barra: str = '█' * comprimento_cheio + '-' * (comprimento_barra - comprimento_cheio)
    print(f'\rProgresso: |{barra}| {porcento_msg}% Completo', end="")


class TextoCarregamento:
    """Imprime um texto de carregamento animado paralelamente, permitindo que outras coisas sejam executadas."""

    def __init__(self):
        self.carregando: threading.Lock = threading.Lock()

    def animacao_loop(self, mensagem: str):
        """O loop da animação do texto de carregamento."""

        quantos_pontos: int = 0

        while self.carregando.locked():
            print(f"\r{mensagem} " + "." * quantos_pontos, end="")

            if quantos_pontos == 3:
                quantos_pontos = 0
            elif quantos_pontos < 3:
                quantos_pontos += 1

            time.sleep(0.5)

    def comecar(self, mensagem: str = "Carregando"):
        """Começa o texto de carregamento, e sua animação. A animação é do seguinte formato:
        "{mensagem}"
        "{mensagem} ."
        "{mensagem} .."
        "{mensagem} ..."
        "{mensagem}"
        etc.
        """

        self.carregando.acquire()
        carregamento_thread = threading.Thread(target=self.animacao_loop, args=(mensagem,), daemon=True)
        carregamento_thread.start()

    def terminar(self):
        """Termina a animação do texto de carregamento, e pula uma linha."""

        self.carregando.release()
        print()
