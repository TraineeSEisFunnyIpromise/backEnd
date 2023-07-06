from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# instantiate the app
app = Flask(__name__)

if __name__ == '__main__':
    app.run()