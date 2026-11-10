
from pages.signup_page import SignupPage


def test_registration_lookup_empty_email(browser_page):
    # Create the SignupPage object using the existing browser fixture.
    signup = SignupPage(browser_page)

    # Open the Registration Lookup page.
    signup.open_registration_lookup_page()

    # Verify the required email message after leaving
    # the email field empty and moving focus away.
    signup.verify_email_required_error()

    # Verify that the Enter button remains disabled.
    signup.verify_enter_button_disabled()

    print("TC12 - Empty email validation test completed!")
