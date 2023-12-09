import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestE2E(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # You need to have ChromeDriver installed and in your PATH
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_add_update_delete_product_flow(self):
        # Open the application
        self.driver.get('http://localhost:5000/')

        # Add a product
        add_product_button = self.driver.find_element_by_link_text('Add Product')
        add_product_button.click()

        name_input = self.driver.find_element_by_id('name')
        name_input.send_keys('E2E Test Product')

        description_input = self.driver.find_element_by_id('description')
        description_input.send_keys('E2E Test Description')

        add_button = self.driver.find_element_by_xpath('//button[@type="submit"]')
        add_button.click()

        # Check if the added product is displayed on the index page
        self.assertIn('E2E Test Product', self.driver.page_source)

        # Update the added product
        update_link = self.driver.find_element_by_xpath('//a[@class="update-link"]')
        update_link.click()

        name_input = self.driver.find_element_by_id('name')
        name_input.clear()
        name_input.send_keys('Updated E2E Test Product')

        description_input = self.driver.find_element_by_id('description')
        description_input.clear()
        description_input.send_keys('Updated E2E Test Description')

        update_button = self.driver.find_element_by_xpath('//button[@type="submit"]')
        update_button.click()

        # Check if the updated product is displayed on the index page
        self.assertIn('Updated E2E Test Product', self.driver.page_source)

        # Delete the updated product
        delete_link = self.driver.find_element_by_xpath('//a[@class="delete-link"]')
        delete_link.click()

        # Check if the deleted product is no longer displayed on the index page
        self.assertNotIn('Updated E2E Test Product', self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
