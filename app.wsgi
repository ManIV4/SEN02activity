import sys
import logging

# Set up logging to catch any errors during startup
logging.basicConfig(stream=sys.stderr)

# Add your project directory to the system path
sys.path.insert(0, "/var/www/steam-dashboard")

# Import the Flask app object from your app.py
from app import app as application
