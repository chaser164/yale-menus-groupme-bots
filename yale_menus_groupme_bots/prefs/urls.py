#prefs.urls
from django.urls import path
from .views import All_prefs, A_pref

urlpatterns = [
    path("", All_prefs.as_view(), name="my prefs"),
    path("<int:bot_id>/", A_pref.as_view(), name="a pref")
]