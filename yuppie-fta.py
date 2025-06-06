import json
import requests
import os
from datetime import datetime
from typing import Dict, List

def format_url(url):
    if not url:
        return ""
    cdn_base = "https://d229kpbsb5jevy.cloudfront.net/yuppfast/content/"
    if url.startswith('http'):
        return url
    path = url.replace(',', '/')
    return cdn_base + path

def format_slug(slug):
    # Just return the first part of the slug
    return slug.split('/')[0]

def get_headers() -> Dict:
    return {
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "box-id": "7c03c72952b44aa4",
        "sec-ch-ua-mobile": "?0",
        "session-id": "YT-f86ef4ba-57ab-4c06-8552-245abc2c6541",
        "tenant-code": "yuppfast",
        "origin": "https://www.yupptv.com",
        "referer": "https://www.yupptv.com/",
        "accept-language": "en-US,en;q=0.9"
    }

def fetch_channels(genre: str) -> List:
    base_url = "https://yuppfast-api.revlet.net/service/api/v1/tvguide/channels"
    params = f"filter=genreCode:{genre};langCode:ENG,HIN,MAR,BEN,TEL,KAN,GUA,PUN,BHO,URD,ASS,TAM,MAL,ORI,NEP"
    url = f"{base_url}?{params}"
    
    response = requests.get(url, headers=get_headers())
    return response.json()["response"]["data"]

def convert_json_format(output_file):
    genres = ["news", "entertainment", "music", "kids", 
              "spiritual", "movies", "lifestyle", "sports", 
              "educational", "others"]
    
    new_format = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feeds": []
    }
    
    for index, genre in enumerate(genres, 1):
        category = {
            "category_id": index,
            "category_name": genre.title(),
            "category_slug": genre,
            "category_description": f"{genre.title()} Category",
            "category_priority": index,
            "channels": []
        }
        
        channels_data = fetch_channels(genre)
        for channel in channels_data:
            slug = channel["target"].get("path", channel["target"].get("slug", ""))
            new_channel = {
                "channel_id": channel["id"],
                "channel_number": channel["target"]["pageAttributes"]["remoteChannelId"],
                "channel_country": "IN",
                "channel_category": genre.title(),
                "channel_name": channel["display"]["title"],
                "channel_slug": format_slug(slug),
                "channel_logo": format_url(channel["display"]["imageUrl"]),
                "channel_poster": format_url(channel["display"]["loadingImageUrl"])
            }
            category["channels"].append(new_channel)
        
        new_format["feeds"].append(category)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_format, f, indent=2)

def generate_playlist(json_file, playlist_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(playlist_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        f.write('# Only Free-To-Air Streams\n')
        f.write('# Scrapped by @sunilprregmi\n')
        f.write(f'# Scrapped on {now_str}\n')
        f.write('# Relay server is for playback\n\n')
        
        # Process each channel in the feeds
        for category in data['feeds']:
            category_name = category['category_name']
            for channel in category['channels']:
                # Get channel details
                channel_name = channel['channel_name']
                channel_id = channel['channel_id']
                channel_number = channel['channel_number']
                channel_logo = channel['channel_logo']
                channel_slug = channel['channel_slug']
                
                # Create channel URL
                channel_url = f'https://in1.sunilprasad.com.np/yuppLive/{channel_slug}/master.m3u8'
                
                # Write channel info
                f.write(f'#EXTINF:-1 tvg-id="{channel_id}" tvg-chno="{channel_number}" tvg-name="{channel_slug}" tvg-logo="{channel_logo}" group-title="{category_name}", {channel_name}\n')
                f.write(f'#KODIPROP:inputstream=inputstream.adaptive\n')
                f.write(f'#KODIPROP:inputstream.adaptive.manifest_type=hls\n')
                f.write(f'#EXTVLCOPT:http-user-agent=YuppTV/7.18.1 (Linux;Android 16) ExoPlayerLib/2.19.1\n')
                f.write(f'{channel_url}\n\n')

if __name__ == "__main__":
    output_file = 'yuppie-fta.json'
    playlist_file = 'yuppie-fta.m3u8'
    for f in [output_file, playlist_file]:
        if os.path.exists(f):
            os.remove(f)
    convert_json_format(output_file)
    generate_playlist(output_file, playlist_file)
    print("JSON and Playlist have been generated successfully.")
