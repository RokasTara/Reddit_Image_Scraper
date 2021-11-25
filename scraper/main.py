import praw
import json
import time
from utils import *

reddit = create_reddit_object()

subreddits = ["memes", "dankmemes", "meme", "Memes_Of_The_Dank"]

subreddit = reddit.subreddit('memes')

hot = subreddit.hot(limit=1000)
date = get_current_date()

for name in subreddits:
    top = reddit.subreddit(name).top(limit=50, time_filter='day')
    create_directory(name)
    path = create_directory_for_date(name, get_current_date())
    
    for submission in top:
        if submission.url.endswith(".jpg") or submission.url.endswith(".png") or submission.url.endswith(".gif") or submission.url.endswith(".jpeg") or submission.url.endswith(".webp"): 
            filename = generate_filename(submission.url, path)
            if not os.path.isfile(filename):
                download_image(submission.url, filename)
                print("Downloaded: " + submission.url)
            else:
                print("Already Downloaded: " + submission.url)

    
