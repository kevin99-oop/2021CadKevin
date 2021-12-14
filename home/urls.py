from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='home'),
    path('diabetes/',diabetes,name='diabetes'),
    path('covid/',covid,name='covid'),
    path('alcohol',alcohol,name='alcohol'),
    path('diabetesdb/',diabetesdb,name='diabetesdb'),
    path('coviddb/',coviddb,name='coviddb'),
    path('alcoholdb/',alcoholdb,name='alcoholdb'),
    
    
]
