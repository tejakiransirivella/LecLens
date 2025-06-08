from collections import defaultdict
import re
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def extract_video_id(youtube_url: str) -> str:
    """
    Extract the video ID from a YouTube URL.
    """
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL provided.")


def transform_transcript(transcript_list: list) -> tuple:
    """
    Transform the transcript list to a dictionary where:
    - Keys are unique sentences.
    - Values are sets of start times when the sentence appears.
    """
    transcript_dict = defaultdict(set)
    full_transcript = []

    for segment in transcript_list:
        text = segment["text"].replace("\n", " ")
        transcript_dict[segment["text"]].add(segment["start"])
        full_transcript.append(text)
    full_transcript_str = " ".join(full_transcript)
    formatted_transcript_timestamps = {text: sorted(times) for text, times in transcript_dict.items()}

    return formatted_transcript_timestamps, full_transcript_str  # Convert sets to sorted lists for consistency


def parse_vidcap_content(content):
    matches = re.findall(r'\[at ([\d.]+) seconds\] (.*?)\n', content)
    
    transcript = []
    
    for i in range(len(matches)):
        start = float(matches[i][0])
        text = matches[i][1].strip()

        transcript.append({
            "text": text,
            "start": start,
        })
    
    return transcript

def get_transcript(youtube_url: str) -> tuple:
    """
    Retrieve and transform the transcript for the given YouTube URL.
    """
    transcript_list = []

    video_id = extract_video_id(youtube_url)
    
    load_dotenv()
    
    vidcap_api_key = os.getenv("VIDCAP_API_KEY")
    url = "https://vidcap.xyz/api/v1/youtube/caption"

    query_params = {
        "url": "https://www.youtube.com/watch?v=" + video_id,
        "locale": "en",
        "ext": "json3"
    }

    headers = {
        "x-api-key": vidcap_api_key
    }

    response = requests.get(url, params=query_params, headers=headers)
    
    if response.status_code == 200:
        try:
            body = response.json()
            content = body["data"]["content"]
            transcript_list = parse_vidcap_content(content)
        except Exception as e:
           print(f"Error parsing response: {e}")

    if len(transcript_list) == 0:
        return None,[]
    transcript_with_timestamps, full_transcript = transform_transcript(transcript_list)
    return transcript_with_timestamps, full_transcript
