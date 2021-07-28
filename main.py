from tuya_bulb_control import Bulb
from dotenv import load_dotenv
from time import sleep
import tweepy
import os

load_dotenv()

# Create bulb
bulb = Bulb(
    client_id=os.getenv('CLIENT_ID'),
    secret_key=os.getenv('SECRET_KEY'),
    device_id=os.getenv('DEVICE_ID'),
    region_key=os.getenv('REGION_KEY'),
)

CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')

ACCESS_KEY = os.getenv('TWITTER_ACCESS_KEY')
ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

# authenticate with the Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# define default followers count
count = 0


def get_latest_data():
    user = api.me()

    return user.followers_count


def notify_default():
    bulb.set_colour_v2(rgb=(255, 255, 255))  # white


def notify_unfollow():
    bulb.set_colour_v2(rgb=(255, 0, 0))  # red


def notify_follow():
    bulb.set_colour_v2(rgb=(0, 255, 0))  # green


while True:
    # get latest user data
    user_followers_count = get_latest_data()

    if count > 0:
        if user_followers_count > count:
            notify_follow()
        if user_followers_count < count:
            notify_unfollow()
        else:
            notify_default()

    count = user_followers_count
    sleep(1)  # add delay 1s
