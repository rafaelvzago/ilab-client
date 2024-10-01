from flask import Flask, render_template_string, request, jsonify
import os
import requests

app = Flask(__name__)

# Retrieve the address from an environment variable, defaulting to 'http://127.0.0.1:8000' if not set
ADDRESS = os.environ.get('ADDRESS', 'http://127.0.0.1:8000')

# HTML template for the form
FORM_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ask a Question</title>
</head>
<body>
    <h1>Ask a Question</h1>
    <form method="post">
        <label for="question">Enter your question:</label><br>
        <textarea id="question" name="question" rows="4" cols="80" required></textarea><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
'''

# HTML template for displaying the response
RESPONSE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Response</title>
</head>
<body>
    <h1>Response:</h1>
    <p>{{ response }}</p>
    <a href="/">Ask another question</a>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        
        if not question:
            return render_template_string(FORM_HTML + '<p style="color:red;">Please enter a question.</p>')

        url = f'{ADDRESS}/v1/completions'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "prompt": f"\n\n### Instructions:\n{question}\n\n### Response:\n",
            "stop": [
                "\n",
                "###"
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raises HTTPError if one occurred.
            result = response.json()

            # Extract the 'text' field from the first choice
            response_text = result.get('choices', [{}])[0].get('text', 'No response available.')

            # Optionally, you can strip leading/trailing whitespace
            response_text = response_text.strip()

            return render_template_string(RESPONSE_HTML, response=response_text)
        except requests.exceptions.RequestException as e:
            error_message = f'An error occurred: {str(e)}'
            return render_template_string(RESPONSE_HTML, response=error_message), 500
        except (ValueError, KeyError, IndexError) as e:
            # Handle cases where the expected fields are not in the response
            error_message = f'Unexpected response format: {str(e)}'
            return render_template_string(RESPONSE_HTML, response=error_message), 500

    # GET request renders the form
    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    # Set debug=True for development. In production, use a WSGI server like Gunicorn.
    app.run(host='0.0.0.0', port=5000, debug=True)

