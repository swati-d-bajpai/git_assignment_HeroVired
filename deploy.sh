#!/bin/bash

set -e

REPO_PATH="/mnt/c/Users/Admin/Documents/GitHub/python/gitassignment/git_assignment_HeroVired"
DEPLOY_DIR="/var/www/html"

echo "[`date`] Starting deployment..." >> deploy.log

# Replace HTML file
sudo cp $REPO_PATH/index.html $DEPLOY_DIR/

# Reload Nginx (optional)
sudo systemctl reload nginx

echo "[`date`] Deployment complete." >> deploy.log
