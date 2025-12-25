from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

print("Loading model...")
model = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')
print("Model downloaded successfully")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running'
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    result = model(question=data['question'], context=data['context'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
