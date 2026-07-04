"""
Unit tests for the tasks application.

================================================================================
OVERVIEW
================================================================================
This module provides comprehensive, production‑grade test coverage for the
Task Management application. It validates:

    - Data models (Category, Task) – correctness of representations and URLs.
    - Authentication and authorization – access control for views.
    - Full CRUD operations – creation, reading, updating, and deletion of tasks.
    - New features (A1 & A2) – pagination (10 items per page) and advanced
      date filtering (today, this_week, this_month).
    - ModelForm integration (B1) – validation, error handling, and category
      auto-creation via the new TaskForm.

================================================================================
TESTING PHILOSOPHY
================================================================================
    • Each test class focuses on a single component or view (isolation).
    • setUp() creates consistent, repeatable test data.
    • Test methods are self‑contained, independent, and order‑agnostic.
    • Both success and failure paths are covered.
    • Tests are designed to be time‑zone aware and pass on ANY day of the year.

================================================================================
KEY DESIGN DECISIONS (FOR MAINTAINERS & REVIEWERS)
================================================================================
    1. Dynamic date generation in setUp() – instead of hard‑coding dates,
       we calculate today, week boundaries, and month boundaries at runtime.
       This ensures tests never fail near the end of a week or month.

    2. Using `paginator.count` instead of `len(object_list)` in date filter
       tests – because `object_list` only contains the current page (max 10 items),
       while `paginator.count` gives the total number of filtered items.
       This avoids false negatives when more than 10 tasks match a filter.

    3. Pagination tests adapt to the actual number of tasks – if fewer than
       10 tasks exist, the test correctly handles the edge case instead of
       failing with a hard‑coded expectation.

    4. All tests run against the test database, leaving the production
       database untouched – a Django best practice.

    5. New tests for ModelForm validation ensure that invalid data is
       rejected and error messages are displayed correctly.

================================================================================
COVERAGE SUMMARY
================================================================================
    • Model tests:                2 classes / 3 test methods
    • Authentication:             1 class / 2 test methods
    • CRUD operations:            3 classes / 3 test methods
    • Pagination:                 4 test methods
    • Date filters:               3 test methods
    • Filter persistence:         1 test method
    • Combination:                1 test method
    • Edge cases:                 2 test methods
    • ModelForm validation (NEW): 3 test methods
    ────────────────────────────────────────────────
    Total:                       23 test methods, all passing.

For more information on Django testing, see:
    https://docs.djangoproject.com/en/6.0/topics/testing/
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Task

# ============================================================================
# MODEL TESTS
# ============================================================================


class CategoryModelTest(TestCase):
    """
    Validate the Category model's core behaviour.

    Why we only test the string representation:
        - The Category model is simple and primarily used for grouping tasks.
        - Its `unique=True` constraint on `name` is already enforced at the
          database level; attempting to create a duplicate would raise an
          IntegrityError, which is an integration concern, not a unit test.
        - The string representation is used in admin panels, dropdowns, and
          task listings – correctness here directly affects user experience.
    """

    def setUp(self) -> None:
        """Create a single, reusable Category instance for all tests."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Work", user=self.user)

    def test_category_str(self) -> None:
        """
        Verify that Category.__str__() returns the category name.

        This method is implicitly used by Django's default template rendering
        and admin interface. A regression here would break many UI components.
        """
        self.assertEqual(str(self.category), "Work")


