from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import StudentSurveyModel
from .serializers import StudentSurveySerializer
from django.http import HttpResponse
import csv



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

def export_survey_data(request):
    response =  HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="survey_data.csv"'
    writer = csv.writer(response)
    writer.writerow([field.name for field in StudentSurveyModel._meta.fields]) # Column headers
    for student in StudentSurveyModel.objects.all():
        writer.writerow([getattr(student, field.name) for field in StudentSurveyModel._meta.fields])
    return response # returning an HTTP response containing a CSV file with survey data which will download automatically