from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.

def search_meaning(request):
    search_result = {}
    if 'word' in request.GET:
        word = request.GET.get('word')
        endpoint = 'https://od-api.oxforddictionaries.com/api/v2/entries/{source_lang}/{word_id}'
        url = endpoint.format(source_lang='en', word_id=word)
        headers = {'app_id': settings.OXFORD_APP_ID, 'app_key': settings.OXFORD_APP_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200: 
            search_result = response.json()
            search_result['success'] = True
        else:
            search_result['success'] = False
            if response.status_code == 404: 
                search_result['message'] = 'No entry found for "%s"' % word
            else:
                search_result['message'] = 'The Oxford API is not available at the moment. Please try again later.'
        return render(request, 'index.html', {'search_result': search_result})
    else:
        return render(request, 'index.html')
