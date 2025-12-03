from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from io import BytesIO
from pdf_processor import extract_pdf_data
from receipt_parser import parse_receipt_data

app = Flask(__name__)
CORS(app)  # Enable CORS for chatbot platform

@app.route('/process-receipt', methods=['POST'])
def process_receipt():
    """
    Process PDF receipt - accepts either file upload OR file URL
    
    Expected:
    - multipart/form-data with 'file' field (file upload), OR
    - form data with 'file_url' field (URL to PDF file)
    
    Returns: JSON with extracted receipt information
    """
    try:
        file_obj = None
        
        # Option 1: Check if file URL is provided (for chatbot platforms that send URLs)
        file_url = request.form.get('file_url') or (request.json.get('file_url') if request.is_json else None)
        
        if file_url:
            print(f"📥 Downloading PDF from URL: {file_url}")
            
            # Download the file from URL
            response = requests.get(file_url, timeout=30)
            if response.status_code != 200:
                return jsonify({
                    'success': False,
                    'error': f'Failed to download file from URL (status {response.status_code})'
                }), 400
            
            # Create file-like object from downloaded content
            file_obj = BytesIO(response.content)
            print(f"✅ Downloaded {len(response.content)} bytes")
        
        # Option 2: Check if file is directly uploaded
        elif 'file' in request.files:
            file_obj = request.files['file']
            
            # Check if file was actually selected
            if file_obj.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400
            
            # Validate file type
            if not file_obj.filename.lower().endswith('.pdf'):
                return jsonify({
                    'success': False,
                    'error': f'Invalid file type: {file_obj.filename}. Please send PDF only.'
                }), 400
            
            print(f"📄 Processing uploaded file: {file_obj.filename}")
        
        else:
            return jsonify({
                'success': False,
                'error': 'No file provided. Send either "file" (file upload) or "file_url" (URL to PDF)'
            }), 400
        
        # Extract text from PDF
        extracted_text = extract_pdf_data(file_obj)
        print(f"✅ Extracted text length: {len(extracted_text)} characters")
        
        # Parse receipt information
        receipt_data = parse_receipt_data(extracted_text)
        
        # Return structured data to chatbot
        return jsonify({
            'success': True,
            'data': receipt_data,
            'message': 'Receipt processed successfully'
        }), 200
        
    except Exception as e:
        print(f"❌ Error processing receipt: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to process receipt: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PDF Receipt Processing API',
        'version': '1.0.0'
    }), 200

@app.route('/', methods=['GET'])
def index():
    """API documentation endpoint"""
    return jsonify({
        'service': 'PDF Receipt Processing API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'This documentation',
            '/health': 'Health check endpoint',
            '/process-receipt': 'POST - Process PDF receipt'
        },
        'usage': {
            'method': 'POST',
            'url': '/process-receipt',
            'options': [
                {'content-type': 'multipart/form-data', 'body': 'file: <PDF file>'},
                {'content-type': 'application/x-www-form-urlencoded', 'body': 'file_url: <URL to PDF>'}
            ]
        }
    }), 200

if __name__ == '__main__':
    print("🚀 Starting PDF Receipt Processing API...")
    print("📍 API running at: http://localhost:5000")
    print("📚 Documentation: http://localhost:5000")
    print("💚 Health check: http://localhost:5000/health")
    print("\n⚡ Ready to process receipts (file upload OR file URL)!\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
