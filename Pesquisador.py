from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec

seguranca: list = [True, True, True]  # 0: iniciar() apenas 1 vez. 1: pesquisar() apenas se iniciar() foi acionado.
# 2:  mínimo valor de 'max_tempo' = 3, mínimo, de 'max_tempo_ortoepia' = 1.
iniciado: bool = False


def iniciar():
    """Abre o navegador com as necessárias configurações e acessa à página da ABL quista"""

    global browser
    global iniciado

    # Sistema de segurança para iniciar() ser ativado apenas 1 vez
    if seguranca[0] and not iniciado:
        iniciado = True
        pass
    else:
        raise Exception("'iniciar()' só pode ser ativado 1 vez. Protocolo de segurança nº 0")

    options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}  # Não carrega imagens
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})  # Não guarda cookies
    options.add_argument("--headless")  # Torna o navegador invisível
    chrome_driver = "D:/programatio/PycharmProjects/pesquisador_de_palavras_no_vocabulario_da_abl" \
                    "/chromedriver_win32/chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
    browser.get("http://www.academia.org.br/print/nossa-lingua/busca-no-vocabulario")


def pesquisar(palavra: str, max_tempo: int = 5, max_tempo_ortoepia: int = 3, ortoepia: bool = True) -> bool:
    """
    É checado se a palavra contida em 'palavra' consta no vocabulário da ABL

    PARÂMETROS:
        palavra             - Requerida : palavra para ser pesquisada (str)
        max_tempo           - Opcional  : tempo para o pesquisador perceber que a variável não consta (int)
        max_tempo_ortoepia  - Opcional  : tempo para o pesquisador com ortoépia perceber que a variável não consta (int)
        ortoepia            - Opcional  : se procurar a palavra com ortoépia. "coroa (ô)" é diferente de "coroa"
    """

    global iniciado

    # Sistema de segurança para pesquisar() só ser iniciado quando 'iniciar()' tiver sido ativado
    if seguranca[1] and iniciado:
        pass
    else:
        raise Exception("'pesquisar()' só funciona se o programar estiver ativado. Para ativar 'iniciar()'. Protocolo "
                        "de segurança nº 1")

    if seguranca[2] and max_tempo < 3 and max_tempo_ortoepia < 1:
        raise Exception("O valor da variável 'max_tempo' tem de ser no mínimo de 3 e da variável 'max_tempo_ortoepia',1"
                        ". Protocolo de segurança nº 2")

    # Procura INPUT para escrever-lhe a variável 'palavra'
    findinput = browser.find_element_by_tag_name("input")  # Procura o INPUT
    findinput.clear()  # Apaga todos os textos contidos em INPUT
    findinput.send_keys(palavra)  # Escreve a palavra contida em 'palavra'

    # Procura botão para apertá-lo
    findbtn = browser.find_element_by_css_selector("button.btn.btn-primary")  # Procura o botão
    findbtn.click()  # Clica-lhe

    # Procura a palavra contida em 'palavra'
    try:
        WebDriverWait(browser, max_tempo).until(ec.presence_of_element_located((By.XPATH, f"//span[.='{palavra}']")))
    except TimeoutException:
        if ortoepia:
            try:
                WebDriverWait(browser, max_tempo_ortoepia).until(ec.presence_of_element_located((By.XPATH, f"//span[contains(.,'{palavra} (')]")))
            except TimeoutException:
                return False
        else:
            return False
    return True


def sair():
    """O Pesquisador é fechado"""
    browser.quit()
