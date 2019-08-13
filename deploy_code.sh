#! /bin/bash

# Gather all static files to the static0 directory for production nginx

echo "Gathering all static files..."
source /home/djr/python-env/recipelab/bin/activate
python /home/djr/recipelab/recipelab/manage.py collectstatic --noinput

# Push code to server
# Assumes password-less ssh access

echo "Setting DEBUG = False for Production..."
sed -i 's/DEBUG = True/DEBUG = False/' /home/djr/recipelab/recipelab/recipelab/settings.py

echo "Rsync'ing code on server..."
rsync -azhv --delete /home/djr/recipelab/recipelab -e 'ssh -p 53' djr@recipelab.org:/home/djr/recipelab/

echo "Setting DEBUG = True for Dev..."
sed -i 's/DEBUG = False/DEBUG = True/' /home/djr/recipelab/recipelab/recipelab/settings.py

echo "Done."
