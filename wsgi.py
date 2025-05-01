import sys
import os

# Set the path to your project folder
project_home = '/home/CaptainSpatula/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Tell PythonAnywhere where your Flask app is
from app import app as application  # or use 'from flask_app import app as application' if your file is named flask_app.py
