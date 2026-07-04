"""
Unit tests for the accounts application.

This module provides comprehensive test coverage for user authentication
and account management functionality, including:
- User registration
- Login and logout
- Form validation
- Redirect behavior
- HTTP method handling

The tests follow Django's testing best practices:
- Each test focuses on a single piece of functionality
- setUp() creates consistent test data
- Test methods are self-contained and independent
- Both successful and failure cases are covered

For more information on Django testing, see:
    https://docs.djangoproject.com/en/6.0/topics/testing/
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTest(TestCase):
    """
    Test cases for authentication views.

    This class covers the full authentication flow:
        - Registration: GET form display and POST submission
        - Login: GET form display and POST authentication
        - Logout: POST request with proper CSRF protection

    All tests use the Django test client to simulate HTTP requests
    and verify responses, redirects, and database state changes.
    """

    def setUp(self) -> None:
        """
        Set up test environment before each test method.

        Creates a test user that can be used across multiple test cases.
        This user is available for login tests and as a reference for
        checking that registration creates new users successfully.

        The user is created with:
            - username: testuser
            - password: testpass (stored hashed by Django)
            - email: test@example.com
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com",
        )

    # ==========================================================================
    # REGISTRATION TESTS
    # ==========================================================================

    def test_register_view_get(self) -> None:
        """
        Verify that the registration form is accessible via GET request.

        The registration page should be publicly accessible without requiring
        authentication. This test ensures that new users can reach the
        registration form to create an account.

        Expected behavior:
            - Response status code: 200 (OK)
            - The registration form is rendered successfully
        """
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_success(self) -> None:
        """
        Verify that a valid registration request creates a new user.

        When a user submits valid registration data (username, password1, password2),
        the system should:
            - Create a new user record in the database
            - Redirect to the login page (or task list)
            - Not return any errors

        This test uses a unique username to avoid conflicts and follows
        Django's UserCreationForm validation rules.
        """
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            },
        )
        # Successful registration redirects (302) to the task list.
        self.assertEqual(response.status_code, 302)

        # Verify that the new user was actually created in the database.
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_view_post_invalid(self) -> None:
        """
        Verify that invalid registration data shows errors.

        When a user submits invalid registration data (e.g., empty username,
        weak password), the system should:
            - Re-render the registration form with error messages
            - Not create a new user record
            - Return status code 200 (OK, with errors displayed)

        This test simulates a user submitting an empty username and an
        invalid password (too short/common).
        """
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "",  # Empty username — should trigger validation error
                "password1": "pass",  # Too short — should trigger validation error
                "password2": "pass",
            },
        )
        # The form should re-render with errors (status 200).
        self.assertEqual(response.status_code, 200)

    # ==========================================================================
    # LOGIN TESTS
    # ==========================================================================

    def test_login_view_get(self) -> None:
        """
        Verify that the login form is accessible via GET request.

        The login page should be publicly accessible without requiring
        authentication. This test ensures that users can reach the
        login form to authenticate.

        Expected behavior:
            - Response status code: 200 (OK)
            - The login form is rendered successfully
        """
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_success(self) -> None:
        """
        Verify that valid credentials successfully authenticate a user.

        When a user submits valid login credentials (username, password),
        the system should:
            - Authenticate the user
            - Redirect to the task list (LOGIN_REDIRECT_URL)
            - Create a session for the authenticated user

        This test uses the test user created in setUp() and verifies
        that the correct redirect URL is used.
        """
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "testuser",
                "password": "testpass",
            },
        )
        # Successful login redirects (302) to the task list.
        self.assertEqual(response.status_code, 302)

        # Verify that the redirect target is correct.
        self.assertRedirects(response, reverse("tasks:task_list"))

    # ==========================================================================
    # LOGOUT TESTS
    # ==========================================================================

    def test_logout_view(self) -> None:
        """
        Verify that logout works correctly with a POST request.

        Logout should be performed via POST request to prevent CSRF attacks
        and accidental logouts from GET requests (e.g., from image tags or
        malicious links).

        Expected behavior:
            - The user is logged out
            - Response status code: 302 (redirect)
            - Redirect to the login page (LOGOUT_REDIRECT_URL)

        Using POST for logout is a security best practice in Django and
        follows the pattern used by Django's built-in LogoutView.
        """
        self.client.login(username="testuser", password="testpass")

        # Use POST (not GET) to avoid 405 Method Not Allowed.
        response = self.client.post(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_logout_get_returns_405(self) -> None:
        """
        Verify that GET requests to logout return 405 Method Not Allowed.

        Django's LogoutView only accepts POST requests for security reasons.
        GET requests should be rejected with a 405 status code to prevent
        cross-site request forgery (CSRF) attacks and accidental logouts.

        This test ensures that the logout endpoint is properly configured
        to reject unsafe HTTP methods.

        Expected behavior:
            - Response status code: 405 (Method Not Allowed)
            - The user remains logged in (since GET is not processed)
        """
        self.client.login(username="testuser", password="testpass")

        # GET request to logout should be rejected.
        response = self.client.get(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 405)  # Method not allowed
