from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for simplicity
POSTS_FILE = 'posts.json'
SHOUTOUTS_FILE = 'shoutouts.json'

# Helper function to load posts or shoutouts from a file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

# Helper function to save posts or shoutouts to a file
def save_data(data, file_path):
    with open(file_path, 'w') as f:
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
        "timestamp": datetime.now().isoformat()
    }

    # Load existing posts, append new post, and save posts
    posts = load_data(POSTS_FILE)
    posts.append(post)
    save_data(posts, POSTS_FILE)

    return jsonify({"status": "success", "post": post})

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = load_data(POSTS_FILE)
    return jsonify(posts)

@app.route('/shoutouts', methods=['GET'])
def shoutouts():
    return render_template("shoutouts.html")

@app.route('/shoutout', methods=['POST'])
def post_shoutout():
    data = request.json
    shoutout = {
        "giver": data['giver'],       # Name of the person giving the shoutout
        "recipient": data['recipient'], # Name of the person receiving the shoutout
        "message": data['message'],
        "timestamp": datetime.now().isoformat()
    }

    # Load existing posts, append new post, and save posts
    shoutouts = load_data(SHOUTOUTS_FILE)
    shoutouts.append(shoutout)
    save_data(shoutouts, SHOUTOUTS_FILE)

    return jsonify({"status": "success", "post": shoutout})

@app.route('/get_shoutouts', methods=['GET'])
def get_shoutouts():
    shoutouts = load_data(SHOUTOUTS_FILE)
    return jsonify(shoutouts)

if __name__ == "__main__":
    app.run(debug=True)
