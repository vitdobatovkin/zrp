from AdsPower import AdsProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from loguru import logger

def press_btn(driver):
    try:
        # Найдите кнопку
        element = driver.find_element(By.XPATH, '//*[@id="message-accessories-1275113837108138057"]/div/div/div/button')
        # Создайте объект ActionChains
        actions = ActionChains(driver)
        
        # Наведите курсор на элемент и выполните клик
        actions.move_to_element(element).click().perform()

        logger.info("Button pressed")
    except Exception as e:
        logger.error(f"Error while pressing button: {e}")

def main():
    # Чтение профилей из файла
    try:
        with open('profiles.txt', 'r') as file:
            profiles = file.read().splitlines()
    except FileNotFoundError:
        logger.error("File 'profiles.txt' not found")
        return
    except Exception as e:
        logger.error(f"Error reading profiles file: {e}")
        return

    for profile_name in profiles:
        # Создаём экземпляр AdsProfile
        profile = AdsProfile(profile_name)
        profile.start()

        try:
            time.sleep(random.uniform(2, 3))
            for handle in profile.driver.window_handles:
                profile.driver.switch_to.window(handle)
                if 'company_id' in profile.driver.current_url:
                    break
            
            # Переходим на нужную страницу
            profile.driver.get('https://discord.com/channels/1220035427952627863/1275113835753373840')
            time.sleep(random.uniform(10, 15))  # Ждём, пока страница загрузится

            # Выполняем действие
            press_btn(profile.driver)
        
        finally:
            logger.info("Закрываю вкладку")
            time.sleep(random.uniform(3, 5))
            profile.driver.close()

            logger.info("Закрываю профиль")
            time.sleep(random.uniform(3, 5))
            profile.stop()

            # Задержка между профилями
            logger.info("Waiting before processing the next profile...")
            time.sleep(random.uniform(3, 5))  # Задержка в секундах

if __name__ == "__main__":
    main()
