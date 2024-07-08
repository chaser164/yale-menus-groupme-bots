from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from .models import Pref
import requests
from dotenv import load_dotenv
import os
from pprint import pprint

# get API token
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

class PrefAdmin(admin.ModelAdmin):
    list_display = ['pref_string']
    search_fields = ['pref_string']

    def has_change_permission(self, request, obj=None):
        return False  # Prohibit editing
    
    def has_add_permission(self, request, obj=None):
        return False  # Prohibit editing
    
    def delete_model(self, request, obj):
        # Custom deletion logic
        groupchat_id = obj.groupchat_id
        # Remove associated groupchat (also causes cascade removal of bot)
        response = requests.post(f'https://api.groupme.com/v3/groups/{groupchat_id}/destroy?token={API_TOKEN}')
        # 404 allowed because this handled the deleted-elsewhere case
        if response.status_code == 200 or response.status_code == 404:
            obj.delete()
        else:
            raise ValidationError("Error deleting group chat")
    

# Register your models here.
admin.site.register(Pref, PrefAdmin)
# No User or Group models required
admin.site.unregister(User)
admin.site.unregister(Group)