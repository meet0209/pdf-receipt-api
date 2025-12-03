from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pdf_processor import extract_pdf_data
from receipt_parser import parse_receipt_data

app = Flask(__name__)
CORS(app)  # Enable CORS for chatbot platform

@app.route('/process-receipt', methods=['POST'])
def process_receipt():
    """
    Process uploaded PDF receipt and extract transaction data
    
    Expected: multipart/form-data with 'file' field containing PDF
    Returns: JSON with extracted receipt information
    """
    try:
        # Check if PDF file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided. Please upload a PDF receipt.'
            }), 400
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({
                'success': False,
                'error': f'Invalid file type: {file.filename}. Please send PDF only.'
            }), 400
        
        print(f"Processing file: {file.filename}")
        
        # Extract text from PDF
        extracted_text = extract_pdf_data(file)
        print(f"Extracted text length: {len(extracted_text)} characters")
        
        # Parse receipt information
        receipt_data = parse_receipt_data(extracted_text)
        
        # Return structured data to chatbot
        return jsonify({
            'success': True,
            'data': receipt_data,
            'message': 'Receipt processed successfully'
        }), 200
        
    except Exception as e:
        print(f"Error processing receipt: {str(e)}")
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
            '/process-receipt': 'POST - Process PDF receipt (multipart/form-data with file field)'
        },
        'usage': {
            'method': 'POST',
            'url': '/process-receipt',
            'content-type': 'multipart/form-data',
            'body': 'file: <PDF file>'
        }
    }), 200

if __name__ == '__main__':
    print("🚀 Starting PDF Receipt Processing API...")
    print("📍 API running at: http://localhost:5000")
    print("📚 Documentation: http://localhost:5000")
    print("💚 Health check: http://localhost:5000/health")
    print("\n⚡ Ready to process receipts!\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
