import os
import boto3
import json
from flask import Flask, request, render_template, jsonify

application = Flask(__name__)

# Configure AWS credentials and region
region = 'us-east-2'  # Make sure this matches your SageMaker endpoint region
runtime = boto3.client('sagemaker-runtime', region_name=region)
endpoint_name = 'fake-news-lstm-endpoint'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
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
    application.run(debug=True, host='0.0.0.0', port=8080)
