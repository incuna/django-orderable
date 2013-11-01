from django.db import models

from ..models import Orderable


class Task(Orderable):
    """A basic orderable model for tests."""

