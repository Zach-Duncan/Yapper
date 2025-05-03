import sys

# Set the path to your project folder
project_home = '/home/CaptainSpatula/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Tell PythonAnywhere where your Flask app is
from app import app as application