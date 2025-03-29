from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
import random
import os

load_dotenv()


def init_browser():
    """Инициализация браузера с улучшенной маскировкой"""

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return browser


def login(browser):
    """Функция входа в аккаунт с человекообразным поведением"""
    try:
        print("Начинаю вход в аккаунт...")

        browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(random.uniform(3, 5))

        # Ждем и заполняем поля
        username_field = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.NAME, 'username')))

        password_field = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.NAME, 'password')))

        # Очищаем поля перед вводом
        username_field.clear()
        password_field.clear()

        # Вводим данные с паузами
        username = os.getenv('INSTAGRAM_USERNAME')
        for char in username:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        time.sleep(random.uniform(1, 2))

        password = os.getenv('INSTAGRAM_PASSWORD')
        for char in password:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))

        # Ждем активации кнопки (пока она не станет кликабельной)
        login_button = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"][not(@disabled)]')))

        # Кликаем с человеческой задержкой
        time.sleep(random.uniform(0.5, 1.5))
        login_button.click()

        # Проверяем успешный вход
        WebDriverWait(browser, 15).until(
            lambda d: "accounts/login" not in d.current_url)

        print("Вход выполнен успешно")
        return True

    except Exception as e:
        print(f"Ошибка входа: {str(e)}")
        browser.save_screenshot("login_error.png")
        print("Скриншот сохранен: login_error.png")
        return False


if __name__ == "__main__":
    browser = init_browser()
    if login(browser):
        print("Успешный вход! Браузер останется открытым.")
        while True:  # Бесконечный цикл - браузер не закроется
            time.sleep(10)
