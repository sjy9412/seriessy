import requests, json

series = []
movies = []
ids = [10]
ids = [84, 119, 151, 230, 263, 264, 295, 328, 399, 420, 432, 528, 556, 645, 656]
ids = [748, 1241, 1565, 1570, 1582, 1709, 1733, 2150, 131635, 295130, 34055, 9888, 121938, 435259, 2344, 31562, 87359, 391860, 313086, 131780, 228446, 10194, 123800, 473847, ]
for num in ids:
    print(num)
    url = f'https://api.themoviedb.org/3/collection/{num}?api_key=196c02579911763f3a86f8b9f729739b&language=ko-kr'
    response = requests.get(url).json()
    series.append({
        "pk": response['id'],
        "model": "series.series",
        "fields": {
            "name": response['name'].replace(' 시리즈', ''),
            "genre": [],
            "overview": response.get('overview'),
            "poster_path": response.get('poster_path'),
            "backdrop_path": response.get('backdrop_path')
        }
    })
    for movie in response['parts']:
        title = movie.get('title')
        params =  {
        'part':'snippet',
        'type': 'video',
        'q': f'{title} 예고편',
        }
        response2 = requests.get('https://www.googleapis.com/youtube/v3/search?key=AIzaSyATxY7wWNHfE0eIYjg4P7_JuczVF7ounqk', params=params).json()
        movies.append({
            "pk": movie['id'],
            "model": "series.movie",
            "fields": {
                "title": movie.get('title'),
                "release_date": movie.get('release_date', 9999-12-31),
                "vote_average": movie.get('vote_average'),
                "overview": movie.get('overview'),
                "poster_path": movie.get('poster_path', response.get('poster_path')),
                "backdrop_path": movie.get('backdrop_path'),
                "video_url": "",
                "series": response['id']
            }
        })
        print(response2)
        if response2.get('items', 0):
            print(response2['items'])
            movies[-1]['fields']['video_url'] = response2['items'][0]['id']['videoId'][0],
        for genre_id in movie['genre_ids']:
            if genre_id not in series[-1]['fields']['genre']:
                series[-1]['fields']['genre'].append(genre_id)

with open('series.json', 'w', encoding='utf-8') as f:
    json.dump(series, f, ensure_ascii=False, indent="\t")

with open('movie.json', 'w', encoding='utf-8') as f:
    json.dump(movies, f, ensure_ascii=False, indent="\t")
