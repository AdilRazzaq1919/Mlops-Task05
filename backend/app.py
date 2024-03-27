from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
# Ensure the MongoDB URI includes your database name after the address
app.config["MONGO_URI"] = "mongodb+srv://adilrazzaq1919:adil1234@mlopstask05.frund.mongodb.net/yourDatabaseName?retryWrites=true&w=majority&appName=MlopsTask05"
mongo = PyMongo(app)

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/submit', methods=['POST'])
def submit():
    # Check if the MongoDB connection is successful
    if mongo.db is None:
        app.logger.debug("Failed to establish a connection with MongoDB")
        return jsonify({"error": "Connection to MongoDB was unsuccessful"}), 500
    
    if not request.is_json:
        app.logger.debug("Request Content-Type is not application/json")
        return jsonify({"error": "Request must be JSON"}), 415
    
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing name or email"}), 400
    
    mongo.db.submissions.insert_one(data)
    return jsonify({"message": "Success"}), 201

@app.route('/')
def test():
    # Test the connection and access to the database
    if mongo.db is None:
        return {"error": "Connection to MongoDB was unsuccessful"}

    try:
        collections = mongo.db.list_collection_names()
        return {"collections": collections}
    except Exception as e:
        app.logger.debug("Error accessing MongoDB: %s", str(e))
        return {"error": "Failed to access MongoDB"}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
