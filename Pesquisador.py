from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def iniciar():
    """Esta função abre o novegador com as necessárias configurações, acessa à página da ABL quista"""

    global browser

    options = Options()
    options.add_argument("--headless")  # Torna o navegador invisível
    chrome_driver = "chromedriver_win32/chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
    browser.implicitly_wait(10)
    browser.get("http://www.academia.org.br/print/nossa-lingua/busca-no-vocabulario")


def pesquisar(x: str) -> bool:
    """É checado se a palavra contida em 'X' consta no vocabulário da ABL"""

    # Procurar input para nele escrever a variável 'x'
    findinput = browser.find_element_by_tag_name("input")  # Procura o input
    findinput.send_keys(Keys.CONTROL, "a", Keys.DELETE)  # Deletar o texto escrito no input.
    findinput.send_keys(x)  # Escreve a variável 'x'

    # Procurar botão para apertá-lo
    findbtn = browser.find_element_by_css_selector("button.btn.btn-primary")  # Procura o botão
    findbtn.click()  # Clica-lhe

    # Procura todas as respostas dadas pelo site
    browser.implicitly_wait(10)
    for c in range(0, 5):
        try:
            findpalavra = browser.find_elements_by_class_name("item-palavra")
        except NoSuchElementException:
            return False
        except StaleElementReferenceException:
            print("BATATUS")
            return False

        # Checa se uma das respostas é igual à variável 'x' e resolve o erro de "StaleElementReferenceException"
        try:
            for d in range(0, len(findpalavra)):
                if findpalavra[c].text == x:
                    return True
                elif c == len(findpalavra) - 1:
                    return False
        except StaleElementReferenceException:
            continue


def sair():
    """O navegador e o programa são fechados"""

    browser.quit()
