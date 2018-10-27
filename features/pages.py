from browser import Browser
from selenium.webdriver.common.action_chains import ActionChains


class ItemListPage(Browser):
    def move_item(self, source, destination):

        template = '#neworder-{} .ui-sortable-handle'
        find = self.driver.find_element_by_css_selector
        offset = 2 if destination > source else -2
        (
            ActionChains(self.driver)
            .click_and_hold(find(template.format(source)))
            .move_to_element(find(template.format(destination)))
            .move_by_offset(0, offset)
            .release()
            .perform()
        )

    def open(self, context):
        url = context.get_url('admin:bdd_item_changelist')
        self.driver.get(url)
