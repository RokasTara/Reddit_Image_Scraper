import json
import praw
import time
import urllib.request
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(levelname)s - %(message)s', filename='scraper.log')

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
        try:
            with open('credentials.json', 'r') as f:
                credentials = json.load(f)
            return credentials
        except FileNotFoundError:
            logging.critical("Credentials file not found")
            return None

    #create reddit instance
    def create_reddit_object(self):
        credentials = self.load_credentials()
        reddit = praw.Reddit(client_id=credentials['client_id'],
                        client_secret=credentials['client_secret'],
                        user_agent=credentials['user_agent'],
                        username = credentials['username'],
                        password = credentials['password'])
        logging.info("Reddit object created")
        return reddit

    #download image
    @staticmethod
    def download_image(url, filename):
        try: urllib.request.urlretrieve(url, filename)
        
        except TypeError:
            logging.error("failed to download the image")
            return
    
    @staticmethod    
    def generate_filename(url, path):
        try: 
            os.mkdir(path + "files/")
            logging.info(f"directory {path}files/ was created")
        except:
            logging.info(f"Directory \"{path}\"files/ already exist")
            pass
        return path + "files/" + url.split('/')[-1]

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
            logging.info(f"Directory \"{directory}\" created")
        except:
            logging.info(f"Directory \"{directory}\" already exist")
            pass
        return directory

    @staticmethod
    def create_directory_for_date(subreddit : str, date : str): 
        directory = f"downloads/{subreddit}/{date}"
        try: 
            os.mkdir(directory)
            logging.info(f"Directory \"{directory}\" created")
        except:
            logging.info(f"Directory \"{directory}\" already exist")
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
        metrics = []
        self.create_directory(subreddit)
        path = self.create_directory_for_date(subreddit, self.get_current_date())
        for submission in self.top_posts(subreddit, limit, time_filter):
            filename = self.generate_filename(submission.url, path)
            comment_list = self.get_top_comments(submission)
            metrics.append(self.generate_metrics(submission, filename, comment_list))
            if self.is_image(submission):
                self.download_image(submission.url, filename)
                logging.info(f"Downloaded {submission.url}")
            else:
                logging.warning(f"{submission.url} is not an image")
        self.save_metrics_to_csv(metrics, path + 'metrics.csv')
                
    #download images from a list of subreddits 
    def download_images_from_list(self, subreddits=subreddits, limit=5, time_filter='day'):
        for subreddit in subreddits:
            self.download_images(subreddit, limit, time_filter)
     
    #TODO fix comment saving to the csv file cause that motherfucker is broken       
    # get a list of n top coments from a submission
    def get_top_comments(self, submission, n=5):
        comments = []
        submission.comment_sort = 'best'
        submission.comment_limit = n
        for comment in submission.comments:
            if isinstance(comment, praw.models.MoreComments):
                continue
            comments.append(comment.body)

    # generate metrics of the submission 
    def generate_metrics(self, submission, filename, comments):
        metrics = {
            'filename':filename,
            'title': submission.title,
            'score': submission.score,
            'url': submission.url,
            'created_utc': submission.created_utc,
            'num_comments': submission.num_comments,
            'top_comments': comments,
            'subreddit': submission.subreddit.display_name,
            'author': submission.author.name,
            'is_self': submission.is_self,
            'is_video': submission.is_video,
            'is_image': self.is_image(submission),
            'is_stickied': submission.stickied,
            'is_nsfw': submission.over_18}
        return metrics
    
    #save metrics to a csv file
    def save_metrics_to_csv(self, metrics, filename):
        df = pd.DataFrame(metrics)
        df.to_csv(filename, index=False)
        

        


        
        




scraper = RedditScraper()

scraper.download_images_from_list()


