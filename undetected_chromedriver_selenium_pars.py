import undetected_chromedriver
import time
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
import random



try:
    driver = undetected_chromedriver.Chrome()
    driver.get("https://chat.openai.com/auth/login")
    time.sleep(random.uniform(1, 3))
    login_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button']")
    login_button.click()
    time.sleep(random.uniform(10, 20))
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()









# import time
# import undetected_chromedriver
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import random
# from selenium.webdriver.common.action_chains import ActionChains


# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Chrome(
#     #executable_path = "https://chat.openai.com/auth/login",
#     options = options
# )


# # JavaScript обрабатывается автоматически в Selenium. Пример использования cookies
# cookies = driver.get_cookies()
# print(cookies) # Вывести cookies

# # options.add_argument("--headless") # Активация headless режима

# # element = driver.find_element_by_id('__next')
# # actions = ActionChains(driver)
# # actions.move_to_element(element).perform() # Перемещение курсора к элементу


# try:

#     #time.sleep(random.uniform(1, 3)) # Пауза от 1 до 3 секунд https://chat.openai.com/auth/login


#     driver.get("https://auth0.openai.com/u/login/identifier?state=hKFo2SAtbkRvNGlHX000YjhKZkVjRU5Zb2l1ODM4YzRncVMzb6Fur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGZZc1dqX09LRW5kLUxaanpFc0loZDJxcUo0RUVNcjRMo2NpZNkgVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEc")
#     # Найдите кнопку по атрибуту data-testid и выполните на ней клик
#     #login_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button']")
#     # Пример задержки между действиями
#     time.sleep(random.uniform(1, 3))
#     #login_button.click()

#     time.sleep(random.uniform(10, 15)) 

# except Exception as ex:
#     print(ex)
# finally:
#     driver.close()
#     driver.quit()