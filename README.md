# 🎮 Steam Game Trends Dashboard

A real-time web application that fetches live data from Steam API, performs sentiment analysis on game reviews, and displays trending games on an auto-refreshing dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Team Members](#team-members)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Deployment](#deployment)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Management](#project-management)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🎯 Overview

This project is a collaborative effort to create a Python web application hosted on an Apache web server that:
- Fetches live data from Steam's public API
- Analyzes sentiment from game reviews
- Identifies trending genres and categories
- Displays results on an auto-refreshing HTML dashboard
- Implements full Git workflow for team collaboration

**No database required** - all data is fetched in real-time!

## ✨ Features

### Data Collection
- ✅ Fetches top 10 most-played Steam games by current player count
- ✅ Retrieves detailed game information (genres, categories, descriptions)
- ✅ Pulls recent user reviews for sentiment analysis

### Analysis
- ✅ **Sentiment Analysis**: Calculates positive/negative review ratios
- ✅ **Trend Analysis**: Identifies popular genres and game categories
- ✅ **Player Statistics**: Aggregates total concurrent players
- ✅ **Rating System**: Categorizes games from "Very Negative" to "Overwhelmingly Positive"

### Dashboard
- ✅ **Auto-refresh**: Updates every 60 seconds automatically
- ✅ **Real-time Stats**: Shows total players, games tracked, average sentiment
- ✅ **Game Cards**: Displays rank, name, player count, and sentiment for each game
- ✅ **Visual Elements**: Progress bars, color-coded sentiment indicators
- ✅ **Trend Visualization**: Top genres and categories charts
- ✅ **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

```
┌─────────────┐
│   Browser   │
│  (Client)   │
└──────┬──────┘
       │ HTTP/HTTPS
       ▼
┌─────────────────┐
│  Apache Server  │
│   (mod_wsgi)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask App      │
│  (app.py)       │
└────────┬────────┘
         │
         ├─► Steam API (Top Games)
         ├─► Steam API (Game Details)
         └─► Steam API (Reviews)
```

### Technology Stack
- **Backend**: Python 3.8+, Flask 3.0
- **Web Server**: Apache 2.4 with mod_wsgi
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **APIs**: Steam Web API (no authentication required)
- **Version Control**: Git
- **Deployment**: Ubuntu 24.04 on Azure/Local VM

## 👥 Team Members

| Role | Name | Responsibilities |
|------|------|------------------|
| **Team Lead & DevOps** | Roman IV Canlas | Git management, deployment, Apache config |
| **Backend Developer** | Emmanuel Sagcal | Flask app, API integration, endpoints |
| **Data Analyst** | Robert Benj Manuel | Sentiment analysis, trend analysis, algorithms |
| **Frontend Developer** | Carlo Glenn Dalusung | HTML/CSS/JS, dashboard UI, auto-refresh |

## 📦 Prerequisites

### Ubuntu VM Requirements
- Ubuntu 24.04 LTS (or 20.04/22.04)
- Python 3.8 or higher
- Apache 2.4
- 2GB RAM minimum
- Internet connection for API access

### Required Software
```bash
sudo apt update
sudo apt install -y python3 python3-pip apache2 libapache2-mod-wsgi-py3 git
```

### Python Dependencies
See `requirements.txt`:
- Flask==3.0.0
- requests==2.31.0
- gunicorn==21.2.0

## 🚀 Installation

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/ManIV4/SEN02activity.git
cd SEN02activity
```

### 2. Install Python Dependencies

```bash
# Install globally (simple method)
sudo pip3 install -r requirements.txt --break-system-packages

# OR use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Test Locally

```bash
# Run the Flask development server
python3 app.py

# Open browser to http://localhost:5000
```

You should see the dashboard loading and fetching Steam data!

## 🌐 Deployment

### Automated Deployment (Recommended)

```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment script
sudo ./deploy.sh
```

The script will:
1. Install required packages
2. Copy files to `/var/www/steam-dashboard`
3. Install Python dependencies
4. Configure Apache
5. Set proper permissions
6. Restart Apache

### Manual Deployment

If you prefer to deploy manually:

#### Step 1: Copy Files
```bash
sudo mkdir -p /var/www/steam-dashboard
sudo cp -r ./* /var/www/steam-dashboard/
```

#### Step 2: Install Dependencies
```bash
cd /var/www/steam-dashboard
sudo pip3 install -r requirements.txt --break-system-packages
```

#### Step 3: Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/steam-dashboard
sudo chmod -R 755 /var/www/steam-dashboard
```

#### Step 4: Configure Apache
```bash
# Copy Apache configuration
sudo cp steam-dashboard.conf /etc/apache2/sites-available/

# Enable site and mod_wsgi
sudo a2ensite steam-dashboard
sudo a2enmod wsgi

# Disable default site (optional)
sudo a2dissite 000-default

# Test configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

#### Step 5: Verify Deployment
```bash
# Check Apache status
sudo systemctl status apache2

# View logs
sudo tail -f /var/log/apache2/steam-dashboard-error.log
```

### Access Your Dashboard

Open a browser and navigate to:
- **Local access**: `http://localhost`
- **Remote access**: `http://YOUR_VM_IP_ADDRESS`

To find your VM's IP:
```bash
hostname -I
```

## 🎮 Usage

### Dashboard Features

1. **Auto-Refresh**: The dashboard automatically refreshes every 60 seconds
2. **Live Stats**: View total players online, games tracked, and average sentiment
3. **Game Rankings**: See top 10 most-played Steam games with:
   - Current player count
   - Sentiment score (percentage)
   - Review count analyzed
   - Overall sentiment label
4. **Trend Analysis**: Explore popular genres and game categories

### Manual Refresh

If you want to refresh immediately, simply reload the page (F5 or Ctrl+R).

## 🔌 API Endpoints

### `GET /`
Returns the main dashboard HTML page.

**Response**: HTML page

---

### `GET /api/data`
Fetches and analyzes Steam game data.

**Response**:
```json
{
  "games": [
    {
      "rank": 1,
      "app_id": 730,
      "name": "Counter-Strike 2",
      "concurrent_players": 850000,
      "sentiment_ratio": 75.5,
      "sentiment_label": "Very Positive",
      "review_count": 20
    }
  ],
  "trends": {
    "total_players": 5000000,
    "top_genres": [["Action", 8], ["Shooter", 6]],
    "top_categories": [["Multiplayer", 9], ["PvP", 7]]
  },
  "timestamp": "2026-02-02 14:30:00",
  "total_games": 10
}
```

---

### `GET /api/health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-02T14:30:00"
}
```

## 📊 Project Management

### Methodology
This project follows **Agile/Scrum** methodology with:
- 1-week sprint
- Daily standup meetings (15 minutes)
- Feature-based development
- Continuous integration via Git

### Git Workflow

#### Branching Strategy
```
main (production)
  └── dev (integration)
       ├── feature/backend
       ├── feature/frontend
       └── feature/analytics
