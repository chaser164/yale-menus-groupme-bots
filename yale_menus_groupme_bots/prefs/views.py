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

# load dotenv
load_dotenv()

GROUPME_URL = f'https://api.groupme.com/v3/groups?token={os.getenv('API_TOKEN')}'

class All_prefs(APIView):

    def get(self, request):
        groupchat_urls = PrefSerializer(Pref.objects.all(), many=True).data
        return Response(groupchat_urls)
    
    def post(self, request):
        if 'pref_string' in request.data and request.data['pref_string']:
            pref_string = request.data['pref_string']

            try:
                # Try to get the existing Pref object
                existing_pref = Pref.objects.get(pref_string=pref_string)
                return Response(PrefSerializer(existing_pref).data, status=HTTP_200_OK)
            except Pref.DoesNotExist:
                # Pref object does not exist, so create a new one

                # Build groupchat
                # Make the GET request to the third-party API
                response = requests.post(GROUPME_URL, json={"name": f"{pref_string.title()} Finder", "share": True})
                if response.status_code == 201:
                    data = response.json()['response']
                    groupchat_id = data.get('id')
                    share_url = data.get('share_url')
                    print(share_url)
                    # Check if the request was successful
                    
                else:
                    return JsonResponse({'error': 'Failed to create groupchat'}, status=response.status_code)
                # Add bot
                



                new_pref = Pref(
                    pref_string=pref_string,
                    bot_id='123',
                    groupchat_url=share_url,
                    groupchat_id=groupchat_id
                )
                new_pref.save()
                return Response(PrefSerializer(new_pref).data, status=HTTP_201_CREATED)
        else:
            return JsonResponse({"error": "invalid request body"}, status=HTTP_400_BAD_REQUEST)
        
class A_pref(APIView):

    def delete(self, request, bot_id):
        pref = get_object_or_404(Pref, bot_id = bot_id)
        pref.delete()
        return JsonResponse({"message": "deleted successfully"}, status=HTTP_204_NO_CONTENT)