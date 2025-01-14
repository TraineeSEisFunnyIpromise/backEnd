import pytest
import asyncio
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_login_success():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:4000/login") 

        await page.fill("#username", "test1")
        await page.fill("#password", "1234")
        await page.click("#login-button")

        success_message = await page.text_content(".success-message")
        assert "Login successful" in success_message

        await context.close()
        await browser.close()

@pytest.mark.asyncio
async def test_login_unsuccess():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:4000/login") 

        await page.fill("#username", "test1")
        await page.fill("#password", "12345678")
        await page.click("#login-button")

        success_message = await page.text_content(".unsuccess-message")
        assert "Login unsuccessful" in success_message

        await context.close()
        await browser.close()

@pytest.mark.asyncio
async def test_resetpassword_success():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:4000/resetpassword") 

        await page.fill("#username", "test1")
        await page.fill("#password", "1234")
        await page.click("#reset-button")

        success_message = await page.text_content(".success-message")
        assert "Login successful" in success_message

        await context.close()
        await browser.close()
        
@pytest.mark.asyncio
async def test_resetpassword_unsuccess():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:4000/resetpassword") 

        await page.fill("#username_reset", "te")
        await page.click('button[id="submit_resetuser"]')


        success_message = await page.text_content(".success-message")
        assert "reset password successful" in success_message

        await context.close()
        await browser.close()

@pytest.mark.asyncio
async def test_registration_success():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:4000/login") 

        await page.fill("#username_reset", "test1")
        await page.click('button[id="submit_resetuser"]')
        
        await page.fill("#answer", "1234")
        
        await page.fill("#password_reset", "12345678")

        success_message = await page.text_content(".result")
        assert "Reset password successful" in success_message

        await context.close()
        await browser.close()

@pytest.mark.asyncio
async def test_registration_unsuccess():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("http://localhost:4000/login") 

        await page.fill("#username", "test1")
        await page.fill("#password", "1234")
        await page.click("#login-button")

        success_message = await page.text_content(".result")
        assert "user not found" in success_message

        await page.wait_for_timeout(2000)

        await page.fill("#username_reset", "test1")
        await page.click('button[id="submit_resetuser"]')
        
        await page.fill("#answer", "124")
        

        success_message = await page.text_content(".result")
        assert "Reset password Unsuccessfully" in success_message


        await context.close()
        await browser.close()
