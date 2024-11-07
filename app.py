from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for simplicity
POSTS_FILE = 'posts.json'

# Helper function to load posts from a file
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

# Helper function to save posts to a file
def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

@app.route("/")
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
    posts = load_posts()
    posts.append(post)
    save_posts(posts)

    return jsonify({"status": "success", "post": post})

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = load_posts()
    return jsonify(posts)

if __name__ == "__main__":
    app.run(debug=True)
