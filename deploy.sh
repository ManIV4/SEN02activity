#!/bin/bash
# Steam Dashboard - Apache Deployment Script
# Run this script on Ubuntu VM to deploy the application

echo "========================================="
echo "Steam Dashboard - Apache Deployment"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run with sudo: sudo bash deploy.sh${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Installing required packages...${NC}"
apt update
apt install -y python3 python3-pip apache2 libapache2-mod-wsgi-py3 git

echo -e "${GREEN}✓ Packages installed${NC}"
echo ""

echo -e "${YELLOW}Step 2: Creating web directory...${NC}"
mkdir -p /var/www/steam-dashboard
echo -e "${GREEN}✓ Directory created${NC}"
echo ""

echo -e "${YELLOW}Step 3: Copying application files...${NC}"
# Assuming script is run from the project directory
cp -r ./* /var/www/steam-dashboard/
echo -e "${GREEN}✓ Files copied${NC}"
echo ""

echo -e "${YELLOW}Step 4: Installing Python dependencies...${NC}"
cd /var/www/steam-dashboard
pip3 install -r requirements.txt --break-system-packages
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

echo -e "${YELLOW}Step 5: Setting permissions...${NC}"
chown -R www-data:www-data /var/www/steam-dashboard
chmod -R 755 /var/www/steam-dashboard
echo -e "${GREEN}✓ Permissions set${NC}"
echo ""

echo -e "${YELLOW}Step 6: Configuring Apache...${NC}"
# Copy Apache configuration
cp /var/www/steam-dashboard/steam-dashboard.conf /etc/apache2/sites-available/

# Enable site and mod_wsgi
a2ensite steam-dashboard
a2enmod wsgi

# Disable default site (optional)
a2dissite 000-default

echo -e "${GREEN}✓ Apache configured${NC}"
echo ""

echo -e "${YELLOW}Step 7: Testing configuration...${NC}"
apache2ctl configtest
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Configuration test passed${NC}"
else
    echo -e "${RED}✗ Configuration test failed - please check errors${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}Step 8: Restarting Apache...${NC}"
systemctl restart apache2
systemctl status apache2 --no-pager
echo -e "${GREEN}✓ Apache restarted${NC}"
echo ""

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Your Steam Dashboard is now running!"
echo ""
echo "Access it at:"
echo "  - http://localhost"
echo "  - http://$(hostname -I | awk '{print $1}')"
echo ""
echo "Logs located at:"
echo "  - Error log: /var/log/apache2/steam-dashboard-error.log"
echo "  - Access log: /var/log/apache2/steam-dashboard-access.log"
echo ""
echo "To view logs:"
echo "  sudo tail -f /var/log/apache2/steam-dashboard-error.log"
echo ""
echo -e "${YELLOW}Note: If accessing from another machine, use the IP address shown above${NC}"
echo ""
