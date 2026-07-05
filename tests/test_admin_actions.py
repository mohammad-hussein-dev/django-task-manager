"""
Tests for custom admin actions to cover lines 107 and 113 in admin.py.
"""
import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.contrib.auth.models import User
from tasks.models import Task
from tasks.admin import TaskAdmin


@pytest.mark.django_db
def test_admin_mark_as_completed():
    user = User.objects.create_user(username='testuser', password='testpass')
    task1 = Task.objects.create(title='Task 1', user=user, status='pending')
    task2 = Task.objects.create(title='Task 2', user=user, status='in_progress')
    
    admin = TaskAdmin(Task, AdminSite())
    request = RequestFactory().get('/admin/tasks/task/')
    request.user = user
    
    # خط 107: فراخوانی متد mark_as_completed
    response = admin.mark_as_completed(request, Task.objects.filter(pk__in=[task1.pk, task2.pk]))
    task1.refresh_from_db()
    task2.refresh_from_db()
    assert task1.status == 'completed'
    assert task2.status == 'completed'


@pytest.mark.django_db
def test_admin_mark_as_pending():
    user = User.objects.create_user(username='testuser', password='testpass')
    task1 = Task.objects.create(title='Task 1', user=user, status='completed')
    task2 = Task.objects.create(title='Task 2', user=user, status='in_progress')
    
    admin = TaskAdmin(Task, AdminSite())
    request = RequestFactory().get('/admin/tasks/task/')
    request.user = user
    
    # خط 113: فراخوانی متد mark_as_pending
    response = admin.mark_as_pending(request, Task.objects.filter(pk__in=[task1.pk, task2.pk]))
    task1.refresh_from_db()
    task2.refresh_from_db()
    assert task1.status == 'pending'
    assert task2.status == 'pending'
