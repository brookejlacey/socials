import os

class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Social Media API Keys
    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    if not all([TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        raise ValueError("Missing required Twitter API credentials in environment variables.")

    FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
    if not FACEBOOK_ACCESS_TOKEN:
        raise ValueError("Missing Facebook Access Token in environment variables.")

    INSTAGRAM_USERNAME = os.environ.get('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.environ.get('INSTAGRAM_PASSWORD')
    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        raise ValueError("Missing Instagram credentials in environment variables.")

    LINKEDIN_USERNAME = os.environ.get('LINKEDIN_USERNAME')
    LINKEDIN_PASSWORD = os.environ.get('LINKEDIN_PASSWORD')
    if not LINKEDIN_USERNAME or not LINKEDIN_PASSWORD:
        raise ValueError("Missing LinkedIn credentials in environment variables.")
