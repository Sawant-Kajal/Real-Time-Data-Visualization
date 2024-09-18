import csv
import time
from googleapiclient.discovery import build

# Initialize values
fieldnames = ["upload_date", "video_name", "likes", "channel_name"]

# Replace with your own API key
api_key = 'AIzaSyCKkRZ-_aj2yXOEqCc_CAhSU0mduypnmcA'
youtube = build('youtube', 'v3', developerKey=api_key)

# Replace with the channel names of the YouTube channels you want to track
channel_names = ['Carryminati', 'BB Ki Vines']

def get_channel_id(channel_name):
    request = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel'
    )
    response = request.execute()
    
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['id']['channelId']
    else:
        print(f"Error: No data found for channel name {channel_name}")
        return None

def get_all_videos_info(channel_id):
    videos_info = []
    next_page_token = None
    
    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            order='date',
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            for item in response['items']:
                if item['id']['kind'] == 'youtube#video':
                    video_id = item['id']['videoId']
                    video_title = item['snippet']['title']
                    upload_date = item['snippet']['publishedAt']
                    
                    video_request = youtube.videos().list(
                        part='statistics',
                        id=video_id
                    )
                    video_response = video_request.execute()
                    
                    if 'items' in video_response and len(video_response['items']) > 0:
                        like_count = int(video_response['items'][0]['statistics']['likeCount'])
                        videos_info.append((upload_date, video_title, like_count))
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos_info

# Get channel IDs from channel names
channel_ids = [get_channel_id(name) for name in channel_names]

with open('data.csv', 'w', encoding='utf-8', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('data.csv', 'a', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for channel_name, channel_id in zip(channel_names, channel_ids):
            videos_info = get_all_videos_info(channel_id)
            for upload_date, video_title, like_count in videos_info:
                info = {
                    "upload_date": upload_date,
                    "video_name": video_title,
                    "likes": like_count,
                    "channel_name": channel_name
                }
                csv_writer.writerow(info)
                print(upload_date, video_title, like_count, channel_name)
    time.sleep(1200)  # Fetch data every min
