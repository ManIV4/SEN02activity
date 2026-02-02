"""
Steam Game Trends Dashboard
Fetches live data from Steam API and performs sentiment/trend analysis
"""

from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime
from collections import Counter
import re

app = Flask(__name__)

# Steam API endpoints
STEAM_TOP_GAMES_URL = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"
STEAM_REVIEWS_URL = "https://store.steampowered.com/appreviews/"

def fetch_top_games(limit=10):
    """Fetch top games by current player count from Steam"""
    try:
        response = requests.get(STEAM_TOP_GAMES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'response' in data and 'ranks' in data['response']:
            games = data['response']['ranks'][:limit]
            return games
        return []
    except Exception as e:
        print(f"Error fetching top games: {e}")
        return []

def fetch_game_details(app_id):
    """Fetch detailed information about a specific game"""
    try:
        params = {'appids': app_id}
        response = requests.get(STEAM_APP_DETAILS_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if str(app_id) in data and data[str(app_id)]['success']:
            return data[str(app_id)]['data']
        return None
    except Exception as e:
        print(f"Error fetching game details for {app_id}: {e}")
        return None

def fetch_game_reviews(app_id, num_reviews=20):
    """Fetch recent reviews for a game"""
    try:
        url = f"{STEAM_REVIEWS_URL}{app_id}"
        params = {
            'json': 1,
            'language': 'english',
            'num_per_page': num_reviews,
            'purchase_type': 'all'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'reviews' in data:
            return data['reviews']
        return []
    except Exception as e:
        print(f"Error fetching reviews for {app_id}: {e}")
        return []

def analyze_sentiment(reviews):
    """
    Simple sentiment analysis based on Steam's recommendation system
    Returns: positive_ratio, total_reviews, sentiment_score
    """
    if not reviews:
        return 0, 0, "No Data"
    
    positive = sum(1 for r in reviews if r.get('voted_up', False))
    total = len(reviews)
    ratio = (positive / total * 100) if total > 0 else 0
    
    # Sentiment categories
    if ratio >= 80:
        sentiment = "Overwhelmingly Positive"
    elif ratio >= 70:
        sentiment = "Very Positive"
    elif ratio >= 60:
        sentiment = "Positive"
    elif ratio >= 50:
        sentiment = "Mixed"
    elif ratio >= 40:
        sentiment = "Negative"
    else:
        sentiment = "Very Negative"
    
    return ratio, total, sentiment

def analyze_trends(games_data):
    """
    Analyze trends across top games
    """
    genres = []
    categories = []
    total_players = 0
    
    for game in games_data:
        if 'details' in game and game['details']:
            details = game['details']
            
            # Extract genres
            if 'genres' in details:
                genres.extend([g['description'] for g in details['genres']])
            
            # Extract categories
            if 'categories' in details:
                categories.extend([c['description'] for c in details['categories']])
        
        # Sum player counts
        total_players += game.get('concurrent_in_game', 0)
    
    # Get top genres and categories
    top_genres = Counter(genres).most_common(5)
    top_categories = Counter(categories).most_common(5)
    
    return {
        'total_players': total_players,
        'top_genres': top_genres,
        'top_categories': top_categories
    }

@app.route('/')
def index():
    """Render the dashboard homepage"""
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    """API endpoint that returns analyzed Steam data"""
    # Fetch top games
    top_games = fetch_top_games(10)
    
    enriched_games = []
    for game in top_games:
        app_id = game.get('appid')
        rank = game.get('rank')
        concurrent_players = game.get('concurrent_players', 0)
        
        # Fetch game details
        details = fetch_game_details(app_id)
        
        # Fetch and analyze reviews
        reviews = fetch_game_reviews(app_id, 20)
        sentiment_ratio, review_count, sentiment_label = analyze_sentiment(reviews)
        
        game_data = {
            'rank': rank,
            'app_id': app_id,
            'name': details.get('name', 'Unknown') if details else 'Unknown',
            'concurrent_players': concurrent_players,
            'sentiment_ratio': round(sentiment_ratio, 1),
            'sentiment_label': sentiment_label,
            'review_count': review_count,
            'details': details
        }
        
        enriched_games.append(game_data)
    
    # Analyze overall trends
    trends = analyze_trends(enriched_games)
    
    response_data = {
        'games': enriched_games,
        'trends': trends,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_games': len(enriched_games)
    }
    
    return jsonify(response_data)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

