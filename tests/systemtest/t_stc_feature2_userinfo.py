from playwright.sync_api import sync_playwright,expect
import pytest
import asyncio
from playwright.async_api import async_playwright


@pytest.mark.asyncio
async def test_aboutme_success():
    with async_playwright() as p:
        browser = p.chromium.launch(headless=False)  

        context = browser.new_context()
        page = context.new_page()

        # Login Test
        page.goto("http://localhost:4000/login")  # Replace with your login page URL

        page.fill("#username", "test1")  # Replace with your username
        page.fill("#password", "1234")  # Replace with your password
        page.click("#login-button")  # Replace with your login button selector

        # Navigate to the user information page assume the login is worked
        page.wait(2000)

        # Check if user information is displayed (if logged in)
        username_element = page.locator('.username')  
        about_me_element = page.locator('p:text-contains(About me:)')

        if username_element.is_visible():
            # Username exists, verify its presence
            expect(username_element.inner_text).to_contain('Username: ')
        else:
            # No user information available
            expect(page.inner_text('p')).to_contain('No user information available')

        if about_me_element.is_visible():
            # About me exists, verify its presence
            expect(about_me_element.inner_text).to_contain('About me: ')

        # Test Update Functionality assuming logged in
        page.click('.updateUserForm')  # Using class for update button 
        page.wait_for_timeout(2000)  # Wait for update form to show 
        page.fill('input[type="text"]', 'Updated About Me Information')
        page.click('.updateUser')  # Using class for save button

        update_success_element = page.locator('p:text-contains(Updated About Me Information)')
        expect(update_success_element.is_visible()).to_be_truthy()

        # Test Delete Functionality
        page.click('.deleteUserForm') 
        page.wait_for_timeout(2000)  


        current_url = page.url
        expect(current_url).to_be('http://localhost:4000')  # Replace with your homepage URL

@pytest.mark.asyncio
async def test_updatepassword_success():
    with async_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://localhost:4000/login")  # Replace with your login page URL

        page.fill("#username", "test1")  # Replace with your username
        page.fill("#password", "1234")  # Replace with your password
        page.click("#login-button")  # Replace with your login button selector


        context = browser.new_context()
        page = context.new_page()

@pytest.mark.asyncio
async def test_updatepassword_unsuccess():
    with async_playwright() as p:
        browser = p.chromium.launch(headless=False)  

        context = browser.new_context()
        page = context.new_page()
 
