import json
import praw
import time
import urllib.request
import os


# create a reddit scraper class to handle all the scraping 
class RedditScraper:

    subreddits = ["memes", "dankmemes", "meme", "Memes_Of_The_Dank"]

# create reddit object
    def __init__(self) -> None:
        self.reddit = self.create_reddit_object()
    
    def get_subreddit_posts(self, subreddit: str) -> list:
        subreddit = self.reddit.subreddit(subreddit)
        posts = subreddit.hot(limit=10)
        return posts
    
    @staticmethod
    def save_credentials(credentials):
        with open('credentials.json', 'w') as f:
            json.dump(credentials, f)
           
    # load reddit credentials
    @staticmethod
    def load_credentials():
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
        return credentials

    #create reddit instance
    def create_reddit_object(self):
        credentials = self.load_credentials()
        reddit = praw.Reddit(client_id=credentials['client_id'],
                        client_secret=credentials['client_secret'],
                        user_agent=credentials['user_agent'],
                        username = credentials['username'],
                        password = credentials['password'])
        return reddit

    #download image
    @staticmethod
    def download_image(url, filename):
        try: urllib.request.urlretrieve(url, filename)
        
        except TypeError:
            print("failed to download the file")
            return
    
    @staticmethod    
    def generate_filename(url, path):
        return path + url.split('/')[-1]

    # get current date
    @staticmethod
    def get_current_date():
        return time.strftime("%Y-%m-%d")

    # create a directory for the current date with name of subreddit and current date
    @staticmethod
    def create_directory(subreddit : str): 
        directory = f"{subreddit}"
        try: 
            os.mkdir("downloads/" + directory)
        except:
            print(f"Directory \"{directory}\" already exist")
            pass
        return directory

    @staticmethod
    def create_directory_for_date(subreddit : str, date : str): 
        directory = f"downloads/{subreddit}/{date}"
        try: 
            os.mkdir(directory)
        except:
            print(f"Directory \"{directory}\" already exist")
            pass
        return directory + '/'
    
    #returns a post generator from a subreddit
    def top_posts(self, subreddit: str, limit=5, time_filter='day'):
        top = self.reddit.subreddit(subreddit).top(limit=limit, time_filter=time_filter)
        return top
    
    #check if submission is an image
    @staticmethod
    def is_image(submission):
        return submission.url.endswith(".jpg") or submission.url.endswith(".png") or submission.url.endswith(".gif") or submission.url.endswith(".jpeg") or submission.url.endswith(".webp")
    
    def download_images(self, subreddit, limit=5, time_filter='day'):
        self.create_directory(subreddit)
        path = self.create_directory_for_date(subreddit, self.get_current_date())
        for submission in self.top_posts(subreddit, limit, time_filter):
            if self.is_image(submission):
                self.download_image(submission.url, self.generate_filename(submission.url, path))
                print(f"Downloaded {submission.url}")
            else:
                print(f"{submission.url} is not an image")
                
    #download images from a list of subreddits 
    def download_images_from_list(self, subreddits=subreddits, limit=5, time_filter='day'):
        for subreddit in subreddits:
            self.download_images(subreddit, limit, time_filter)




scraper = RedditScraper()

scraper.download_images_from_list()


