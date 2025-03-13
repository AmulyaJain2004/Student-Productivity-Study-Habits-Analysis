from django.urls import path
from .views import save_survey_data, get_survey_data, export_survey_data

urlpatterns = [
    path('save/', save_survey_data),  # POST request to save data
    path('data/', get_survey_data),  # GET request to retrieve data
    path('export/', export_survey_data),  # GET request to export data
]
