# Quick Start Guide

## 🚀 Start the API

```bash
# Navigate to project directory
cd c:\Users\Meet\.gemini\pdf-receipt-api

# Activate virtual environment
.\venv\Scripts\activate

# Run the API
python app.py
```

The API will be available at: **http://localhost:5000**

---

## 🧪 Test the API

### Option 1: Use the Test Script
```bash
python test_api.py
```

### Option 2: Test with curl
```bash
# Health check
curl http://localhost:5000/health

# Process a receipt
curl -X POST http://localhost:5000/process-receipt -F "file=@your_receipt.pdf"
```

### Option 3: Test with Browser
Open in browser: http://localhost:5000

---

## 📋 Next Steps

1. **Test with your actual PDF receipt**
   - Place a receipt PDF in the project folder
   - Run: `python test_api.py`
   - Enter the PDF filename when prompted

2. **Check the extracted data**
   - Verify transaction ID, amount, date are correct
   - If parsing fails, you may need to adjust regex patterns in `receipt_parser.py`

3. **Deploy the API**
   - See `README.md` for deployment options (Render, Railway, etc.)

4. **Integrate with chatbot**
   - Use the External API Request button
   - Point to your deployed API URL
   - Map response fields to chatbot variables

---

## 🔧 Troubleshooting

**Dependencies not installing?**
```bash
# Make sure you're in the virtual environment
.\venv\Scripts\activate

# Upgrade pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

**API not starting?**
```bash
# Check if port 5000 is already in use
netstat -ano | findstr :5000

# Try a different port (edit app.py line 63)
app.run(host='0.0.0.0', port=8000, debug=True)
```

**PDF text extraction failing?**
- Your PDF might be scanned (image-based)
- You'll need OCR support (pytesseract + Tesseract)
- See the full solution document for OCR setup
