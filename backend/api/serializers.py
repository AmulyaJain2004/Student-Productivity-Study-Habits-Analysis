from rest_framework import serializers
from .models import StudentSurveyModel

class StudentSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSurveyModel
        fields = '__all__'