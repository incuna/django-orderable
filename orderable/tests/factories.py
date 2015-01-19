import factory

from . import models


class TaskFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Task


class SubTaskFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.SubTask

    task = factory.SubFactory(TaskFactory)
