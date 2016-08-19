import logging
import os
import platform
import sys
from flask import Flask, render_template

# figure out this platform's temp dir
if platform.system() == 'Windows':
    temp_dir = os.environ['Temp'].replace('\\', '/')
    sys.stdout = open('{0}/neutronui.stdout.log'.format(temp_dir), 'w')
    sys.stderr = open('{0}/neutronui.stderr.log'.format(temp_dir), 'w')
else:
    temp_dir = '/tmp/'

log_handler = logging.FileHandler('{0}/neutronui.web.log'.format(temp_dir))
log_handler.setLevel(logging.DEBUG)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.logger.addHandler(log_handler)

os.environ['FLASK_DEBUG'] = "1"

@app.route("/")
def index():
    return render_template('index.html')
