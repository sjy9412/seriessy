import requests
import json


url = f'https://api.themoviedb.org/3/genre/movie/list?api_key=196c02579911763f3a86f8b9f729739b&language=ko-kr'
response = requests.get(url).json()
genres = []
for genre in response['genres']:
    genres.append({"pk": genre['id'],
    "model": "movies.genre",
    "fields": {
        "name": genre['name']
    }
    })
with open('genres.json', 'w', encoding="utf-8") as f:
    json.dump(genres, f, ensure_ascii=False, indent="\t")
