#!/bin/bash

# Generate the site in the project directory
python3 project/src/main.py "/StaticSiteGenerator/"

# Create docs directory at the root if it doesn't exist
mkdir -p docs

# Copy everything from project/docs to the root docs directory
cp -r project/docs/* docs/

# Add .nojekyll file to prevent Jekyll processing 
touch docs/.nojekyll

echo "Site built and copied to repository root docs directory"