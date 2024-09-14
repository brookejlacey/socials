def get_engagement_metrics(metrics):
    total_interactions = metrics.get('likes', 0) + metrics.get('comments', 0) + metrics.get('shares', 0)
    followers = metrics.get('followers', 1)  # Avoid division by zero
    
    engagement_rate = (total_interactions / followers) * 100
    
    return {
        'total_interactions': total_interactions,
        'engagement_rate': round(engagement_rate, 2)
    }
