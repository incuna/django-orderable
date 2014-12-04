import django
from django.test import TestCase

from . import factories
from .models import Task


DJANGO_16 = '.'.join(map(str, django.VERSION)) >= '1.6'


class TestOrderingOnSave(TestCase):
    def test_normal_save(self):
        """Normal saves should avoid giggery pokery."""
        task = Task.objects.create()

        with self.assertNumQueries(1 if DJANGO_16 else 2):
            # https://docs.djangoproject.com/en/dev/releases/1.6/#model-save-algorithm-changed
            # Queries on django < 1.6
            #     SELECT
            #     UPDATE
            # Queries on django >= 1.6
            #     UPDATE
            task.save()

    def test_unspecified_order(self):
        """New inserts should default to the end of the list.

        Index:   1    2
        Before: old
        After:  old  new
        """
        old = factories.TaskFactory.create(sort_order=1)

        with self.assertNumQueries(2):
            # Queries
            #     Find last position in list
            #     Save to last position in list
            new = factories.TaskFactory.create()

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
        old_1 = factories.TaskFactory.create(sort_order=1)
        old_2 = factories.TaskFactory.create(sort_order=2)
        old_3 = factories.TaskFactory.create(sort_order=3)

        # Insert between old_1 and old_2
        with self.assertNumQueries(2):
            # Queries:
            #     Bump old_2 to position 3
            #     Save new in position 2
            new = factories.TaskFactory.create(sort_order=old_2.sort_order)

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
        item1 = factories.TaskFactory.create(sort_order=1)
        item2 = factories.TaskFactory.create(sort_order=2)
        item3 = factories.TaskFactory.create(sort_order=3)
        item4 = factories.TaskFactory.create(sort_order=4)
        item5 = factories.TaskFactory.create(sort_order=5)

        # Move item2 to position 4
        with self.assertNumQueries(4 if DJANGO_16 else 6):
            # Queries:
            #     Find end of list
            #     SELECT item2 (on django < 1.6)
            #     Move item2 to end of list
            #     Shuffle item3 and item4 back by one
            #     SELECT item2 (on django < 1.6)
            #     Save item2 to new desired position
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
        item1 = factories.TaskFactory.create(sort_order=1)
        item2 = factories.TaskFactory.create(sort_order=2)
        item3 = factories.TaskFactory.create(sort_order=3)
        item4 = factories.TaskFactory.create(sort_order=4)
        item5 = factories.TaskFactory.create(sort_order=5)

        # Move item4 to position 2
        with self.assertNumQueries(4 if DJANGO_16 else 6):
            # Queries:
            #     Find end of list
            #     SELECT item4 (on django < 1.6)
            #     Move item4 to end of list
            #     Bump item2 and item3 on by one
            #     SELECT item4 (on django < 1.6)
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
