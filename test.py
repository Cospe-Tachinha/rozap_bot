#Imports
import webbrowser
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#Configuring Firefox browser options
driver = Service(GeckoDriverManager().install())
options = webdriver.FirefoxOptions()
options.add_argument("--lang=pt")

#Launch Firefox with the browser profile
myprofile = webdriver.FirefoxProfile(r'C:\Users\vitin\AppData\Roaming\Mozilla\Firefox\Profiles\mhhsjylt.default-release')
browser = webdriver.Firefox(firefox_profile=myprofile, service=driver, options=options)
browser.get('https://web.whatsapp.com/')
browser.set_window_size(1000, 700)

#Authentication
input("Faça a autenticação no WhatsApp Web e pressione Enter para continuar...")
sleep(1)

name_chat = 'Cospe Tachinha'

#Open the chat
chat = browser.find_element(By.XPATH, f"//span[@title='{name_chat}']")
chat.click()
sleep(2)

#Receive and send messages
while True:
    mensagens = browser.find_elements(By.CSS_SELECTOR, ".message-in, .message-out")

    ultima_mensagem = None
    for mensagem in reversed(mensagens):
        if mensagem.get_attribute("class").startswith("message-out"):
            WebDriverWait(browser, 10).until(EC.visibility_of(mensagem))
            try:
                ultima_mensagem = mensagem.find_element(By.CSS_SELECTOR, ".selectable-text")
                break
            except NoSuchElementException:
                continue

    texto_ultima_mensagem = ultima_mensagem.text if ultima_mensagem else ""
    if texto_ultima_mensagem:
        print("Última mensagem enviada:", texto_ultima_mensagem)

    sleep(2)