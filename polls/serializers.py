from rest_framework import serializers
from .models import Person,Chore,Homework

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = []

class ChoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chore
        exclude = []

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        exclude = []