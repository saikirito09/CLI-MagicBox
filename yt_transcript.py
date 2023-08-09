#!/usr/bin/env python3

import sys
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

def extract_video_id(youtube_url):
    # This regex will extract the video ID from a YouTube URL
    regex = r"(?<=v=)[a-zA-Z0-9_-]+"
    match = re.search(regex, youtube_url)
    return match.group(0) if match else None

def get_video_title(youtube_url):
    try:
        yt = YouTube(youtube_url)
        return yt.title
    except Exception as e:
        print(f"An error occurred while fetching the title: {e}")
        return None

def download_transcript(youtube_url, show_timestamps=True):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        print("Failed to extract video ID from the provided URL.")
        return

    title = get_video_title(youtube_url)
    if not title:
        title = video_id

    # Sanitize the title for file naming
    title_sanitized = re.sub(r'[\\/:"*?<>|]+', '', title)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Construct file name
        file_name = f"{title_sanitized}_transcript.txt"
        file_path = os.path.join(os.getcwd(), file_name)

        # Save to file
        with open(file_path, 'w') as f:
            for entry in transcript:
                if show_timestamps:
                    f.write(f"{entry['start']} - {entry['start'] + entry['duration']}: {entry['text']}\n")
                else:
                    f.write(f"{entry['text']}\n")
        print(f"Transcript saved to {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: yt_transcript.py <YouTube Video URL> [--no-timestamps]")
        sys.exit(1)

    youtube_url = sys.argv[1]
    show_timestamps = True

    if '--no-timestamps' in sys.argv:
        show_timestamps = False

    download_transcript(youtube_url, show_timestamps)
