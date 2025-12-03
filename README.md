# PDF Receipt Processing API

API service to extract and parse transaction data from PDF receipts for chatbot integration.

## Features

- ✅ Extract text from PDF receipts
- ✅ Parse Malaysian bank transaction details (Maybank, CIMB, Public Bank, etc.)
- ✅ Extract: Transaction ID, Amount, Date, Time, Bank name, Status
- ✅ RESTful API with JSON responses
- ✅ CORS enabled for chatbot integration
- ✅ Multiple PDF extraction methods (pdfplumber + PyPDF2)

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Run the API

```bash
python app.py
```

The API will start at: `http://localhost:5000`

### 3. Test the API

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Process Receipt:**
```bash
curl -X POST http://localhost:5000/process-receipt -F "file=@receipt.pdf"
```

## API Endpoints

### `GET /`
API documentation and usage information

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "PDF Receipt Processing API",
  "version": "1.0.0"
}
```

### `POST /process-receipt`
Process PDF receipt and extract transaction data

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` field with PDF file

**Success Response (200):**
```json
{
  "success": true,
  "message": "Receipt processed successfully",
  "data": {
    "transaction_id": "M2U_20251203_0937",
    "amount": 100.0,
    "date": "03/12/2025",
    "time": "09:37",
    "bank": "Maybank",
    "status": "successful",
    "sender_account": null,
    "receiver_account": null,
    "raw_text": "First 500 chars of extracted text..."
  }
}
```

**Error Response (400/500):**
```json
{
  "success": false,
  "error": "Error message here"
}
```

## Chatbot Integration

### Step 1: Add Condition to Detect PDF
```
Condition: {{last_user_message}} contains ".pdf"
True → Route to PDF processing
False → Continue with image processing
```

### Step 2: Configure External API Request
```
Button: Actions → External API Request

Method: POST
URL: http://your-api-url.com/process-receipt
Content-Type: multipart/form-data
Body: file = {{last_user_attachment}}

Save response to: receipt_data
```

### Step 3: Process Response
```
Use variables in next messages:
- {{receipt_data.data.amount}}
- {{receipt_data.data.transaction_id}}
- {{receipt_data.data.date}}
- {{receipt_data.data.bank}}
- {{receipt_data.data.status}}
```

### Step 4: Validate Payment
```
Condition: {{receipt_data.data.amount}} equals "100"

True → Add Tag: payment_verified
      → Send: "✅ Payment of RM100 confirmed!"
      
False → Send: "❌ Amount mismatch. Expected RM100, received RM{{receipt_data.data.amount}}"
```

## Supported Banks

- Maybank (M2U)
- CIMB Bank
- Public Bank
- RHB Bank
- Hong Leong Bank
- AmBank
- Bank Islam
- HSBC
- Standard Chartered
- Alliance Bank
- Affin Bank
- UOB
- OCBC

## Project Structure

```
pdf-receipt-api/
├── app.py              # Main Flask API
├── pdf_processor.py    # PDF text extraction
├── receipt_parser.py   # Transaction data parser
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Testing with Python

```python
import requests

# Test with local file
with open('receipt.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/process-receipt',
        files={'file': f}
    )
    print(response.json())
```

## Deployment

See `pdf_receipt_processing_solution.md` for deployment options:
- Render.com (Free tier)
- Railway.app
- Google Cloud Run
- PythonAnywhere

## Troubleshooting

**Issue: "Could not extract text from PDF"**
- The PDF might be image-based (scanned). You'll need to add OCR support with pytesseract.

**Issue: "No amount found"**
- Check the PDF format. The parser looks for "RM" or "MYR" followed by numbers.
- You may need to adjust regex patterns in `receipt_parser.py` for your specific bank format.

**Issue: CORS errors**
- CORS is enabled by default. Check if the chatbot platform requires specific headers.

## Next Steps

1. ✅ Test with your actual receipt PDFs
2. 📝 Adjust regex patterns based on your bank's format
3. 🚀 Deploy to cloud hosting
4. 🔗 Integrate with chatbot External API Request
5. ✨ Add OCR support for scanned PDFs (optional)

## License

Created for chatbot PDF receipt processing integration.
