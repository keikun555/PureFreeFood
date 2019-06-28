#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/button', methods=['POST'])
def reserve_button():
    print(request.data)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0')