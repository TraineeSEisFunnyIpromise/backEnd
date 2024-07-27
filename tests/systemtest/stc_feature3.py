from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch the browser (choose Chromium, Firefox, or WebKit)
    browser = p.chromium.launch(headless=False)  # Set headless=True for faster execution without browser window

    context = browser.new_context()
    page = context.new_page()

    # Login Test
    page.goto("http://localhost:4000/login")  # Replace with your login page URL

    page.fill("#username", "test1")  # Replace with your username
    page.fill("#password", "1234")  # Replace with your password
    page.click("#login-button")  # Replace with your login button selector



    success_message = page.text_content(".success-message")
    assert "Login successful" in success_message  # Adjust assertion if needed

    # Registration Test (Clear previous session data if needed)
    page.goto("http://localhost:4000/register")  # Replace with your registration page URL

    page.fill("#namename", "Test1")  # Replace with your registration form field names
    page.fill("#aboutme", "test@example.com")
    page.fill("#password", "12345678")
    page.click("#register-button")  # 

    page.wait_for_selector(".success-message", state="visible")  # Adjust selector if needed

    success_message = page.text_content(".success-message")
    assert "Registration successful" in success_message  # Adjust assertion if needed

    # Close browser context
    context.close()
    browser.close()
