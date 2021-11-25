import json
import praw
import time
import urllib.request
import os

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
    
def generate_filename(url, path):
    return path + url.split('/')[-1]

# get current date
def get_current_date():
    return time.strftime("%Y-%m-%d")

# create a directory for the current date with name of subreddit and current date
def create_directory(subreddit : str): 
    directory = f"{subreddit}"
    try: 
        os.mkdir("downloads/" + directory)
    except:
        print(f"Directory \"{directory}\" already exist")
        pass
    return directory

def create_directory_for_date(subreddit : str, date : str): 
    directory = f"downloads/{subreddit}/{date}"
    try: 
        os.mkdir(directory)
    except:
        print(f"Directory \"{directory}\" already exist")
        pass
    return directory + '/'
    

