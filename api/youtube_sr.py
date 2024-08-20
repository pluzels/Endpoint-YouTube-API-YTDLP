import json
from yt_dlp import YoutubeDL
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/youtube-sr', methods=['GET'])
def search_youtube():
    query = request.args.get('query')
    if not query:
        return json.dumps({"error": "Query not provided"}), 400
    
    ydl_opts = {
        'default_search': 'ytsearch5',
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(query, download=False)

    videos = []
    for entry in results['entries']:
        video = {
            'id': entry['id'],
            'title': entry['title'],
            'url': f"https://www.youtube.com/watch?v={entry['id']}",
            'duration': entry['duration'],
            'thumbnail': entry['thumbnail'],
        }
        videos.append(video)

    return json.dumps(videos), 200

if __name__ == '__main__':
    app.run()