from playwright.sync_api import sync_playwright,expect

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

    # Navigate to the user information page assume the login is worked
    page.goto('http://localhost:your-port/user-info')

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

    # Check if update was successful
    # This example assumes a simple success message
    update_success_element = page.locator('p:text-contains(Updated About Me Information)')
    expect(update_success_element.is_visible()).to_be_truthy()

    # Test Delete Functionality
    page.click('.deleteUserForm')  # Using class for delete button (not logged in)
    page.wait_for_timeout(2000)  # Wait for confirmation or redirect (adjust as needed)

    # Check if user was deleted (implement logic based on your backend response)
    # This example assumes a redirect to the homepage after deletion
    current_url = page.url
    expect(current_url).to_be('http://localhost:4000')  # Replace with your homepage URL

 
