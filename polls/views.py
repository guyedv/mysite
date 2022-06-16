
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Person
from .models import Task
from .models import Chore
from .models import Homework
from .serializers import PersonSerializer, ChoreSerializer, HomeworkSerializer
from rest_framework.decorators import api_view




from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


class PersonView(APIView):


    def post(self, request: Request) -> Response:
        try:
            name: str = request.data["name"]
            email: str = request.data["email"]
            favorite_programming_language: str = request.data["favoriteProgrammingLanguage"]
            person: Person = Person.objects.create(name=name, email=email, favoriteProgrammingLanguage=favorite_programming_language)
            headers_dict: dict = {'Location': f"http://127.0.0.1:8000/api/people/{person.id}", 'x-Created-Id': f"{person.id}"}
            response: Response = Response(f"{name} was successfully added.", status=status.HTTP_201_CREATED,headers=headers_dict)
        except KeyError as e:
            response = Response(f"bad request, missing parameters: {str(e)}", status=status.HTTP_400_BAD_REQUEST)
        return response

    def patch(self, request: Request, id: str) -> Response:
        try:
            name: str = request.data.get("name")
            email: str = request.data.get("email")
            favorite_programming_language: str = request.data.get("favoriteProgrammingLanguage")
            person: Person = Person.objects.get(pk=id)
            if name:
                person.name = name
            if email:
                person.email = email
            if favorite_programming_language:
                person.favoriteProgrammingLanguage = favorite_programming_language
            person.save()
            response: Response = Response(f"person with id : {id} was successfully updated.", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            response = Response(f"person with id {id} was not found.", status=status.HTTP_404_NOT_FOUND)
        return response

    def delete(self, request: Request, id: str) -> Response:
        try:
            person: Person = Person.objects.get(pk=id)
            person_name: str = person.name
            person.delete()
            response: Response = Response(f"{person_name} was removed from the system.", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            response = Response(f"person with id {id} was not found.", status=status.HTTP_404_NOT_FOUND)
        return response


    def get(self, request: Request, *args, **kwargs) -> Response:

        if "id" in kwargs:
            id: str = kwargs.get("id")
            try:
                person: Person = Person.objects.get(pk=id)
                person_data: dict[str, str] = PersonSerializer(person).data
                filtered_chores = Chore.objects.filter(owner_id=id,status="Active")
                filtered_homeworks = Homework.objects.filter(owner_id=id, status="Active")
                person_data["activeTaskCount"] = filtered_chores.count()+filtered_homeworks.count()
                response: Response = Response(person_data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                response = Response(f"a person with the id {id} does not exist.", status=status.HTTP_404_NOT_FOUND)
            return response

        people = Person.objects.all()
        people_details: list[dict[str, str]] = PersonSerializer(people, many=True).data
        for person_details in people_details:
            filtered_chores = Chore.objects.filter(owner_id=person_details["id"], status="Active")
            filtered_homeworks = Homework.objects.filter(owner_id=person_details["id"], status="Active")
            person_details["activeTaskCount"] = filtered_chores.count() + filtered_homeworks.count()

        response = Response(people_details, status=status.HTTP_200_OK)
        return response




class TaskView(APIView):

    @staticmethod
    def _get_sub_task(id: str) -> tuple[Chore | Homework, bool]:
        task: Task = None
        query_a = Chore.objects.filter(pk=id)
        query_b = Homework.objects.filter(pk=id)
        if query_a.exists():
            task = query_a.first()
            return task, True
        elif query_b.exists():
            task = query_b.first()
            return task, False
        else:
            raise ObjectDoesNotExist

    def get(self, request: Request, id: str) -> Response:
        try:
            task,type = self._get_sub_task(id)
            if type:
                task_data: dict[str, str] = ChoreSerializer(task).data
                task_data["type"] = "Chore"
            else:
                task_data: dict[str, str] = HomeworkSerializer(task).data
                task_data["type"] = "Homework"
            response: Response = Response(task_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            response = Response(f"a task with the id {id} does not exist.", status=status.HTTP_404_NOT_FOUND)
        return response

    def delete(self, request: Request, id: str) -> Response:
        try:
            task, _ = self._get_sub_task(id)
            task.delete()
            response: Response = Response(f"task with id {id} was removed from the system.", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            response = Response(f"task with id {id} was not found.", status=status.HTTP_404_NOT_FOUND)
        return response

@api_view(['GET', 'PUT'])
def task_status(request: Request, id: str):
    try:
        task,type = TaskView._get_sub_task(id)

        if request.method == "GET":
            stat: str = task.status
            response: Response = Response(f"the status of task {id} is {stat}.", status=status.HTTP_200_OK)
        else:
            stat: str = request.data.capitalize()
            if stat == 'Active' or stat == 'Done':
                task.status = stat
                task.save()
                response: Response = Response(f"the status of task {id} is updated to {task.status}.", status=status.HTTP_204_NO_CONTENT)
            else:
                response = Response(f"bad request, data makes no sense", status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        response = Response(f"task with id {id} was not found.", status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        response = Response(f"bad request, missing parameters: {str(e)}", status=status.HTTP_400_BAD_REQUEST)
    return response

@api_view(['GET', 'PUT'])
def task_owner(request: Request, id: str):
    try:
        task, type = TaskView._get_sub_task(id)
        print(f"type of task is : {type}")
        if request.method == "GET":
            owner: str = task.owner_id.name
            response: Response = Response(f"the owner of task {id} is {owner}.", status=status.HTTP_200_OK)
        else: # "PUT"
            owner: str = task.owner_id.id
            person_add: Person = Person.objects.get(pk=request.data)
            print(f"person to add is: {person_add}")
            person_remove: Person = Person.objects.get(pk=owner)
            print(f"person to remove is: {person_remove}")
            if type:  # "Chore"
                person_add.chores.add(task)
                print(f"chore {task.id} is added to person: {person_add}")
                print(f"chore {task.id} is removed from person: {person_remove}")
            else:  # "Homework"
                person_add.homeworks.add(task)
                print(f"hw {task.id} is added to person: {person_add}")
                print(f"hw {task.id} is removed from person: {person_remove}")
            response: Response = Response(f"the task's owner was changed from owner {person_remove} to owner {person_add}.", status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        response = Response(f"task with id {id} was not found.", status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        response = Response(f"bad request, missing parameters: {str(e)}", status=status.HTTP_400_BAD_REQUEST)
    return response

@api_view(['GET', 'POST'])
def person_tasks(request: Request, id: str):
    try:
        person: Person = Person.objects.get(pk=id)
        if request.method == "GET":
            stat: str = request.data.get("active")
            if stat == "done":
                hw_query = person.homeworks.filter(status="Done")
                chore_query = person.chores.filter(status="Done")
            else:
                hw_query = person.homeworks.all()
                chore_query = person.chores.all()
            person_hw: list[dict[str, str]] = HomeworkSerializer(hw_query, many=True).data
            person_chores: list[dict[str, str]] = ChoreSerializer(chore_query, many=True).data
            person_hw.extend(person_chores)
            person_tasks: list[dict[str, str]] = person_hw
            response: Response = Response(person_tasks, status=status.HTTP_200_OK)
        else:
            type: str = request.data["type"]
            if type == "Chore":
                stat: str = request.data["status"]
                description: str = request.data["description"]
                size: str = request.data["size"]
                task = Chore(type=type, status=stat, description=description, size=size)
                headers_dict: dict = {'Location': f"http://127.0.0.1:8000/api/tasks/{task.id}", 'x-Created-Id': f"{task.id}"}
                task.full_clean()
                task.save()
                person.chores.add(task)
                response: Response = Response(f"task was successfully assigned to person {person.name}.",
                                              status=status.HTTP_201_CREATED, headers=headers_dict)
            elif type == "Homework":
                course: str = request.data["course"]
                stat: str = request.data["status"]
                details: str = request.data["details"]
                due_date: str = request.data["due_date"]
                task = Homework(course=course, type=type, status=stat, details=details, due_date=due_date)
                headers_dict: dict = {'Location': f"http://127.0.0.1:8000/api/tasks/{task.id}", 'x-Created-Id': f"{task.id}"}
                task.full_clean()
                task.save()
                person.homeworks.add(task)
                response: Response = Response(f"task was successfully assigned to person {person.name}.",
                                              status=status.HTTP_201_CREATED, headers=headers_dict)
            else:
                response: Response = Response(f"error: no such type as '{type}'.", status=status.HTTP_400_BAD_REQUEST)


    except ObjectDoesNotExist:
        response = Response(f"person with id {id} was not found.", status=status.HTTP_404_NOT_FOUND)
    except KeyError as e:
        response = Response(f"bad request, missing parameters: {str(e)}", status=status.HTTP_400_BAD_REQUEST)
    return response




