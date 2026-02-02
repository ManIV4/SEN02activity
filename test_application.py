#!/usr/bin/env python3
"""
Steam Dashboard - Comprehensive Test Script
Tests all components of the application before deployment
"""

import requests
import sys
import time
from datetime import datetime

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def test_python_version():
    """Test if Python version is compatible"""
    print_header("Testing Python Version")
    version = sys.version_info
    print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Python version is compatible (3.8+)")
        return True
    else:
        print_error("Python version must be 3.8 or higher")
        return False

def test_module_imports():
    """Test if required modules can be imported"""
    print_header("Testing Module Imports")
    
    modules = ['flask', 'requests']
    all_imported = True
    
    for module_name in modules:
        try:
            __import__(module_name)
            print_success(f"Module '{module_name}' imported successfully")
        except ImportError:
            print_error(f"Module '{module_name}' not found. Install with: pip3 install {module_name}")
            all_imported = False
    
    return all_imported

def test_steam_api():
    """Test Steam API connectivity and response"""
    print_header("Testing Steam API Connectivity")
    
    # Test 1: Top Games API
    print_info("Testing GetMostPlayedGames endpoint...")
    try:
        url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'response' in data and 'ranks' in data['response']:
            games = data['response']['ranks']
            print_success(f"Steam API responded with {len(games)} games")
            print_info(f"Top game: {games[0] if games else 'No games'}")
        else:
            print_error("Unexpected API response format")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Steam API request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print_error(f"Steam API request failed: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False
    
    # Test 2: Game Details API
    print_info("\nTesting App Details endpoint...")
    try:
        test_app_id = 730  # Counter-Strike 2
        url = f"https://store.steampowered.com/api/appdetails?appids={test_app_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if str(test_app_id) in data and data[str(test_app_id)]['success']:
            game_data = data[str(test_app_id)]['data']
            print_success(f"Game details retrieved for: {game_data.get('name', 'Unknown')}")
        else:
            print_warning("Game details API returned unexpected format")
            
    except Exception as e:
        print_warning(f"Game details test failed (non-critical): {e}")
    
    # Test 3: Reviews API
    print_info("\nTesting Reviews endpoint...")
    try:
        test_app_id = 730
        url = f"https://store.steampowered.com/appreviews/{test_app_id}"
        params = {'json': 1, 'num_per_page': 5}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'reviews' in data:
            print_success(f"Reviews retrieved: {len(data['reviews'])} reviews")
        else:
            print_warning("Reviews API returned unexpected format")
            
    except Exception as e:
        print_warning(f"Reviews test failed (non-critical): {e}")
    
    return True

def test_flask_app():
    """Test Flask application locally"""
    print_header("Testing Flask Application")
    
    print_info("Attempting to import app.py...")
    try:
        from app import app
        print_success("Flask app imported successfully")
    except ImportError as e:
        print_error(f"Failed to import app.py: {e}")
        return False
    except Exception as e:
        print_error(f"Error importing app: {e}")
        return False
    
    # Test Flask routes
    print_info("\nTesting Flask routes...")
    try:
        with app.test_client() as client:
            # Test home route
            response = client.get('/')
            if response.status_code == 200:
                print_success("Home route (/) working")
            else:
                print_error(f"Home route returned status {response.status_code}")
                return False
            
            # Test health check
            response = client.get('/api/health')
            if response.status_code == 200:
                data = response.get_json()
                print_success(f"Health check working: {data}")
            else:
                print_error(f"Health check returned status {response.status_code}")
                return False
            
    except Exception as e:
        print_error(f"Flask route test failed: {e}")
        return False
    
    return True

def test_flask_data_endpoint():
    """Test the main data endpoint (this may take longer)"""
    print_header("Testing Data Endpoint")
    
    print_warning("This test fetches real data from Steam and may take 30-60 seconds...")
    
    try:
        from app import app
        with app.test_client() as client:
            start_time = time.time()
            response = client.get('/api/data')
            elapsed_time = time.time() - start_time
            
            print_info(f"Request completed in {elapsed_time:.2f} seconds")
            
            if response.status_code == 200:
                data = response.get_json()
                
                # Validate response structure
                if 'games' in data and 'trends' in data and 'timestamp' in data:
                    print_success(f"Data endpoint working correctly")
                    print_info(f"Games fetched: {data.get('total_games', 0)}")
                    print_info(f"Total players: {data.get('trends', {}).get('total_players', 0):,}")
                    print_info(f"Timestamp: {data.get('timestamp')}")
                    
                    # Show sample game
                    if data['games']:
                        game = data['games'][0]
                        print_info(f"\nTop game: {game.get('name', 'Unknown')}")
                        print_info(f"  Players: {game.get('concurrent_players', 0):,}")
                        print_info(f"  Sentiment: {game.get('sentiment_ratio', 0)}% ({game.get('sentiment_label', 'Unknown')})")
                    
                    return True
                else:
                    print_error("Data endpoint returned incomplete data")
                    print_info(f"Response keys: {data.keys()}")
                    return False
            else:
                print_error(f"Data endpoint returned status {response.status_code}")
                return False
                
    except Exception as e:
        print_error(f"Data endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test if all required files are present"""
    print_header("Testing File Structure")
    
    import os
    
    required_files = [
        'app.py',
        'requirements.txt',
        'app.wsgi',
        'steam-dashboard.conf',
        'README.md',
        'templates/dashboard.html'
    ]
    
    all_present = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print_success(f"Found: {filepath}")
        else:
            print_error(f"Missing: {filepath}")
            all_present = False
    
    return all_present

def test_templates():
    """Test if HTML template is valid"""
    print_header("Testing HTML Templates")
    
    try:
        with open('templates/dashboard.html', 'r') as f:
            content = f.read()
            
        # Basic validation
        if '<html' in content:
            print_success("HTML structure found")
        else:
            print_error("HTML structure missing")
            return False
            
        if 'Steam' in content:
            print_success("Steam-related content found")
        else:
            print_warning("No Steam-related content found")
            
        if 'api/data' in content:
            print_success("API endpoint reference found")
        else:
            print_warning("No API endpoint reference found")
            
        return True
        
    except Exception as e:
        print_error(f"Template test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print(f"\n{BLUE}{'='*60}")
    print("STEAM DASHBOARD - COMPREHENSIVE TEST SUITE")
    print(f"{'='*60}{RESET}\n")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Python Version", test_python_version),
        ("Module Imports", test_module_imports),
        ("File Structure", test_file_structure),
        ("HTML Templates", test_templates),
        ("Steam API", test_steam_api),
        ("Flask Application", test_flask_app),
        ("Data Endpoint", test_flask_data_endpoint),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print_warning("\n\nTests interrupted by user")
            sys.exit(1)
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed == total:
        print(f"{GREEN}ALL TESTS PASSED! ({passed}/{total}){RESET}")
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"\n{GREEN}✓ Your application is ready for deployment!{RESET}\n")
        return 0
    else:
        print(f"{RED}SOME TESTS FAILED ({passed}/{total} passed){RESET}")
        print(f"{RED}{'='*60}{RESET}")
        print(f"\n{RED}✗ Please fix the issues above before deploying{RESET}\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_warning("\n\nTests interrupted by user")
        sys.exit(1)
