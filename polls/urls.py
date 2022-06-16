from django.urls import path
from . import views

urlpatterns = [
    path("people/", views.PersonView.as_view()),
    path("people/<id>", views.PersonView.as_view()),
    path("people/<id>/tasks/", views.person_tasks),
    path("tasks/<id>", views.TaskView.as_view()),
    path("tasks/<id>/status", views.task_status),
    path("tasks/<id>/owner", views.task_owner),

]