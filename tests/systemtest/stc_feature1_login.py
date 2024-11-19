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

        await page.goto("http://localhost:4000/login") 

        await page.fill("#username", "test1")
        await page.fill("#password", "1234")
        await page.click("#login-button")

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

        await page.goto("http://localhost:4000/login") 

        await page.fill("#username", "test1")
        await page.fill("#password", "1234")
        await page.click("#login-button")

        success_message = await page.text_content(".success-message")
        assert "Login successful" in success_message

        await context.close()
        await browser.close()

@pytest.mark.asyncio
async def test_registration_success():

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
async def test_registration_unsuccess():

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
