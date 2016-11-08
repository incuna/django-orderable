from django.test import TestCase

from .models import SubTask, Task


class TestOrderableManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        tasks = [Task.objects.create(sort_order=i) for i in range(3)]
        cls.first_task, cls.middle_task, cls.last_task = tasks

    def test_gets_next(self):
        next_task = Task.objects.after(self.first_task)
        self.assertEqual(next_task, self.middle_task)

    def test_gets_previous(self):
        previous_task = Task.objects.before(self.last_task)
        self.assertEqual(previous_task, self.middle_task)

    def test_returns_none_if_after_on_last(self):
        next_task = Task.objects.after(self.last_task)
        self.assertIsNone(next_task)

    def test_returns_none_if_previous_on_first(self):
        previous_task = Task.objects.before(self.first_task)
        self.assertIsNone(previous_task)


class TestOrderableRelatedManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task = Task.objects.create()

        sub_tasks = [
            SubTask.objects.create(task=cls.task, sort_order=i) for i in range(3)
        ]
        cls.first_sub_task, cls.middle_sub_task, cls.last_sub_task = sub_tasks

    def test_gets_next(self):
        next_sub_task = self.task.subtask_set.after(self.first_sub_task)
        self.assertEqual(next_sub_task, self.middle_sub_task)

    def test_gets_previous(self):
        previous_sub_task = self.task.subtask_set.before(self.last_sub_task)
        self.assertEqual(previous_sub_task, self.middle_sub_task)

    def test_returns_none_if_after_on_last(self):
        next_sub_task = self.task.subtask_set.after(self.last_sub_task)
        self.assertIsNone(next_sub_task)

    def test_returns_none_if_previous_on_first(self):
        previous_sub_task = self.task.subtask_set.before(self.first_sub_task)
        self.assertIsNone(previous_sub_task)