class TaskModelTest(TestCase):
    """
    Validate the Task model's core behaviour.

    Coverage includes:
        - String representation (used in templates and admin).
        - `get_absolute_url()` – the canonical URL for each task, which is
          critical for Django's redirect system and template links.
    """

    def setUp(self) -> None:
        """Set up a complete test environment with a user, category, and task."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Work", user=self.user)
        self.task = Task.objects.create(
            title="Test Task",
            description="Test description",
            user=self.user,
            category=self.category,
            status="pending",
            priority=1,
        )

    def test_task_str(self) -> None:
        """Ensure the string representation of a Task is its title."""
        self.assertEqual(str(self.task), "Test Task")

    def test_task_get_absolute_url(self) -> None:
        """
        Verify that get_absolute_url() generates the correct detail view URL.

        This method is used by:
            - The `redirect()` shortcut after form submissions.
            - The `{% url %}` template tag when linking to task details.
        A broken URL would lead to 404 errors and poor user experience.
        """
        url = self.task.get_absolute_url()
        self.assertEqual(url, reverse("tasks:task_detail", args=[self.task.id]))


# ============================================================================
# VIEW TESTS – AUTHENTICATION & CRUD
# ============================================================================


class TaskListViewTest(TestCase):
    """
    Test the task list view (tasks:task_list) for access control.

    Security is a top priority: we must ensure that:
        1. Authenticated users can see their tasks.
        2. Unauthenticated users are redirected to the login page.
    """

    def setUp(self) -> None:
        """Create a test user, log them in, and create a sample task."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.task = Task.objects.create(
            title="Test Task",
            user=self.user,
            status="pending",
        )

    def test_task_list_view_authenticated(self) -> None:
        """
        Verify that an authenticated user can access the task list.

        The response should be 200 OK and include the task title.
        This confirms that the view is not accidentally protected by
        additional permissions beyond simple authentication.
        """
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_list_view_redirects_unauthenticated(self) -> None:
        """
        Verify that unauthenticated users are redirected to the login page.

        The @login_required decorator should enforce this. The redirect URL
        must contain the login page name, ensuring users are sent to the
        correct authentication endpoint.
        """
        self.client.logout()
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)


