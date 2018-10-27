from selenium import webdriver


class Browser(object):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    def close(context):
        context.driver.close()
