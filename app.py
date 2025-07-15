from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Function to ensure ADDRESS includes a scheme
def ensure_scheme(address):
    if not address.startswith(('http://', 'https://')):
        return 'http://' + address
    return address

# Retrieve the address from an environment variable, defaulting to 'http://127.0.0.1:8000' if not set
ADDRESS = ensure_scheme(os.environ.get('ADDRESS', 'http://127.0.0.1:8000'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/backend-status', methods=['GET'])
def backend_status():
    try:
        # Try to reach the backend service
        url = f'{ADDRESS}/v1/completions'
        response = requests.get(ADDRESS, timeout=5)
        # If we get any response (even 404), the service is reachable
        return jsonify({
            'status': 'online',
            'address': ADDRESS
        })
    except requests.exceptions.RequestException:
        return jsonify({
            'status': 'offline',
            'address': ADDRESS
        })

@app.route('/api/completions', methods=['POST'])
def completions():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Invalid request. "question" is required.'}), 400

    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'Please enter a question.'}), 400

    url = f'{ADDRESS}/v1/completions'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "prompt": f"\n\n### Instructions:\n{question}\n\n### Response:\n",
        "stop": [
            "###"
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=600)
        response.raise_for_status()  # Raises HTTPError if one occurred.
        result = response.json()

        # Extract the 'text' field from the first choice
        response_text = result.get('choices', [{}])[0].get('text', 'No response available.')
        response_text = response_text.strip()

        return jsonify({'response': response_text})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    except (ValueError, KeyError, IndexError) as e:
        return jsonify({'error': f'Unexpected response format: {str(e)}'}), 500

if __name__ == '__main__':
    # Set debug=True for development. In production, use a WSGI server like Gunicorn.
    app.run(host='0.0.0.0', port=5000, debug=True)

