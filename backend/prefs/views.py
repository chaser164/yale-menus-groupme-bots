from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from .models import Pref
from .serializers import PrefSerializer
import requests
from django.http import JsonResponse
import os
from dotenv import load_dotenv
# from pprint import pprint

# get API token
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

def groupme_url(endpoint):
    return f'https://api.groupme.com/v3/{endpoint}?token={API_TOKEN}'

class All_prefs(APIView):

    def get(self, request):
        groupchat_urls = PrefSerializer(Pref.objects.all(), many=True).data
        return Response(groupchat_urls)
    
    def post(self, request):
        if 'pref_string' in request.data and request.data['pref_string']:
            pref_string = request.data['pref_string'].lower()

            try:
                # Try to get the existing Pref object
                existing_pref = Pref.objects.get(pref_string=pref_string)
                return Response(PrefSerializer(existing_pref).data, status=HTTP_200_OK)
            except Pref.DoesNotExist:
                # Pref object does not exist, so create a new one
                # Create groupchat
                response = requests.post(groupme_url('groups'), json={"name": f"{pref_string.title()} Finder", "share": True})
                if response.status_code == 201:
                    data = response.json()['response']
                    groupchat_id = data.get('id')
                    share_url = data.get('share_url') 
                else:
                    return JsonResponse({'error': 'Failed to create groupchat'}, status=response.status_code)
                # Create bot
                response = requests.post(groupme_url('bots'), json={"bot":{"name": f"{pref_string.upper()} SLEUTH", "group_id": groupchat_id, "active":True}})
                if response.status_code == 201:
                    data = response.json()['response']['bot']
                    bot_id = data.get('bot_id')
                else:
                    # Undo group creation
                    requests.post(groupme_url(f'groups/{groupchat_id}/destroy'))
                    return JsonResponse({'error': 'Failed to create bot'}, status=response.status_code)
                new_pref = Pref(
                    pref_string=pref_string,
                    bot_id=bot_id,
                    groupchat_url=share_url,
                    groupchat_id=groupchat_id
                )
                new_pref.save()
                return Response(PrefSerializer(new_pref).data, status=HTTP_201_CREATED)
        else:
            return JsonResponse({"error": "invalid request body"}, status=HTTP_400_BAD_REQUEST)
        