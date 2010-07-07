#!/bin/sh
echo "Creating Comments for the API Reference..."

echo "> ../elements.html"
#python add_comment.py elements.html > ../elements.html

echo "> ../add.html"
#python add_comment.py add.html > ../add.html

echo "> ../callbacks.html"
#python add_comment.py callbacks.html > ../callbacks.html

echo "> ../manual.html"
python add_comment.py manual.html > ../manual.html

