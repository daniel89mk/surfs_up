# 1. import flask
from flask import Flask

# 2. Create a server
# localhost:5000 -> flask?
# localhost:5432 -> postgres
# localhost:8888 -> jupyter
app = Flask(__name__)

# 3. Define a route (here: home)
@app.route('/')
def hello_world():
    return 'Hello world'