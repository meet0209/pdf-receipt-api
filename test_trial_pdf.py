"""
Quick test script to process trial.pdf
"""
import requests
import os

# Path to your trial.pdf
PDF_PATH = r"c:\Users\Meet\.gemini\trial.pdf"
API_URL = "http://localhost:5000/process-receipt"

def test_trial_pdf():
    """Test the API with trial.pdf"""
    
    print("=" * 60)
    print("Testing PDF Receipt API with trial.pdf")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(PDF_PATH):
        print(f"❌ File not found: {PDF_PATH}")
        return
    
    print(f"📄 Found file: {PDF_PATH}")
    print(f"📏 File size: {os.path.getsize(PDF_PATH)} bytes")
    print()
    
    # Test the API
    print("🔄 Sending to API...")
    try:
        with open(PDF_PATH, 'rb') as f:
            response = requests.post(API_URL, files={'file': f})
        
        print(f"✅ Response received (Status: {response.status_code})")
        print()
        
        # Parse response
        result = response.json()
        
        if result.get('success'):
            print("🎉 SUCCESS! Receipt processed successfully!")
            print()
            print("📊 EXTRACTED DATA:")
            print("-" * 60)
            
            data = result.get('data', {})
            print(f"  🏦 Bank:           {data.get('bank') or 'Not detected'}")
            print(f"  🆔 Transaction ID: {data.get('transaction_id') or 'Not found'}")
            print(f"  💰 Amount:         RM {data.get('amount') or 'Not found'}")
            print(f"  📅 Date:           {data.get('date') or 'Not found'}")
            print(f"  ⏰ Time:           {data.get('time') or 'Not found'}")
            print(f"  📝 Status:         {data.get('status') or 'Unknown'}")
            print(f"  📤 From Account:   {data.get('sender_account') or 'Not found'}")
            print(f"  📥 To Account:     {data.get('receiver_account') or 'Not found'}")
            print("-" * 60)
            
            # Show raw text snippet
            if data.get('raw_text'):
                print()
                print("📄 First 300 characters of extracted text:")
                print("-" * 60)
                print(data.get('raw_text')[:300])
                print("-" * 60)
            
        else:
            print(f"❌ FAILED: {result.get('error')}")
            print()
            print("💡 Possible reasons:")
            print("   - PDF might be scanned/image-based (needs OCR)")
            print("   - PDF format not recognized")
            print("   - File corrupted")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to API")
        print()
        print("💡 Make sure the API is running:")
        print("   1. Open another terminal")
        print("   2. Run: start_api.bat")
        print("   3. Wait for 'Ready to process receipts!'")
        print("   4. Then run this script again")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_trial_pdf()
