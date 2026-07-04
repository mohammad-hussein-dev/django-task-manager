"""
Models for the accounts application.

This module defines the data models for user accounts and related functionality.
It currently uses Django's built-in User model without any custom extensions.

If additional user data is needed in the future, a Profile model can be added
to extend the User model with a one-to-one relationship. This approach follows
Django's recommended pattern for storing user-related data that doesn't belong
in the User model itself (e.g., bio, avatar, preferences).

For more information on extending the User model, see:
    https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#extending-the-existing-user-model
"""

# The default User model from Django's authentication framework is used directly.
# This provides fields for username, password, email, first_name, last_name,
# and permissions out of the box, which is sufficient for the current
# application requirements.
#
# from django.db import models
# from django.contrib.auth.models import User


# Example Profile model for future extension (commented out by default).
# If you need to store additional user data (e.g., bio, profile picture,
# preferred language, etc.), uncomment this class and run makemigrations.
#
# class Profile(models.Model):
#     """
#     Profile model extending the built-in User model with one-to-one relationship.
#
#     This model is used to store additional user data that is not part of
#     Django's default User model. It is linked to the User model via a
#     one-to-one relationship, ensuring each user has exactly one profile.
#     """
#     # One-to-one relationship with the built-in User model.
#     # CASCADE ensures the profile is deleted when the user is deleted.
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='profile',
#         help_text="The user associated with this profile"
#     )
#
#     # Additional fields for user data.
#     bio = models.TextField(
#         blank=True,
#         help_text="Short biography or description about the user"
#     )
#     # ... other fields such as avatar, date_of_birth, location, etc.
