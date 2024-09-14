import tweepy
import facebook
from linkedin_api import Linkedin
from instagram_private_api import Client as InstagramClient, ClientError
from TikTokApi import TikTokApi
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialMediaHandler:
    def __init__(self):
        self.supported_platforms = ['twitter', 'facebook', 'instagram', 'linkedin', 'tiktok']
        self.clients = {
            'twitter': self._init_twitter(),
            'facebook': self._init_facebook(),
            'instagram': self._init_instagram(),
            'linkedin': self._init_linkedin(),
            'tiktok': self._init_tiktok()
        }
        self.active_platforms = [platform for platform, client in self.clients.items() if client is not None]

    def _init_twitter(self):
        try:
            if not Config.TWITTER_CONSUMER_KEY or not Config.TWITTER_CONSUMER_SECRET or not Config.TWITTER_ACCESS_TOKEN or not Config.TWITTER_ACCESS_TOKEN_SECRET:
                logger.error("Twitter credentials are missing in the environment variables")
                return None

            auth = tweepy.OAuth1UserHandler(
                Config.TWITTER_CONSUMER_KEY,
                Config.TWITTER_CONSUMER_SECRET,
                Config.TWITTER_ACCESS_TOKEN,
                Config.TWITTER_ACCESS_TOKEN_SECRET
            )
            return tweepy.API(auth)
        except Exception as e:
            logger.error(f"Error initializing Twitter client: {str(e)}")
            return None

    def _init_facebook(self):
        try:
            if not Config.FACEBOOK_ACCESS_TOKEN:
                logger.error("Facebook access token is missing in the environment variables")
                return None

            return facebook.GraphAPI(access_token=Config.FACEBOOK_ACCESS_TOKEN)
        except Exception as e:
            logger.error(f"Error initializing Facebook client: {str(e)}")
            return None

    def _init_instagram(self):
        try:
            if not Config.INSTAGRAM_USERNAME or not Config.INSTAGRAM_PASSWORD:
                logger.error("Instagram credentials are missing in the environment variables")
                return None

            return InstagramClient(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD)
        except ClientError as e:
            logger.error(f"Instagram client error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error initializing Instagram client: {str(e)}")
            return None

    def _init_linkedin(self):
        try:
            if not Config.LINKEDIN_USERNAME or not Config.LINKEDIN_PASSWORD:
                logger.error("LinkedIn credentials are missing in the environment variables")
                return None
            return Linkedin(Config.LINKEDIN_USERNAME, Config.LINKEDIN_PASSWORD)
        except Exception as e:
            logger.error(f"Error initializing LinkedIn client: {str(e)}")
            if "CHALLENGE" in str(e):
                logger.error("LinkedIn login requires a security challenge. Please log in manually and try again.")
            return None

    def _init_tiktok(self):
        try:
            return TikTokApi()
        except Exception as e:
            logger.error(f"Error initializing TikTok client: {str(e)}")
            return None

    def get_metrics(self, platform, handle):
        if platform not in self.active_platforms:
            logger.warning(f"Platform {platform} is not active or supported")
            return {}

        client = self.clients[platform]

        try:
            if platform == 'twitter':
                user = client.get_user(screen_name=handle)
                tweets = client.user_timeline(screen_name=handle, count=100)
                return {
                    'followers': user.followers_count,
                    'likes': sum(tweet.favorite_count for tweet in tweets),
                    'retweets': sum(tweet.retweet_count for tweet in tweets)
                }
            elif platform == 'facebook':
                # Implement Facebook metrics retrieval
                logger.warning("Facebook metrics retrieval is not implemented")
                return {}
            elif platform == 'instagram':
                # Implement Instagram metrics retrieval
                logger.warning("Instagram metrics retrieval is not implemented")
                return {}
            elif platform == 'linkedin':
                logger.warning("LinkedIn metrics retrieval is not implemented")
                return {}
            elif platform == 'tiktok':
                # Implement TikTok metrics retrieval
                logger.warning("TikTok metrics retrieval is not implemented")
                return {}
        except Exception as e:
            logger.error(f"Error getting metrics for {platform}: {str(e)}")
            return {}

    def post_update(self, platform, message):
        if platform not in self.active_platforms:
            logger.warning(f"Platform {platform} is not active or supported")
            return False

        client = self.clients[platform]

        try:
            if platform == 'twitter':
                client.update_status(message)
            elif platform == 'facebook':
                client.put_object(parent_object='me', connection_name='feed', message=message)
            elif platform == 'instagram':
                logger.warning("Instagram posting is not implemented")
                return False
            elif platform == 'linkedin':
                logger.warning("LinkedIn posting is not implemented")
                return False
            elif platform == 'tiktok':
                logger.warning("TikTok posting is not implemented")
                return False
            else:
                logger.warning(f"Posting not implemented for {platform}")
                return False
            return True
        except Exception as e:
            logger.error(f"Error posting update to {platform}: {str(e)}")
            return False
