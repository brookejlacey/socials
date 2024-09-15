from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from config import Config
from models import db, User, SocialMediaAccount
from social_media_handler import SocialMediaHandler
from scraper import Scraper
from scheduler import scheduler
from utils import get_engagement_metrics
import logging

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
scheduler.init_app(app)
scheduler.start()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

social_media_handler = SocialMediaHandler()
scraper = Scraper()

@app.route('/')
def index():
    accounts = SocialMediaAccount.query.all()
    return render_template('dashboard.html', accounts=accounts)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/posting')
def posting():
    return render_template('posting.html')

@app.route('/api/add_account', methods=['POST'])
def add_account():
    try:
        data = request.json
        logger.info(f"Received add_account request with data: {data}")
        
        platform = data['platform']
        handle = data['handle']
        
        user = User.query.first()
        if not user:
            logger.info("No user found. Creating default user.")
            user = User(username="default_user", email="default@example.com")
            db.session.add(user)
            db.session.commit()
        
        account = SocialMediaAccount(user_id=user.id, platform=platform, handle=handle)
        db.session.add(account)
        db.session.commit()
        
        logger.info(f"Successfully added account: {platform} - {handle}")
        return jsonify({'success': True, 'id': account.id, 'platform': account.platform, 'handle': account.handle})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({'success': False, 'error': 'Database error occurred'}), 500
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500

@app.route('/api/get_analytics')
def get_analytics():
    try:
        accounts = SocialMediaAccount.query.all()
        analytics = {}
        
        for account in accounts:
            if account.platform in social_media_handler.active_platforms:
                metrics = social_media_handler.get_metrics(account.platform, account.handle)
            else:
                metrics = scraper.get_metrics(account.platform, account.handle)
            
            analytics[account.id] = {
                'platform': account.platform,
                'handle': account.handle,
                'metrics': get_engagement_metrics(metrics)
            }
        
        logger.info(f"Successfully retrieved analytics for {len(accounts)} accounts")
        return jsonify(analytics)
    except Exception as e:
        logger.error(f"Error in get_analytics: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching analytics'}), 500

@app.route('/api/post_update', methods=['POST'])
def post_update():
    data = request.json
    platform = data['platform']
    message = data['message']
    schedule_time = data.get('schedule_time')
    
    if schedule_time:
        scheduler.add_job(
            social_media_handler.post_update,
            'date',
            run_date=schedule_time,
            args=[platform, message]
        )
        return jsonify({'success': True, 'message': 'Post scheduled'})
    else:
        success = social_media_handler.post_update(platform, message)
        return jsonify({'success': success})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
