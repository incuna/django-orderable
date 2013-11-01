import factory

from . import models


class TaskFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Task
