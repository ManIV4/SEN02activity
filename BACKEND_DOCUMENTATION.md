# Backend Documentation - Person 2

## Steam API Integration

### Endpoints Used:
1. **GetMostPlayedGames**
   - URL: https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/
   - Purpose: Fetch top 10 games by player count
   - Returns: List of games with rank, app_id, concurrent players

2. **App Details**
   - URL: https://store.steampowered.com/api/appdetails?appids={id}
   - Purpose: Get game information (name, genres, categories)
   - Returns: Game metadata

3. **App Reviews**
   - URL: https://store.steampowered.com/appreviews/{id}
   - Purpose: Fetch user reviews for sentiment analysis
   - Returns: Recent reviews with voted_up/voted_down

## Data Flow:
1. Client requests `/api/data`
2. Flask calls `fetch_top_games()` → gets top 10 games
3. For each game:
   - Call `fetch_game_details()` → get game info
   - Call `fetch_game_reviews()` → get reviews
   - Call `analyze_sentiment()` → calculate sentiment
4. Aggregate all data
5. Return JSON to client

## Error Handling:
- 10-second timeout on all API calls
- Try-catch blocks for network errors
- Returns empty arrays on failure (graceful degradation)

## Testing Notes:
- All endpoints tested through browser
- API response times: 2-5 seconds for full data
- No rate limiting issues observed with 60s refresh

## Potential Improvements:
- Add caching layer (Redis)
- Implement retry logic
- Add request pooling for parallel API calls
- Monitor API response times

---
**Tested by:** [Emmanuel Sagcal]
**Date:** [February 02, 2026]
