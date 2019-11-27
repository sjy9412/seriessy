import requests
import json


url = f'https://api.themoviedb.org/3/genre/movie/list?api_key=196c02579911763f3a86f8b9f729739b&language=ko-kr'
response = requests.get(url).json()
genres = []
for genre in response['genres']:
    genres.append({"pk": genre['id'],
    "model": "series.genre",
    "fields": {
        "name": genre['name']
    }
    })
with open('genres.json', 'w', encoding="utf-8") as f:
    json.dump(genres, f, ensure_ascii=False, indent="\t")

params =  {
        'part':'snippet',
        'type': 'video',
        'q': '스타워즈 에피소드 4: 새로운 희망 예고편',
    }
response = requests.get('https://www.googleapis.com/youtube/v3/search?key=AIzaSyBclnDZz8Zaqq4Fh1rdxoOVNoLzK6OZhu8', params=params).json()
print('https://www.youtube.com/embed/' + response['items'][0]['id']['videoId'])
