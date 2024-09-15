import tweepy
import facebook
from linkedin_api import Linkedin
from instagram_private_api import Client as InstagramClient, ClientError
from TikTokApi import TikTokApi
from config import Config
import logging
from textblob import TextBlob
from collections import Counter
from datetime import datetime, timedelta
import numpy as np

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

            auth = tweepy.OAuthHandler(
                Config.TWITTER_CONSUMER_KEY,
                Config.TWITTER_CONSUMER_SECRET
            )
            auth.set_access_token(
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
                tweets = client.user_timeline(screen_name=handle, count=200)
                
                # Perform sentiment analysis on tweets
                sentiments = [TextBlob(tweet.text).sentiment.polarity for tweet in tweets]
                avg_sentiment = np.mean(sentiments) if sentiments else 0
                sentiment_std = np.std(sentiments) if sentiments else 0
                
                # Extract hashtags and mentions
                hashtags = [hashtag['text'] for tweet in tweets for hashtag in tweet.entities['hashtags']]
                mentions = [mention['screen_name'] for tweet in tweets for mention in tweet.entities['user_mentions']]
                
                # Calculate post frequency
                if len(tweets) > 1:
                    time_diff = tweets[0].created_at - tweets[-1].created_at
                    post_frequency = len(tweets) / (time_diff.days + 1)
                else:
                    post_frequency = 0
                
                # Determine best posting time
                posting_hours = [tweet.created_at.hour for tweet in tweets]
                best_posting_time = max(set(posting_hours), key=posting_hours.count)
                
                # Calculate engagement rate trends
                engagement_rates = [((tweet.favorite_count + tweet.retweet_count) / user.followers_count) * 100 for tweet in tweets]
                engagement_trend = np.polyfit(range(len(engagement_rates)), engagement_rates, 1)[0]
                
                return {
                    'followers': user.followers_count,
                    'likes': sum(tweet.favorite_count for tweet in tweets),
                    'retweets': sum(tweet.retweet_count for tweet in tweets),
                    'avg_sentiment': avg_sentiment,
                    'sentiment_std': sentiment_std,
                    'top_hashtags': Counter(hashtags).most_common(5),
                    'top_mentions': Counter(mentions).most_common(5),
                    'post_frequency': round(post_frequency, 2),
                    'best_posting_time': f"{best_posting_time}:00",
                    'engagement_trend': engagement_trend,
                    'engagement_rate': np.mean(engagement_rates)
                }
            elif platform == 'facebook':
                # Implement Facebook metrics retrieval (requires Facebook Graph API)
                logger.warning("Facebook metrics retrieval is not fully implemented")
                return {}
            elif platform == 'instagram':
                # Implement Instagram metrics retrieval (requires Instagram API)
                logger.warning("Instagram metrics retrieval is not fully implemented")
                return {}
            elif platform == 'linkedin':
                # Implement LinkedIn metrics retrieval (requires LinkedIn API)
                logger.warning("LinkedIn metrics retrieval is not fully implemented")
                return {}
            elif platform == 'tiktok':
                # Implement TikTok metrics retrieval (requires TikTok API)
                logger.warning("TikTok metrics retrieval is not fully implemented")
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
