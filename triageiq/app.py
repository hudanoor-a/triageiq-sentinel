import joblib
from flask import Flask, request, jsonify
from textblob import TextBlob
import os


app = Flask(__name__)

MODEL_PATH = os.getenv('MODEL_PATH', 'triageiq/models/triage_model.joblib')
model = joblib.load(MODEL_PATH)


def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/triage', methods=['POST'])
def triage():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    ticket_text = data['text'].strip().lower()

    if not ticket_text:
        return jsonify({'error': 'Empty ticket text'}), 400

    category = model['category'].predict([ticket_text])[0]
    priority = model['priority'].predict([ticket_text])[0]
    sentiment = get_sentiment(ticket_text)

    return jsonify({
        'category': category,
        'priority': priority,
        'sentiment': sentiment
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
