import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/main')
def main():
    return jsonify(message="Hello from the serverless function!")

if __name__ == "__main__":
    app.run()
