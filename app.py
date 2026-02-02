from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
from collections import Counter

app = Flask(__name__)

STEAM_TOP_GAMES_URL = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"
STEAM_REVIEWS_URL = "https://store.steampowered.com/appreviews/"

def fetch_top_games(limit=10):
    try:
        response = requests.get(STEAM_TOP_GAMES_URL, timeout=10)
        data = response.json()
        if 'response' in data and 'ranks' in data['response']:
            raw_games = data['response']['ranks'][:limit]
            for game in raw_games:
                game['concurrent_players'] = game.get('peak_in_game', 0)
            return raw_games
        return []
    except: return []

def fetch_game_details(app_id):
    try:
        response = requests.get(STEAM_APP_DETAILS_URL, params={'appids': app_id}, timeout=10)
        data = response.json()
        if str(app_id) in data and data[str(app_id)]['success']:
            return data[str(app_id)]['data']
        return None
    except: return None

def fetch_game_reviews(app_id):
    try:
        params = {'json': 1, 'language': 'english', 'num_per_page': 20}
        response = requests.get(f"{STEAM_REVIEWS_URL}{app_id}", params=params, timeout=10)
        return response.json().get('reviews', [])
    except: return []

def analyze_sentiment(reviews):
    if not reviews: return 0, 0, "No Data"
    positive = sum(1 for r in reviews if r.get('voted_up'))
    total = len(reviews)
    ratio = (positive / total * 100)
    if ratio >= 80: label = "Overwhelmingly Positive"
    elif ratio >= 70: label = "Very Positive"
    elif ratio >= 50: label = "Mixed"
    else: label = "Negative"
    return ratio, total, label

def analyze_trends(games_data):
    genres, categories, total_players = [], [], 0
    for game in games_data:
        total_players += game.get('concurrent_players', 0)
        if game.get('details'):
            genres.extend([g['description'] for g in game['details'].get('genres', [])])
            categories.extend([c['description'] for c in game['details'].get('categories', [])])
    return {
        'total_players': total_players,
        'top_genres': Counter(genres).most_common(5),
        'top_categories': Counter(categories).most_common(5)
    }

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    top_games = fetch_top_games(10)
    enriched_games = []
    for game in top_games:
        app_id = game.get('appid')
        details = fetch_game_details(app_id)
        sentiment_ratio, review_count, sentiment_label = analyze_sentiment(fetch_game_reviews(app_id))
        enriched_games.append({
            'rank': game.get('rank'),
            'app_id': app_id,
            'name': details.get('name', 'Unknown') if details else 'Unknown',
            'concurrent_players': game.get('concurrent_players', 0),
            'sentiment_ratio': round(sentiment_ratio, 1),
            'sentiment_label': sentiment_label,
            'review_count': review_count,
            'details': details
        })
    return jsonify({
        'games': enriched_games,
        'trends': analyze_trends(enriched_games),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_games': len(enriched_games)
    })

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
