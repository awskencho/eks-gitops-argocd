from flask import Flask, render_template, request, jsonify
import boto3
import uuid
import os

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-west-2'))
table = dynamodb.Table(os.getenv('TABLE_NAME', 'notes'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    response = table.scan()
    return jsonify(response.get('Items', []))

@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.json
    item = {'id': str(uuid.uuid4()), 'title': data['title'], 'content': data['content']}
    table.put_item(Item=item)
    return jsonify(item), 201

@app.route('/api/notes/<id>', methods=['DELETE'])
def delete_note(id):
    table.delete_item(Key={'id': id})
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
