from django.db import models

from ..models import Orderable


class Task(Orderable):
    """A basic orderable model for tests."""


class SubTask(Orderable):
    """An orderable model with unique_together."""
    task = models.ForeignKey('Task')

    class Meta:
        unique_together = ('task', 'sort_order')
