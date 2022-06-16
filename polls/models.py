from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.translation import gettext_lazy as _
from datetime import date



import uuid


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    favoriteProgrammingLanguage = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Task(models.Model):

    class TaskStatus(models.TextChoices):
        ACTIVE = "Active", _("Active")
        DONE = "Done", _("Done")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=6, choices=TaskStatus.choices)
    type = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def get_status_type(self) -> str:
        return self.TaskStatus(self.status).label


class Homework(Task):
    course = models.CharField(max_length=100)
    due_date = models.DateField(default=date.today())
    details = models.CharField(max_length=200)
    owner_id = models.ForeignKey(to=Person, related_name="homeworks", on_delete=SET_NULL, null=True, blank=True)


class Chore(Task):

    class ChoreSize(models.TextChoices):

        SMALL = "Small", _("Small")
        MEDIUM = "Medium", _("Medium")
        LARGE = "Large", _("Large")

    description = models.CharField(max_length=200)
    size = models.CharField(max_length=6, choices=ChoreSize.choices)
    owner_id = models.ForeignKey(to=Person, related_name="chores", on_delete=SET_NULL, null=True, blank=True)

    def get_size_type(self) -> str:
        return self.ChoreSize(self.size).label
















