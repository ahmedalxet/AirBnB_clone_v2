#!/usr/bin/env bash
# This script sets up the web servers for the deployment of web_static.

# Install Nginx if it not already installed
if ! which nginx > /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create the necessary directories if they don't already exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file in /data/web_static/releases/test
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link to /data/web_static/releases/test/
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '/listen 80 default_server/a location /hbnb_static {\n\talias /data/web_static/current/;\n}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
