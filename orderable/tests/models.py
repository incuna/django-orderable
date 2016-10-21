from django.db import models

from ..models import Orderable


class Task(Orderable):
    """A basic orderable model for tests."""

    def __str__(self):
        return 'Task {}'.format(self.pk)


class SubTask(Orderable):
    """An orderable model with unique_together."""
    task = models.ForeignKey('Task')

    class Meta:
        unique_together = ('task', 'sort_order')

    def __str__(self):
        return 'SubTask {}'.format(self.pk)


class TodoList(models.Model):
    """Parent model"""
    pass


class Todo(Orderable):
    """Child orderable, for the unique together bug"""
    name = models.CharField(max_length='255', default='')
    list = models.ForeignKey(TodoList, related_name='todos')

    class Meta:
        unique_together = ('name', 'list')


