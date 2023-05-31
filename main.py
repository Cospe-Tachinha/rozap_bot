#Imports
import webbrowser
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

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

nome_chat = input("Insira o nome do chat: ")
response = input("Insira a message a ser enviada: ")
command = "/test"

#Open the chat
chat = browser.find_element(By.XPATH, f"//span[@title='{nome_chat}']")
chat.click()
sleep(2)

#Receive and send messages
while True:
    messages = browser.find_elements(By.CSS_SELECTOR, ".selectable-text")

    for i in range(len(messages)):
        messages = browser.find_elements(By.CSS_SELECTOR, ".selectable-text")
        message = messages[i]
        received_message = message.text.lower()
        print("message recebida:", received_message)

        if received_message == command:
            for letter in response:
                field = browser.find_element(By.CSS_SELECTOR, 'div[title="Mensagem"]')
                field.send_keys(letter)
            field.send_keys(Keys.ENTER)
    sleep(2)