```

#### Daily Workflow
```bash
# Pull latest changes
git checkout feature/your-branch
git pull origin dev
git merge dev

# Work on features
# ... make changes ...

# Commit and push
git add .
git commit -m "Descriptive message"
git push origin feature/your-branch
```

#### Merge Process (Team Lead)
```bash
# Review and merge features to dev
git checkout dev
git merge feature/backend
git merge feature/analytics
git merge feature/frontend

# Test integration
python3 app.py

# Merge to main when ready
git checkout main
git merge dev
git push origin main
```

### Common Process Framework

1. **Initiating**: Team formation, role assignment, project charter
2. **Planning**: Timeline, Git strategy, risk management, scope definition
3. **Executing**: Daily development, code commits, testing
4. **Monitoring**: Daily standups, Git history review, progress tracking
5. **Closing**: Deployment, documentation, presentation, postmortem

### Postmortem Template

See `TEAM_WORKFLOW.md` for complete postmortem analysis template covering:
- What went well
- What went wrong
- Lessons learned
- Future improvements
- Project metrics

## 🤝 Contributing

### For Team Members

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd steam-dashboard
   ```

2. **Create/checkout your feature branch**
   ```bash
   git checkout feature/your-name
   ```

3. **Make changes and commit**
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

4. **Push to remote**
   ```bash
   git push origin feature/your-name
   ```

5. **Create Pull Request** (if using GitHub/GitLab)
   - Go to repository web interface
   - Click "New Pull Request"
   - Select your feature branch → dev
   - Add description and request review

### Code Style Guidelines

- Use descriptive variable names
- Add comments for complex logic
- Follow PEP 8 for Python code
- Test locally before committing
- Write clear commit messages

### Commit Message Format

```
[TYPE] Brief description

Detailed explanation if needed.

Examples:
[FEATURE] Add sentiment analysis function
[FIX] Resolve API timeout issue
[DOCS] Update README with deployment steps
[REFACTOR] Optimize data fetching logic
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Apache Won't Start
```bash
# Check configuration
sudo apache2ctl configtest

# View error logs
sudo tail -f /var/log/apache2/error.log

# Common fix: Restart Apache
sudo systemctl restart apache2
```

#### 2. Module 'wsgi' Not Found
```bash
# Install mod_wsgi
sudo apt install libapache2-mod-wsgi-py3

# Enable module
sudo a2enmod wsgi
sudo systemctl restart apache2
```

#### 3. Permission Denied Errors
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/steam-dashboard

# Fix permissions
sudo chmod -R 755 /var/www/steam-dashboard
```

#### 4. Steam API Not Responding
- Check internet connection
- Verify Steam API is online: https://steamstat.us/
- Check if you're hitting rate limits (unlikely with 60s refresh)
- Look for timeout errors in logs

#### 5. Dashboard Shows No Data
```bash
# Test API manually
python3 -c "import requests; print(requests.get('http://localhost/api/data').json())"

# Check Flask logs
sudo tail -f /var/log/apache2/steam-dashboard-error.log

# Verify Python packages installed
pip3 list | grep -E "Flask|requests"
```

#### 6. Port 80 Already in Use
```bash
# Check what's using port 80
sudo netstat -tulpn | grep :80

# Stop conflicting service or change port in Apache config
```

### Getting Help

1. **Check logs first**:
   ```bash
   sudo tail -f /var/log/apache2/steam-dashboard-error.log
   ```

2. **Test each component**:
   - Steam API connection
   - Flask app locally
   - Apache configuration

3. **Ask your team** in group chat

4. **Search error messages** online (Stack Overflow, GitHub Issues)

## 📈 Performance Optimization

### Current Performance
- Auto-refresh: 60 seconds (safe for API limits)
- API timeout: 10 seconds
- Fetches: 10 games + details + 20 reviews each

### Potential Improvements
- Implement caching (Redis/Memcached)
- Reduce refresh frequency to 120 seconds
- Fetch fewer reviews (10 instead of 20)
- Use async requests for parallel API calls
- Add lazy loading for game details

## 🔒 Security Considerations

- No API keys required (Steam public API)
- No user authentication needed
- No sensitive data stored
- Input validation on API responses
- Timeout limits to prevent hanging requests
- Error handling to prevent crashes

## 📜 License

This project is licensed under the MIT License - see below for details.

```
MIT License

Copyright (c) 2026 Steam Dashboard Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


**Built with ❤️ by the Steam Dashboard Team**

*Last Updated: February 2026*

