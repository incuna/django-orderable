from selenium import webdriver


chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1024x768")


class Browser(object):
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(5)

    def close(context):
        context.driver.close()
