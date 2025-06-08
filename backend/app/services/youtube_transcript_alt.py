from collections import defaultdict
import re
import subprocess
import os
from typing import List
from pathlib import Path

home_dir = Path(__file__).resolve(strict=True).parents[2]

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


def parse_timestamp(timestamp: str) -> float:
    """
    Convert a timestamp string in the format 'HH:MM:SS.mmm' to seconds.
    """
    parts = timestamp.split(':')
    sm = parts[2].split('.')
    parts[2] = sm[0]
    parts.append(sm[1])
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    milliseconds = float(parts[3])
    return hours * 3600 + minutes * 60 + seconds + (milliseconds / 1000)

def parse_vtt_file(file_path:str) -> List[dict]:
    timestamp_expr = r"^(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3}) align:start position:0%$"
    res = []
    count = 0
    isText = False
    record = ["",0.0]

    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:

            if isText:
                record[0] = line.strip()
                res.append({
                    "text": record[0],
                    "start": record[1]
                })
                isText = False
                continue

            if re.match(timestamp_expr, line):
                count += 1

                if count%2 == 0:
                    isText = True
            
                if count%2 == 1:
                    timestamp = line[0:line.index(" --> ")]
                    record[1]= parse_timestamp(timestamp)
    return res

def download_subtitles(video_id:str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    command = [
        "yt-dlp",
        "--cookies", f"{home_dir}/data/cookies.txt",  # path to cookies file"
        "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "--add-header", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "--add-header", "Accept-Language: en-US,en;q=0.9",
        "--add-header", "Referer: https://www.youtube.com/",
        "--add-header", "Cache-Control: no-cache",
        "--add-header", "Pragma: no-cache",
        "--write-auto-sub",        # auto-generated subtitles
        "--sub-lang", "en",        # language code
        "--skip-download",         # don't download the video
        "--quiet",                 # suppress output
        "--no-warnings",
        "--output", "%(id)s.%(ext)s",
        url
    ]

    subprocess.run(command,check = True)
    subtitle_file = f"{video_id}.en.vtt"
    return subtitle_file

def get_transcript(youtube_url: str) -> tuple:
    """
    Retrieve and transform the transcript for the given YouTube URL.
    """
    video_id = extract_video_id(youtube_url)
    # transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    subtitle_file = download_subtitles(video_id)
    transcript_list = parse_vtt_file(subtitle_file)
    transcript_with_timestamps, full_transcript = transform_transcript(transcript_list)
    os.remove(subtitle_file)
    return transcript_with_timestamps, full_transcript
