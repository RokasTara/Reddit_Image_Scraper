import json
import praw
import urllib.request

def save_credentials(credentials):
    with open('credentials.json', 'w') as f:
        json.dump(credentials, f)
           
# load reddit credentials
def load_credentials():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials

#create reddit instance
def create_reddit_object():
    credentials = load_credentials()
    reddit = praw.Reddit(client_id=credentials['client_id'],
                     client_secret=credentials['client_secret'],
                     user_agent=credentials['user_agent'],
                     username = credentials['username'],
                     password = credentials['password'])
    return reddit

#download image
def download_image(url, filename):
    try: urllib.request.urlretrieve(url, filename)
    
    except TypeError:
        print("failed to download the file")
        return
    
def generate_filename(url):
    return "downloads/" + url.split('/')[-1]