from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

seguranca: list = [True, True, True]  # 0: iniciar() apenas 1 vez. 1: pesquisar() apenas se iniciar() foi acionado.
# 2:  mínimo valor de 'max_tempo' = 3, mínimo, de 'max_tempo_ortoepia' = 1.
iniciado: bool = False


def iniciar():
    """Abre o navegador com as necessárias configurações e acessa à página da ABL quista"""

    global browser
    global iniciado

    # Sistema de segurança para iniciar() ser ativado apenas 1 vez
    if seguranca[0] and iniciado:
        raise Exception("'iniciar()' só pode ser ativado 1 vez. Protocolo de segurança nº 0")

    options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}  # Não carrega imagens
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})  # Não guarda cookies
    options.add_argument("--headless")  # Torna o navegador invisível


    try:
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=options)
    except selenium.common.exceptions.WebDriverException:
        raise selenium.common.exceptions.WebDriverException("O pesquisador não pôde ser iniciad, pois, o chrome "
                                                            "driver não foi encontrado encontrado.")

    iniciado = True

    browser.get("https://www.academia.org.br/print/nossa-lingua/busca-no-vocabulario")


def pesquisar_caixa(palavra: str):
    """Digita 'palavra' na caixa de pesquisa e pressiona o botão para pesquisar"""

    # Procura INPUTo, a caixa de pesquisa, para escrever-lhe a variável 'palavra'
    findinput = browser.find_element(By.TAG_NAME, "input")  # Procura o INPUT
    findinput.clear()  # Apaga todos os textos contidos em INPUT
    findinput.send_keys(palavra)  # Escreve a palavra contida em 'palavra'

    # Procura botão para apertá-lo
    findbtn = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")  # Procura o botão
    findbtn.click()  # Clica-lhe


def pesquisar(palavra: str, max_tempo: int = 5) -> bool:
    """
    É checado se a palavra contida em 'palavra' consta no vocabulário da ABL

    PARÂMETROS:
        palavra             - Requerida : palavra para ser pesquisada (str)
        max_tempo           - Opcional  : tempo para o pesquisador perceber que a variável não consta (int)
    """

    if palavra == "constituinte":
        return True

    global iniciado

    # Sistemas de segurança
    if seguranca[1] and iniciado:
        pass
    else:
        raise Exception("'pesquisar()' só funciona se o programar estiver ativado. Para ativar 'iniciar()'. Protocolo "
                        "de segurança nº 1")

    if seguranca[2] and max_tempo < 3:
        raise Exception("O valor da variável 'max_tempo' tem de ser no mínimo de 3 e da variável 'max_tempo_ortoepia',1"
                        ". Protocolo de segurança nº 2")

    # Procura a palavra contida em 'palavra' e retorna a resposta
    class ElementoNaoLocalizado(object):

        """Um expectativa para checar o elemento não está presente"""
        """An expectation for checking that an element has a particular css class.

          locator - usado para encontrar o elemento
          retorna o WebElement quando não estiver presente
          """

        def __init__(self, locator):
            self.locator = locator

        def __call__(self, driver):
            elemento = driver.find_elements(By.XPATH, self.locator)

            if not elemento:
                return True
            else:
                return False

    # Assegura que a página carregou

    pesquisar_caixa("constituinte")
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, f"//span[.='constituinte']")))
    pesquisar_caixa(palavra)
    WebDriverWait(browser, 10).until(ElementoNaoLocalizado(f"//span[.='constituinte']"))

    # A procura

    if browser.find_elements(By.XPATH, f"//span[.='{palavra}']"):
        return True
    elif browser.find_elements(By.XPATH, f"//span[contains(.,'{palavra} (')]"):  # Com ortoépia, como "oi (ô)"
        return True
    else:
        return False


def sair():
    """O Pesquisador é fechado"""
    if iniciado:
        browser.quit()
