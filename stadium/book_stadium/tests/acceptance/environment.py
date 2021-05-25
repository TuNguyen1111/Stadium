from behave import fixture, use_fixture
from selenium import webdriver

from django.conf import settings


@fixture
def selenium_browser_chrome(context):
    context.url = 'http://127.0.0.1:8000'
    context.browser = webdriver.Chrome(settings.SELENIUM_CHROME_DRIVER_PATH)
    context.browser.maximize_window()
    context.browser.implicitly_wait(4)
    yield context.browser
    context.browser.quit()


def before_all(context):
    use_fixture(selenium_browser_chrome, context)
