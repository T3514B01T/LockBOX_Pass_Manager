# Flask web service code
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/save_password', methods=['POST'])
def save_password():
    # Extract data from the request
    data = request.json
    website = data.get('website')
    username = data.get('username')
    password = data.get('password')

    # Call your existing save_password function
    # Consider using Flask-SQLAlchemy or another database to store passwords securely

    return jsonify({"message": "Password saved successfully!"})

@app.route('/retrieve_password', methods=['POST'])
def retrieve_password():
    # Extract data from the request
    data = request.json
    website = data.get('website')

    # Call your existing retrieve_password function

    return jsonify({"message": "Password retrieved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
