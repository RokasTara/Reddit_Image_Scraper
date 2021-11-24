import praw
import json
from utils import *

reddit = create_reddit_object()

subreddit = reddit.subreddit('memes')

hot = subreddit.hot(limit=1000)

for post in hot:
    print(post.title)
    print(post.url)
    print("\n")

    download_image(post.url, generate_filename(post.url))