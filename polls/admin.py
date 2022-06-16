from django.contrib import admin
from .models import Person, Chore, Homework


# Register your models here.


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in Person._meta.get_fields() if f.one_to_many is not True
    ]


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in Chore._meta.get_fields() if f.one_to_many is not True
    ]

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = [
        "id", "status", "details", "owner_id"
    ]
