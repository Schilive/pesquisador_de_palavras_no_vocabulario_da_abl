from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec


def iniciar():
    """Abre o novegador com as necessárias configurações e acessa à página da ABL quista"""

    global browser

    options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")  # Torna o navegador invisível
    chrome_driver = "D:/programatio/PycharmProjects/pesquisador_de_palavras_no_vocabulario_da_abl" \
                    "/chromedriver_win32/chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
    browser.get("http://www.academia.org.br/print/nossa-lingua/busca-no-vocabulario")


def pesquisar(plvr: str, maxtempo: int = 5) -> bool:
    """
    É checado se a palavra contida em 'X' consta no vocabulário da ABL

    PARÂMETROS:
        plvr        - Requerida : palavra para ser pesquisada (str)
        maxtempo    - Opcional  : tempo para o pesquisador perceber que a variável não consta (int)
    """

    # digita e espera até a palavra "alhures" ser encontrada

    # Procura input para escrever-lhe a variável 'x'
    findinput = browser.find_element_by_tag_name("input")  # Procura o INPUT
    findinput.clear()  # Apaga todos os textos contidos em INPUT
    findinput.send_keys("alhures")  # Escreve "alhures"

    # Procura botão para apertá-lo
    findbtn = browser.find_element_by_css_selector("button.btn.btn-primary")  # Procura o botão
    findbtn.click()  # Clica-lhe

    # Espera até "alhures" ser encontrado
    WebDriverWait(browser, 50).until(ec.presence_of_element_located((By.XPATH, "//strong[contains(.,'alhures')]")))

    # Digita e procura à palavra contida na varável 'x'

    # Escreve a variável 'x' e clica no botão "pesquisar"
    findinput.clear()
    findinput.send_keys(plvr)

    findbtn.click()

    # Procura a palavra contida em 'x'
    try:
        WebDriverWait(browser, maxtempo).until(ec.presence_of_element_located((By.XPATH, f"//strong[contains(.,'{plvr}')]")))
    except TimeoutException:
        return False
    return True


def sair():
    """O Pesquisador é fechado"""

    browser.quit()
