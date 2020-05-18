from .browser import Browser
from .pages import ItemListPage


def before_all(context):
    context.browser = Browser()
    context.item_list_page = ItemListPage()


def after_all(context):
    context.browser.close()
