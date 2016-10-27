from django.db import models

from ..models import Orderable


class Task(Orderable):
    """A basic orderable model for tests."""

    def __str__(self):
        return 'Task {}'.format(self.pk)


class SubTask(Orderable):
    """An orderable model with unique_together."""
    task = models.ForeignKey('Task')

    class Meta(Orderable.Meta):
        unique_together = ('task', 'sort_order')

    def __str__(self):
        return 'SubTask {}'.format(self.pk)
