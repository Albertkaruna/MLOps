from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running'
    }), 200


@app.route('/api/process', methods=['POST'])
def process_data():
    """Process POST data and return a response"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Please send JSON data in the request body'
            }), 400

        name = data.get('name', 'Guest')
        id = data.get('id', '')
        
        # Process and return response based on input
        response = {
            'status': 'success',
            'message': f'Hello {name}! Received your data. Account number for this ID {id} is your birth date in DDMMYYYY format.',
            'received_data': data
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

