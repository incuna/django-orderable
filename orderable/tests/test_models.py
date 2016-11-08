from hypothesis import example, given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import integers, lists

from .models import SubTask, Task


class TestOrderingOnSave(TestCase):
    def test_normal_save(self):
        """Normal saves should avoid giggery pokery."""
        task = Task.objects.create()

        with self.assertNumQueries(3):
            # Queries:
            #     SAVEPOINT
            #     UPDATE
            #     COMMIT
            task.save()

    def test_unspecified_order(self):
        """New inserts should default to the end of the list.

        Index:   1    2
        Before: old
        After:  old  new
        """
        old = Task.objects.create(sort_order=1)

        with self.assertNumQueries(4):
            # Queries
            #     Savepoint
            #     Find last position in list
            #     Save to last position in list
            #     Commit
            new = Task.objects.create()

        tasks = Task.objects.all()
        # Make sure list is in correct order
        self.assertSequenceEqual(tasks, [old, new])
        # Make sure sort_order is unique
        self.assertEqual(len(tasks), len(set(t.sort_order for t in tasks)))

    def test_insert_on_create(self):
        """New insert should bump rest of list along if sort_order specified.

        Index:    1      2      3
        Before: old_1  old_2  old_3
        After:  old_1   new   old_2  old_3
        """
        old_1 = Task.objects.create(sort_order=1)
        old_2 = Task.objects.create(sort_order=2)
        old_3 = Task.objects.create(sort_order=3)

        # Insert between old_1 and old_2
        with self.assertNumQueries(6):
            # Queries:
            #     Savepoint
            #     Savepoint
            #     Bump old_2 to position 3
            #     Release savepoint
            #     Release savepoint
            #     Save new in position 2
            new = Task.objects.create(sort_order=old_2.sort_order)

        tasks = Task.objects.all()
        # Make sure list is in correct order
        self.assertSequenceEqual(tasks, [old_1, new, old_2, old_3])
        # Make sure sort_order is still unique
        self.assertEqual(len(tasks), len(set(t.sort_order for t in tasks)))

    def test_increase_order(self):
        """Increasing sort_order should move back those in the middle.

        Moving 2 to 4:

        Index:    1      2      3      4      5
        Before: item1  item2  item3  item4  item5
        After:  item1  item3  item4  item2  item5
        """
        item1 = Task.objects.create(sort_order=1)
        item2 = Task.objects.create(sort_order=2)
        item3 = Task.objects.create(sort_order=3)
        item4 = Task.objects.create(sort_order=4)
        item5 = Task.objects.create(sort_order=5)

        # Move item2 to position 4
        with self.assertNumQueries(6):
            # Queries:
            #     Savepoint
            #     Find end of list
            #     Move item2 to end of list
            #     Shuffle item3 and item4 back by one
            #     Save item2 to new desired position
            #     Commit
            item2.sort_order = item4.sort_order
            item2.save()

        tasks = Task.objects.all()
        # Make sure list is in correct order
        expected = [item1, item3, item4, item2, item5]
        self.assertSequenceEqual(tasks, expected)
        # Make sure sort_order is still unique
        self.assertEqual(len(tasks), len(set(t.sort_order for t in tasks)))

    def test_decrease_order(self):
        """Decreasing sort_order should bump those in the middle on.

        Moving 4 to 2:

        Index:    1      2      3      4      5
        Before: item1  item2  item3  item4  item5
        After:  item1  item4  item2  item3  item5
        """
        item1 = Task.objects.create(sort_order=1)
        item2 = Task.objects.create(sort_order=2)
        item3 = Task.objects.create(sort_order=3)
        item4 = Task.objects.create(sort_order=4)
        item5 = Task.objects.create(sort_order=5)

        # Move item4 to position 2
        with self.assertNumQueries(8):
            # Queries:
            #     Savepoint
            #     Find end of list
            #     Move item4 to end of list
            #     Savepoint
            #     Bump item2 and item3 on by one
            #     Release savepoint
            #     Release savepoint
            #     Save item4 to new desired position
            item4.sort_order = item2.sort_order
            item4.save()

        tasks = Task.objects.all()
        # Make sure list is in correct order
        expected = [item1, item4, item2, item3, item5]
        self.assertSequenceEqual(tasks, expected)
        # Make sure sort_order is still unique
        self.assertEqual(len(tasks), len(set(t.sort_order for t in tasks)))

    def test_zero_sort_order(self):
        """Zero should be a valid value for sort_order."""
        zero_task = Task.objects.create(sort_order=0)
        self.assertEqual(zero_task.sort_order, 0)

    def test_reordering(self):
        """Check you can reassign a complete new order.

        This is similar to a formset or the admin reorder view.
        """
        tasks = [
            Task.objects.create(),
            Task.objects.create(),
            Task.objects.create(),
            Task.objects.create(),
        ]
        tasks[0].sort_order = 3
        tasks[0].save()
        tasks[1].sort_order = 4
        tasks[1].save()
        tasks[2].sort_order = 1
        tasks[2].save()
        tasks[3].sort_order = 2
        tasks[3].save()
        self.assertSequenceEqual(Task.objects.all(), [
            tasks[2],
            tasks[3],
            tasks[0],
            tasks[1],
        ])


class TestSubTask(TestCase):

    def test_duplicated_sort_order_on_different_parents(self):
        task = Task.objects.create()
        task_2 = Task.objects.create()
        subtask = SubTask.objects.create(task=task)
        subtask_2 = SubTask.objects.create(task=task_2)
        self.assertEqual(subtask.sort_order, subtask_2.sort_order)

    def test_reordering(self):
        """Check you can reassign a complete new order.

        This is similar to a formset or the admin reorder view. The subtask
        version differs importantly because there is a database level
        uniqueness constraint.
        """
        task = Task.objects.create()
        subtasks = [
            SubTask.objects.create(task=task, sort_order=3),
            SubTask.objects.create(task=task, sort_order=4),
            SubTask.objects.create(task=task, sort_order=1),
            SubTask.objects.create(task=task, sort_order=2),
        ]
        self.assertSequenceEqual(task.subtask_set.all(), [
            subtasks[2],
            subtasks[3],
            subtasks[0],
            subtasks[1],
        ])

    def test_changing_parent(self):
        """Check changing the unique together parent."""
        task = Task.objects.create()
        task_2 = Task.objects.create()
        subtask = SubTask.objects.create(task=task)
        subtask_2 = SubTask.objects.create(task=task_2)
        self.assertEqual(subtask.sort_order, subtask_2.sort_order)
        subtask_2 = SubTask.objects.get(pk=subtask_2.pk)
        subtask_2.task = task
        subtask_2.save()
        self.assertSequenceEqual(task.subtask_set.all(), [subtask, subtask_2])

    def test_next_and_prev(self):
        task = Task.objects.create()
        task_2 = Task.objects.create()
        subtask = SubTask.objects.create(task=task)
        subtask_2 = SubTask.objects.create(task=task)
        subtask_3 = SubTask.objects.create(task=task_2)

        self.assertEqual(subtask.next(), subtask_2)
        self.assertIsNone(subtask_2.next())

        self.assertIsNone(subtask_3.prev())
        self.assertIsNone(subtask_3.next())

    @given(lists(integers(min_value=1), min_size=1, unique=True))
    @example([2, 3, 1])
    @example([2, 3, 4])
    def test_save_subtask_no_errors(self, sort_orders):
        """Ensure Orderable.save does not raise IntegrityError."""
        task = Task.objects.create()

        for order in sort_orders:
            subtask = SubTask.objects.create(task=task, sort_order=order)

        subtask.sort_order = 2
        subtask.save()
