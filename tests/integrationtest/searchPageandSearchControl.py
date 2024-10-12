# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 

import time

# Define browser driver (replace with your preferred driver)
driver = webdriver.Chrome()  # Replace with your browser driver path

# Define base URL for your application
base_url = "http://localhost:4000"  # Replace with your application URL

# Define search data and target
search_data = "laptop"
target_data = "student"


def test_search_and_scrape_response():

    driver.get(f"{base_url}")  # Navigate to your application

    # Find search input elements and enter data
    search_input = driver.find_element(By.ID, "searchData")
    search_input.send_keys(search_data)

    target_input = driver.find_element(By.ID, "usertargetData")
    target_input.send_keys(target_data)

    # Find submit button and click
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # Wait for loading indicator or some element that signifies response received
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loader_criteria"))  # Replace with the ID of an element displayed after response
        )
    except TimeoutException:
        assert False, "Timed out waiting for response"

    # Check if result section appears (optional)
    result_section = driver.find_element(By.CSS_SELECTOR, ".colored-box-display")
    assert result_section.is_displayed(), "Result section not displayed"

    # Close the browser after the test
    driver.quit()

if __name__ == "__main__":
    test_search_and_scrape_response()