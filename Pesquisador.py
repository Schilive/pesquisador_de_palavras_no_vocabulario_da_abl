from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement


class PesquisadorPalavraABL:
    """Pesquisa no vocabulário da ABL (https://www.academia.org.br/print/nossa-lingua/busca-no-vocabulario) se
    uma palavra consta nele."""

    def __init__(self):
        self.seguranca: list[int] = [True, True, True]  # 0: iniciar() apenas 1 vez.
        # 1: pesquisar() apenas se iniciar() tiver sido acionado.
        # 2:  mínimo valor de 'max_tempo' = 3

        self.iniciado: bool = False

        self.browser: webdriver.Chrome | None = None

    def iniciar(self):
        """Abre o navegador com as necessárias configurações e acessa à página do vocabulário ABL. A página usada é de
        impressão, pois, ela contém menos itens desnecessários."""

        # Sistema de segurança para iniciar() ser ativado apenas 1 vez
        if self.seguranca[0] and self.iniciado:
            raise Exception("'iniciar()' só pode ser ativado 1 vez. Protocolo de segurança nº 0")

        options: Options = Options()
        prefs: dict[str, int] = {"profile.managed_default_content_settings.images": 2}  # Não carrega imagens
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})  # Não guarda cookies
        options.add_argument("--headless")  # Torna o navegador invisível

        try:
            self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                            chrome_options=options)
            self.iniciado = True
        except selenium.common.exceptions.WebDriverException:
            mensagem_erro = "O pesquisador não pôde ser iniciado, pois, o ChromeDriver não foi encontrado."
            raise selenium.common.exceptions.WebDriverException(mensagem_erro)

        self.browser.get("https://www.academia.org.br/print/nossa-lingua/busca-no-vocabulario")

    def pesquisar_caixa(self, palavra: str):
        """Digita 'palavra' na caixa de pesquisa e pressiona o botão para pesquisar."""

        # Procura o "INPUT", que é a caixa de pesquisa, para escrever nela 'palavra'
        caixa_de_pesquisa: WebElement = self.browser.find_element(By.TAG_NAME, "input")
        caixa_de_pesquisa.clear()
        caixa_de_pesquisa.send_keys(palavra)

        # Procura botão para apertá-lo
        botao_pesquisar: WebElement = self.browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        botao_pesquisar.click()

    def pesquisar(self, palavra: str, max_tempo: int = 5) -> bool:
        """
        Checa se a palavra contida em 'palavra' consta no vocabulário da ABL

        PARÂMETROS:
            palavra    (str)   - Requerida : palavra para ser pesquisada
            max_tempo  (int)   - Opcional  : tempo máximo para o pesquisador perceber que a variável não consta
        """

        palavra_certa: str = "constituinte"

        if palavra == palavra_certa:
            return True

        # Sistemas de segurança
        if self.seguranca[1] and self.iniciado:
            pass
        else:
            raise Exception("'pesquisar()' só funciona se o programar estiver ativado. Para ativar 'iniciar()'. "
                            "Protocolo de segurança nº 1")

        if self.seguranca[2] and max_tempo < 3:
            raise Exception("O valor da variável 'max_tempo' tem de ser no mínimo de 3 e da variável. Protocolo de "
                            "segurança nº 2.")

        # Assegura que a página carregou

        self.pesquisar_caixa(palavra_certa)
        WebDriverWait(self.browser, max_tempo).until(ec.presence_of_element_located((
            By.XPATH, f"//span[.='{palavra_certa}']")))

        self.pesquisar_caixa(palavra)
        WebDriverWait(self.browser, max_tempo).until_not(ec.presence_of_element_located((
            By.XPATH, f"//span[.='{palavra_certa}']")))

        # A procura

        if self.browser.find_elements(By.XPATH, f"//span[.='{palavra}']"):
            return True
        elif self.browser.find_elements(By.XPATH, f"//span[contains(.,'{palavra} (')]"):  # Com ortoépia, como "oi (ô)"
            return True
        else:
            return False

    def sair(self):
        """Fecha o pesquisador."""

        if self.iniciado:
            self.browser.quit()
