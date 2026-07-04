"""
Forms for the tasks application.

This module defines forms for creating and updating tasks,
with proper validation and Bootstrap 5 styling via crispy-forms.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Category, Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks.

    Includes a dynamic category field that allows selecting existing
    categories or creating a new one on the fly via category_name.
    """

    # Text input for category name (auto-creates or selects)
    category_name = forms.CharField(
        max_length=100,
        required=False,
        label=_("Category"),
        help_text=_("Enter an existing category name or create a new one."),
    )

    # Priority as a choice field with human-readable labels
    # The values map to the model's choices: ('low', 'medium', 'high')
    priority = forms.ChoiceField(
        choices=[
            ("low", _("Low")),
            ("medium", _("Medium")),
            ("high", _("High")),
        ],
        initial="medium",
        label=_("Priority"),
        required=True,
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_date",
            "status",
        ]  # removed priority, category
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "title": _("Title"),
            "description": _("Description"),
            "due_date": _("Due Date"),
            "status": _("Status"),
        }

    def __init__(self, *args, **kwargs):
        """Store user for category handling and set initial priority."""
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # If editing an existing task with a category, populate category_name
        if self.instance and self.instance.pk and self.instance.category:
            self.fields["category_name"].initial = self.instance.category.name

        # If editing an existing task, set initial priority
        if self.instance and self.instance.pk and self.instance.priority:
            self.fields["priority"].initial = self.instance.priority

    def save(self, commit=True):
        """Save the task and handle category creation/selection."""
        instance = super().save(commit=False)

        # Handle priority from the choice field
        priority_value = self.cleaned_data.get("priority")
        if priority_value:
            instance.priority = priority_value  # 'low', 'medium', or 'high'

        # Handle category
        category_name = self.cleaned_data.get("category_name")
        if category_name:
            user = self.user or getattr(instance, "user", None)
            if user:
                category, created = Category.objects.get_or_create(
                    name=category_name.strip(), user=user
                )
                instance.category = category
            else:
                instance.category = None
        else:
            instance.category = None

        if commit:
            instance.save()
            self.save_m2m()

        return instance
