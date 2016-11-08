from django.test import TestCase

from .models import SubTask, Task


class TestOrderableManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tasks = []
        for i in range(3):
            task = Task(sort_order=i)
            task.save()
            cls.tasks.append(task)

    def test_gets_next(self):
        first_task = self.tasks[0]
        next_task = Task.objects.after(first_task)
        self.assertEqual(next_task, self.tasks[1])

    def test_gets_previous(self):
        last_task = self.tasks[2]
        previous_task = Task.objects.before(last_task)
        self.assertEqual(previous_task, self.tasks[1])

    def test_returns_none_if_after_on_last(self):
        last_task = self.tasks[2]
        next_task = Task.objects.after(last_task)
        self.assertIsNone(next_task)

    def test_returns_none_if_previous_on_first(self):
        first_task = self.tasks[0]
        previous_task = Task.objects.before(first_task)
        self.assertIsNone(previous_task)


class TestOrderableRelatedManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.task = Task()
        cls.task.save()

        cls.sub_tasks = []
        for i in range(3):
            sub = SubTask(task=cls.task, sort_order=i)
            sub.save()
            cls.sub_tasks.append(sub)

    def test_gets_next(self):
        first_sub_task = self.sub_tasks[0]
        next_sub_task = self.task.subtask_set.after(first_sub_task)
        self.assertEqual(next_sub_task, self.sub_tasks[1])

    def test_gets_previous(self):
        last_sub_task = self.sub_tasks[2]
        previous_sub_task = self.task.subtask_set.before(last_sub_task)
        self.assertEqual(previous_sub_task, self.sub_tasks[1])

    def test_returns_none_if_after_on_last(self):
        last_sub_task = self.sub_tasks[2]
        next_sub_task = self.task.subtask_set.after(last_sub_task)
        self.assertIsNone(next_sub_task)

    def test_returns_none_if_previous_on_first(self):
        first_sub_task = self.sub_tasks[0]
        previous_sub_task = self.task.subtask_set.before(first_sub_task)
        self.assertIsNone(previous_sub_task)