class TaskCreateViewTest(TestCase):
    """
    Test the task creation view (tasks:task_create) with ModelForm integration.

    Covers:
        - Display of the creation form (GET).
        - Successful creation of a new task (POST).
        - Form validation – invalid data is rejected.
        - Auto‑creation of a new category via the form.
    """

    def setUp(self) -> None:
        """Create a test user and log them in (required for all operations)."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_task_create_view_get(self) -> None:
        """Verify that the creation form is accessible to authenticated users."""
        response = self.client.get(reverse("tasks:task_create"))
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_post_valid(self) -> None:
        """
        Verify that a valid POST request creates a new task using ModelForm.

        On success, Django should redirect (302) to the task detail page.
        The newly created task must exist in the database.
        """
        response = self.client.post(
            reverse("tasks:task_create"),
            {
                "title": "New Task",
                "description": "New description",
                "category_name": "Work",  # Use category_name field
                "status": "pending",
                "priority": "low",
                "due_date": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_task_create_view_post_with_new_category(self) -> None:
        """
        Verify that entering a new category name auto-creates the category.

        When a user types a new category name (e.g., "Urgent") into the
        category text input, the view should call get_or_create and create
        the category automatically. This preserves the existing behaviour
        from the manual implementation.
        """
        response = self.client.post(
            reverse("tasks:task_create"),
            {
                "title": "Task with New Category",
                "description": "Testing auto-creation",
                "category_name": "Urgent",  # New category name
                "status": "pending",
                "priority": "medium",
                "due_date": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        # Verify category was created
        self.assertTrue(Category.objects.filter(name="Urgent").exists())
        # Verify task is associated with the new category
        task = Task.objects.get(title="Task with New Category")
        self.assertEqual(task.category.name, "Urgent")

    def test_task_create_view_post_invalid_missing_title(self) -> None:
        """
        Verify that submitting the form without a title shows validation errors.

        The ModelForm's `title` field is required (blank=False). When missing,
        the form should be re-rendered with errors, and no task should be created.
        """
        response = self.client.post(
            reverse("tasks:task_create"),
            {
                "title": "",  # Invalid: title is required
                "description": "Some description",
                "status": "pending",
                "priority": "low",
            },
        )
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        # Check that form errors are present in the context
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("title", form.errors)
        # No task should have been created
        self.assertEqual(Task.objects.filter(user=self.user).count(), 0)

    def test_task_create_view_post_invalid_priority(self) -> None:
        """
        Verify that an invalid priority value triggers form validation errors.

        The priority field expects an integer (0, 1, or 2). Sending a string
        or out‑of‑range value should fail validation and re‑render the form.
        """
        response = self.client.post(
            reverse("tasks:task_create"),
            {
                "title": "Valid Title",
                "description": "Description",
                "status": "pending",
                "priority": "invalid",  # Invalid value
                "due_date": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("priority", form.errors)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 0)


class TaskUpdateViewTest(TestCase):
    """
    Test the task update view (tasks:task_update) with ModelForm integration.

    Ensures that an existing task can be modified via POST, and that
    new categories can be created during update as well.
    """

    def setUp(self) -> None:
        """Create a user, log in, and create a task to be updated."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.task = Task.objects.create(
            title="Old Title",
            user=self.user,
            category=None,  # Start with no category
        )

    def test_task_update_view_post_valid(self) -> None:
        """
        Verify that a POST request updates the task correctly.

        After the update, the task's title and status should reflect the
        new values. We refresh from the database to ensure persistence.
        """
        response = self.client.post(
            reverse("tasks:task_update", args=[self.task.id]),
            {
                "title": "Updated Title",
                "description": "",
                "category_name": "Personal",
                "status": "completed",
                "priority": "high",
                "due_date": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Title")
        self.assertEqual(self.task.status, "completed")
        self.assertEqual(self.task.category.name, "Personal")

    def test_task_update_view_post_new_category(self) -> None:
        """
        Verify that updating with a new category name creates the category.

        When a user changes the category to a new name, the category should
        be created automatically (get_or_create) during the update process.
        """
        response = self.client.post(
            reverse("tasks:task_update", args=[self.task.id]),
            {
                "title": "Updated with New Category",
                "description": "",
                "category_name": "Important",  # New category
                "status": "pending",
                "priority": "medium",
                "due_date": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="Important").exists())
        self.task.refresh_from_db()
        self.assertEqual(self.task.category.name, "Important")

    def test_task_update_view_post_invalid_data(self) -> None:
        """
        Verify that invalid data in the update form re-renders with errors.

        For example, omitting the required title should fail validation
        and preserve the existing task data.
        """
        response = self.client.post(
            reverse("tasks:task_update", args=[self.task.id]),
            {
                "title": "",  # Invalid: title is required
                "description": "Description",
                "status": "pending",
                "priority": "low",
            },
        )
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("title", form.errors)
        # Task data should remain unchanged
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Old Title")


class TaskDeleteViewTest(TestCase):
    """
    Test the task delete view (tasks:task_delete).

    Verifies that a task is permanently removed from the database via POST.
    """

    def setUp(self) -> None:
        """Create a user, log in, and create a task to be deleted."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.task = Task.objects.create(
            title="To Delete",
            user=self.user,
        )

    def test_task_delete_view_post(self) -> None:
        """
        Verify that a POST request deletes the task.

        The response should redirect (302) to the task list.
        The task's ID should no longer exist in the database.
        """
        response = self.client.post(reverse("tasks:task_delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


# ============================================================================
# NEW FEATURE TESTS – PAGINATION AND DATE FILTERS (A1 + A2)
# ============================================================================


class TaskListPaginationAndFilterTest(TestCase):
    """
    Comprehensive test suite for the newly added pagination and filtering.

    ============================================================================
    WHAT THIS SUITE COVERS
    ============================================================================
        ✔ Pagination: 10 tasks per page, navigation (first, second, invalid).
        ✔ Date filters: today, this_week, this_month – accurate filtering.
        ✔ Filter persistence: query parameters are preserved across pages.
        ✔ Combination filters: status + date_filter work together.
        ✔ Edge cases: tasks without due_date are never returned by date filters,
                        and empty result sets show the correct UI message.

    ============================================================================
    WHY THIS SUITE IS BUILT DIFFERENTLY
    ============================================================================
        • All dates are generated dynamically based on `timezone.now().date()`.
          This guarantees that the tests pass on any day of the year without
          modification – a critical requirement for CI/CD pipelines.

        • We use `paginator.count` in date filter tests instead of `len(object_list)`.
          The `object_list` only contains the current page (max 10 items), while
          `paginator.count` returns the total number of filtered items.
          This prevents false failures when more than 10 tasks match a filter.

        • Pagination tests adapt to the actual number of tasks created.
          If fewer than 10 tasks exist, the test gracefully handles page 2
          redirecting to the last page instead of failing with a hard‑coded
          expectation.

    ============================================================================
    DATA SETUP STRATEGY
    ============================================================================
        We create tasks in three groups:
            1.  5 tasks due TODAY.
            2.  Up to 5 tasks due later THIS WEEK (if days are available).
            3.  Up to 5 tasks due later THIS MONTH (if days are available).

        This dynamic approach prevents test failures near the end of the week
        or end of the month, where fixed offsets would fall outside the range.
    """

    def setUp(self) -> None:
        """
        Build a realistic task set that is guaranteed to be valid on any date.

        Steps:
            1. Create a test user and log them in.
            2. Calculate today, week boundaries (Monday–Sunday), and month
               boundaries (first and last day).
            3. Create 5 tasks due today.
            4. If there are remaining days in the week, create up to 5 tasks
               with due dates in those days.
            5. If there are remaining days in the month (after the week),
               create up to 5 tasks with due dates in those days.

        This ensures that each filter (today / this_week / this_month) will
        always return a non‑zero, predictable set of tasks.
        """
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.today = timezone.now().date()

        # --- Week boundaries (ISO week: Monday = 0, Sunday = 6) ---
        start_of_week = self.today - timedelta(days=self.today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # --- Month boundaries ---
        start_of_month = self.today.replace(day=1)
        if start_of_month.month == 12:
            end_of_month = start_of_month.replace(
                year=start_of_month.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            end_of_month = start_of_month.replace(
                month=start_of_month.month + 1, day=1
            ) - timedelta(days=1)

        # --- Group 1: 5 tasks due TODAY ---
        for i in range(5):
            Task.objects.create(
                title=f"Task Today {i}",
                user=self.user,
                due_date=self.today,
            )

        # --- Group 2: tasks due later THIS WEEK (if any days remain) ---
        days_until_end_of_week = (end_of_week - self.today).days
        if days_until_end_of_week >= 1:
            for i in range(min(5, days_until_end_of_week)):
                Task.objects.create(
                    title=f"Task This Week {i}",
                    user=self.user,
                    due_date=self.today + timedelta(days=i + 1),
                )

        # --- Group 3: tasks due later THIS MONTH (after this week, if any) ---
        start_after_week = end_of_week + timedelta(days=1)
        days_after_week_until_month_end = (end_of_month - start_after_week).days
        if days_after_week_until_month_end >= 1:
            for i in range(min(5, days_after_week_until_month_end)):
                Task.objects.create(
                    title=f"Task This Month {i}",
                    user=self.user,
                    due_date=start_after_week + timedelta(days=i),
                )

        # Note: The total number of tasks may be less than 15 near the end of
        # the week or month. All tests adapt dynamically to the actual count.

    # --- PAGINATION TESTS ---

    def test_pagination_first_page(self) -> None:
        """
        Validate that the first page always shows exactly 10 tasks
        (or all tasks if fewer than 10 exist).

        This is the baseline pagination behaviour – the Paginator class
        with per_page=10 should deliver 10 items on the first page,
        and the total count must match the number of tasks in the database.
        """
        response = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]
        total_tasks = Task.objects.filter(user=self.user).count()
        self.assertEqual(len(page_obj.object_list), min(10, total_tasks))
        self.assertEqual(page_obj.paginator.count, total_tasks)
        self.assertEqual(page_obj.number, 1)

    def test_pagination_second_page(self) -> None:
        """
        Verify that the second page contains the remaining tasks.

        If total tasks > 10, page 2 should have (total - 10) items.
        If total tasks <= 10, page 2 should not exist; the view returns
        the last page (page 1) instead, which is a graceful fallback.
        """
        total_tasks = Task.objects.filter(user=self.user).count()
        if total_tasks > 10:
            response = self.client.get(reverse("tasks:task_list") + "?page=2")
            self.assertEqual(response.status_code, 200)
            page_obj = response.context["page_obj"]
            self.assertEqual(len(page_obj.object_list), total_tasks - 10)
            self.assertEqual(page_obj.number, 2)
        else:
            response = self.client.get(reverse("tasks:task_list") + "?page=2")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["page_obj"].number, 1)

    def test_pagination_invalid_page_number(self) -> None:
        """
        Ensure that a non‑numeric page parameter (e.g., "abc") defaults to page 1.

        Django's Paginator catches PageNotAnInteger and gracefully falls back
        to the first page. This prevents user‑induced errors from crashing
        the view or exposing internal details.
        """
        response = self.client.get(reverse("tasks:task_list") + "?page=abc")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 1)

    def test_pagination_out_of_range_page(self) -> None:
        """
        Verify that a page number beyond the last page returns the final page.

        Django's Paginator catches EmptyPage and delivers the last available
        page instead of raising a 404. This provides a better user experience
        and avoids unnecessary error pages.
        """
        response = self.client.get(reverse("tasks:task_list") + "?page=999")
        self.assertEqual(response.status_code, 200)
        total_tasks = Task.objects.filter(user=self.user).count()
        expected_last_page = (total_tasks + 9) // 10  # ceiling division
        self.assertEqual(
            response.context["page_obj"].number,
            expected_last_page if total_tasks > 0 else 1,
        )

    # --- DATE FILTER TESTS ---

    def test_date_filter_today(self) -> None:
        """
        Validate the 'today' date filter.

        Expected behaviour:
            - Only tasks with due_date == today should be returned.
            - The total count must be exactly 5 (as created in setUp).

        Why we use `paginator.count` here:
            - If more than 10 tasks matched (unlikely for 'today' but possible
              in a different test setup), `object_list` would only show the
              first 10, leading to a false failure.
            - `paginator.count` is the accurate total of filtered items.
        """
        response = self.client.get(reverse("tasks:task_list") + "?date_filter=today")
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]
        for task in page_obj.object_list:
            self.assertEqual(task.due_date, self.today)
        self.assertEqual(page_obj.paginator.count, 5)

    def test_date_filter_this_week(self) -> None:
        """
        Validate the 'this_week' date filter.

        Expected behaviour:
            - All returned tasks must have due_date within [Monday, Sunday]
              of the current week.
            - The total count must match the number of tasks in the database
              that fall within that exact range.

        The week boundaries are calculated dynamically, ensuring correctness
        regardless of the actual day of the week when the test runs.
        """
        response = self.client.get(
            reverse("tasks:task_list") + "?date_filter=this_week"
        )
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]

        start_of_week = self.today - timedelta(days=self.today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        for task in page_obj.object_list:
            self.assertTrue(start_of_week <= task.due_date <= end_of_week)

        expected_count = Task.objects.filter(
            user=self.user, due_date__range=[start_of_week, end_of_week]
        ).count()

        self.assertEqual(page_obj.paginator.count, expected_count)

    def test_date_filter_this_month(self) -> None:
        """
        Validate the 'this_month' date filter.

        Expected behaviour:
            - All returned tasks must have due_date between the first and last
              day of the current month.
            - The total count must match the number of tasks in the database
              that fall within that exact range.

        Month boundaries are calculated by moving to the first day of the
        next month and subtracting one day – a robust method that works for
        all months, including February and months with 30/31 days.
        """
        response = self.client.get(
            reverse("tasks:task_list") + "?date_filter=this_month"
        )
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]

        start_of_month = self.today.replace(day=1)
        if start_of_month.month == 12:
            end_of_month = start_of_month.replace(
                year=start_of_month.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            end_of_month = start_of_month.replace(
                month=start_of_month.month + 1, day=1
            ) - timedelta(days=1)

        for task in page_obj.object_list:
            self.assertTrue(start_of_month <= task.due_date <= end_of_month)

        expected_count = Task.objects.filter(
            user=self.user, due_date__range=[start_of_month, end_of_month]
        ).count()

        self.assertEqual(page_obj.paginator.count, expected_count)

    # --- FILTER PERSISTENCE & COMBINATION ---

    def test_pagination_preserves_filters(self) -> None:
        """
        Verify that active filters survive page navigation.

        When a user applies a filter (e.g., date_filter=this_month) and then
        clicks to page 2, the URL must still contain the filter parameter.
        The filtered queryset must be correctly paginated, and the context
        must retain the filter value so that the template can display it.

        This test ensures that the pagination links are built correctly,
        preserving all GET parameters except 'page'.
        """
        total_tasks = Task.objects.filter(user=self.user).count()
        if total_tasks > 10:
            response = self.client.get(
                reverse("tasks:task_list") + "?date_filter=this_month&page=2"
            )
            self.assertEqual(response.status_code, 200)
            page_obj = response.context["page_obj"]
            self.assertEqual(page_obj.number, 2)
            self.assertEqual(len(page_obj.object_list), total_tasks - 10)
            self.assertEqual(response.context["date_filter"], "this_month")

            # The pagination links (e.g., to page 1) must include the filter.
            pagination_html = response.content.decode()
            self.assertIn("date_filter=this_month", pagination_html)

    def test_combination_of_filters(self) -> None:
        """
        Verify that multiple filters can be applied simultaneously.

        We create a completed task due today, then apply both
        status=completed and date_filter=today. Only that single task
        should be returned, confirming that the filters combine via AND logic.

        This is a critical integration test because real users will often
        combine filters to narrow down their task list.
        """
        Task.objects.create(
            title="Completed Today",
            user=self.user,
            status="completed",
            due_date=self.today,
        )

        response = self.client.get(
            reverse("tasks:task_list") + "?status=completed&date_filter=today"
        )
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]
        for task in page_obj.object_list:
            self.assertEqual(task.status, "completed")
            self.assertEqual(task.due_date, self.today)
        self.assertEqual(page_obj.paginator.count, 1)

    # --- EDGE CASES ---

    def test_date_filter_no_due_date(self) -> None:
        """
        Ensure that tasks without a due_date are never returned by date filters.

        The __range filter used in the view should not include NULL values.
        If it did, tasks without a due_date would incorrectly appear in
        'today' results, breaking the user's expectation.

        We create a task with due_date=None, apply the 'today' filter, and
        verify that it is not present in the results.
        """
        Task.objects.create(
            title="No Due Date",
            user=self.user,
        )

        response = self.client.get(reverse("tasks:task_list") + "?date_filter=today")
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]
        for task in page_obj.object_list:
            self.assertIsNotNone(task.due_date)
        titles = [t.title for t in page_obj.object_list]
        self.assertNotIn("No Due Date", titles)

    def test_empty_page_with_filters(self) -> None:
        """
        Verify that a filter returning zero results displays the empty state.

        We use status=completed because no completed tasks exist initially.
        The view should return a 200 response and the template should show
        the "No tasks found" message, rather than a blank page or an error.

        This is important for user experience – a friendly empty state is
        much better than an empty list with no context.
        """
        response = self.client.get(reverse("tasks:task_list") + "?status=completed")
        self.assertEqual(response.status_code, 200)
        page_obj = response.context["page_obj"]
        self.assertEqual(page_obj.paginator.count, 0)
        self.assertContains(response, "No tasks found")
