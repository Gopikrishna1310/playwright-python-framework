from pages.common.login_page import LoginPage


# =========================================================
# FEATURE: Login Functionality
#
# SCENARIO:
# Verify valid login with Company Admin role
#
# TEST STEPS:
# 1. Open login page
# 2. Enter valid username
# 3. Enter valid password
# 4. Click Sign In
# 5. Verify organization selection screen
# 6. Select organization
# 7. Select Company Admin role
# 8. Click Continue
#
# EXPECTED RESULT:
# Admin home page should be displayed successfully
# =========================================================


def test_valid_login(page):

    # Create LoginPage object
    login_page = LoginPage(page)

    # Step 1: Open login page
    login_page.open_login_page()

    # Step 2-8: Perform login flow
    login_page.login(
        "admin@objectways.com",
        "Admin123!"
    )

    # Step 9: Capture current URL
    current_url = page.url

    print(f"\nCurrent URL: {current_url}")

    # Step 10: Validate successful login
    assert "login" not in current_url.lower()

    print("Login Successful")