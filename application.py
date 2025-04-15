from flask import Flask, request, render_template, jsonify
import boto3
import json

application = Flask(__name__)  # Change from app to application

# Configure AWS region
region = 'us-east-2'
runtime = boto3.client('sagemaker-runtime', region_name=region)
endpoint_name = 'fake-news-lstm-endpoint'

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text')
    payload = json.dumps({'text': text})
    
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=payload
    )
    
    result = json.loads(response['Body'].read().decode())
    return jsonify(result)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000)
