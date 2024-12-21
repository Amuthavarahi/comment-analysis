from googleapiclient.discovery import build
import pandas as pd
from textblob import TextBlob
import nltk

nltk.download('stopwords')


API_KEY = 'YOUR_YOUTUBE_API_KEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_youtube_comments(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            break

    return comments


def analyze_sentiments(comments):
    sentiments = []
    for comment in comments:
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            sentiments.append('Positive')
        elif polarity < 0:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
    return sentiments


if __name__ == "__main__":
    video_id = input("Enter YouTube video ID: ")  # Example: dQw4w9WgXcQ
    print("Fetching comments...")
    comments = get_youtube_comments(video_id)
    
    print("Analyzing sentiments...")
    sentiments = analyze_sentiments(comments)

    data = pd.DataFrame({
        'Comment': comments,
        'Sentiment': sentiments
    })
    data.to_csv('youtube_comments_analysis.csv', index=False)

    print("Analysis complete! Results saved to 'youtube_comments_analysis.csv'")
