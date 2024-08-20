import json
import os
from yt_dlp import YoutubeDL
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/api/youtube-dlp', methods=['GET'])
def download_youtube():
    link = request.args.get('links')
    if not link:
        return json.dumps({"error": "Link not provided"}), 400
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
        return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run()