from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for simplicity
POSTS_FILE = 'posts.json'
SHOUTOUTS_FILE = 'shoutouts.json'

# Helper function to load posts from a file
def load_posts(filename=POSTS_FILE):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

# Helper function to save posts to a file
def save_posts(data, filename=POSTS_FILE):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/post', methods=['POST'])
def post_update():
    data = request.json
    post = {
        "username": data['username'],
        "message": data['message'],
        # "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        "timestamp": datetime.now().isoformat()
    }

    # Load existing posts, append new post, and save posts
    posts = load_posts(POSTS_FILE)
    posts.append(post)
    save_posts(posts, POSTS_FILE)

    return jsonify({"status": "success", "post": post})

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = load_posts(POSTS_FILE)
    return jsonify(posts)

@app.route('/shoutout-page', methods=['GET'])
def shoutouts():
    return render_template("shoutouts.html")

@app.route('/shoutout', methods=['POST'])
def shoutout_update():
    data = request.json
    shoutout = {
        "name": data['name'],
        "username": data['username'],
        "message": data['message'],
        "timestamp": datetime.now().isoformat()
    }

    # Load existing posts, append new post, and save posts
    shoutouts = load_posts(SHOUTOUTS_FILE)
    shoutouts.append(shoutout)
    save_posts(shoutouts, SHOUTOUTS_FILE)

    return jsonify({"status": "success", "post": shoutout})

@app.route('/shoutouts', methods=['GET'])
def get_shoutouts():
    shoutouts = load_posts(SHOUTOUTS_FILE)
    return jsonify(shoutouts)

if __name__ == "__main__":
    app.run(debug=True)
