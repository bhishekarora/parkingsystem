from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route('/ams', methods=['POST'])
def receive_tail_number():
    data = request.get_json()
    tail_number = data.get('tail_number', None)
    if tail_number:
        print(f"Received tail number: {tail_number}, hangar charges started")
        return jsonify({"status": "success", "message": "Tail number received"}), 200
    else:
        return jsonify({"status": "error", "message": "No tail number provided"}), 400

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    print("AMS interface listening for Tail no")
    app.run(host='0.0.0.0', port=5000, debug=False)
