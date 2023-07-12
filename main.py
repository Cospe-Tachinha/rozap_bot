import requests
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

def configure_browser():
    profile_path = r'C:\Users\vitin\AppData\Roaming\Mozilla\Firefox\Profiles\mhhsjylt.default-release'
    options = FirefoxOptions()
    options.add_argument("--lang=pt")
    options.profile = profile_path

    service = Service(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=service, options=options)
    browser.get('https://web.whatsapp.com/')
    browser.set_window_size(1000, 700)

    return browser

def open_gpt(browser):
    browser.execute_script("window.open()")
    browser.switch_to.window(browser.window_handles[1])
    browser.get("https://chat.openai.com/?model=text-davinci-002-render-sha")
    browser.switch_to.window(browser.window_handles[0])

def open_chat(browser):
    name_chat = input("Insira o nome do chat: ")

    chat = browser.find_element(By.XPATH, f"//span[@title='{name_chat}']")
    chat.click()
    sleep(2)

    initial_message = 'Opaa! Eu sou o RoZAP\nEnvie */help* para ver os comandos'
    send_message(browser, initial_message)

def send_message(browser, message):
    text_box = browser.find_element(By.CSS_SELECTOR, 'div[title="Mensagem"]')
    for letter in message:
        text_box.send_keys(letter)
    text_box.send_keys(Keys.ENTER)

def get_phrase(author):
    page = requests.get(f'https://www.pensador.com/autor/{author}')
    soup = BeautifulSoup(page.text, 'html.parser')

    phrases = soup.find_all('p', class_='frase')
    nmr = randint(0, len(phrases))
    phrase = phrases[nmr].get_text()

    author_name = soup.find('span', class_='author-name').get_text()

    return phrase, author_name

def process_messages(browser):
    while True:
        messages = browser.find_elements(By.CSS_SELECTOR, ".message-in, .message-out")
        last_message = None

        for message in reversed(messages):
            if message.get_attribute("class").startswith("message-in"):
                WebDriverWait(browser, 10).until(EC.visibility_of(message))
                try:
                    last_message = message.find_element(By.CSS_SELECTOR, ".selectable-text")
                    break
                except NoSuchElementException:
                    continue
            elif message.get_attribute("class").startswith("message-out"):
                WebDriverWait(browser, 10).until(EC.visibility_of(message))
                try:
                    last_message = message.find_element(By.CSS_SELECTOR, ".selectable-text")
                    break
                except NoSuchElementException:
                    continue

        last_message_text = last_message.text if last_message else ""
        if last_message_text:
            print("Última mensagem enviada:", last_message_text)

        text = last_message_text.split(" ")

        if text[0] == '/help':
            help_message = '*Comandos:*\n\n*/phrase autor* - Envia uma frase aleatória do autor desejado'
            send_message(browser, help_message)

        if text[0] == '/phrase':
            try:
                if len(text) < 3:
                    author = text[1]
                else:
                    text.pop(0)
                    author = '_'.join(text)

                author = unidecode(author.lower())
                phrase, author_name = get_phrase(author)
                print("Frase:", phrase)

                if len(phrase) < 350:
                    send_message(browser, f'*{author_name}:*\n\n{phrase}')
                else:
                    error_message = '*Ops!* Acho que a frase é muito grande. Tente novamente, por favor.'
                    send_message(browser, error_message)
                    continue
            except IndexError:
                error_message = 'Foi mal ;-; Não consegui encontrar esse autor. Tente com um diferente, por favor.'
                send_message(browser, error_message)
                continue
        sleep(2)

def main():
    browser = configure_browser()
    input("Faça a autenticação no WhatsApp Web e pressione Enter para continuar...")
    sleep(1)
    #open_gpt(browser)
    open_chat(browser)
    process_messages(browser)

if __name__ == '__main__':
    main()