from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import StudentSurveyModel
from .serializers import StudentSurveySerializer

# Create your views here.
@api_view(['POST'])
def save_survey_data(request):
    serializer = StudentSurveySerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Survey data saved successfully!"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_survey_data(request):
    survey_data = StudentSurveyModel.objects.all()
    serializer = StudentSurveySerializer(survey_data, many=True)
    return Response(serializer.data)

