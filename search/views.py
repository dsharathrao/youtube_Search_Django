from django.shortcuts import render, redirect
from isodate import parse_duration
import requests
from django.conf import settings


# Create your views here.


def index(request):
    global form
    form = ''
    form = request.POST['search']
    print(form)
    print(form)
    
    return render(request, 'index.html')

def result(request):
    video_ids = []
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    videos = []
    search_params = {
        'part' : 'snippet',
        'q' : form,
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 9,
        'type' : 'video'
    }
    
    r = requests.get(search_url, params=search_params)

    results = r.json()['items']

    
    for result in results:
        video_ids.append(result['id']['videoId'])

    
    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet,contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 9
    }

    r = requests.get(video_url, params=video_params)

    results = r.json()['items']

    
    for result in results:
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }

        videos.append(video_data)

    context = {
        'videos' : videos
    }
    
    return render(request, 'result.html', context)
