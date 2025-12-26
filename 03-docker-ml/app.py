from flask import Flask, request, jsonify
from transformers import pipeline
import redis
import json
import hashlib
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize Redis connection
redis_host = os.getenv('REDIS_HOST', 'redis')
logger.info(f"Redis host: {redis_host}")
redis_port = int(os.getenv('REDIS_PORT', 6379))
cache = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

try:
    logger.info(f"Redis connection successful: {cache.ping()}")
except Exception as e:
    logger.error(f"Redis connection failed: {str(e)}")

logger.info("Loading model...")
model = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')
logger.info("Model downloaded successfully")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        redis_status = 'connected' if cache.ping() else 'disconnected'
    except redis.ConnectionError:
        redis_status = 'disconnected'
        
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running',
        'redis': redis_status
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    question = data['question']
    context = data['context']
    
    # Create a unique cache key
    cache_key = hashlib.md5(f"{question}{context}".encode()).hexdigest()
    
    # Check cache
    try:
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for key: {cache_key}")
            return jsonify(json.loads(cached_result))
    except redis.ConnectionError:
        logger.error("Redis unavailable, skipping cache")

    # Run prediction
    logger.info("Cache miss - Running model prediction")
    result = model(question=question, context=context)
    
    # Save to cache (expire in 1 hour)
    try:
        cache.setex(cache_key, 3600, json.dumps(result))
    except redis.ConnectionError:
        logger.error("Failed to save to Redis cache")
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
