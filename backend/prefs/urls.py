#prefs.urls
from django.urls import path
from .views import All_prefs

urlpatterns = [
    path("", All_prefs.as_view(), name="all food preferences"),
]