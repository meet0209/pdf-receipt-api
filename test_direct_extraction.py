"""
Direct PDF text extraction test for trial.pdf
This will show what text can be extracted from the PDF
"""
import sys
sys.path.insert(0, r'c:\Users\Meet\.gemini\pdf-receipt-api')

from pdf_processor import extract_pdf_data
from receipt_parser import parse_receipt_data

PDF_PATH = r"c:\Users\Meet\.gemini\trial.pdf"

def test_extraction():
    print("=" * 70)
    print("DIRECT PDF TEXT EXTRACTION TEST")
    print("=" * 70)
    print(f"\n📄 Testing: {PDF_PATH}\n")
    
    try:
        # Open the PDF file
        with open(PDF_PATH, 'rb') as f:
            print("🔍 Extracting text from PDF...")
            text = extract_pdf_data(f)
            
            print(f"\n✅ Extraction successful!")
            print(f"📏 Total text length: {len(text)} characters\n")
            
            print("=" * 70)
            print("EXTRACTED TEXT:")
            print("=" * 70)
            print(text)
            print("=" * 70)
            
            # Now parse it
            print("\n🔬 Parsing receipt data...")
            data = parse_receipt_data(text)
            
            print("\n" + "=" * 70)
            print("PARSED DATA:")
            print("=" * 70)
            print(f"  Bank:           {data.get('bank')}")
            print(f"  Transaction ID: {data.get('transaction_id')}")
            if data.get('amount') is not None:
                print(f"  Amount:         RM {data.get('amount'):.2f}")
            else:
                print(f"  Amount:         Not found")
            print(f"  Date:           {data.get('date')}")
            print(f"  Time:           {data.get('time')}")
            print(f"  Status:         {data.get('status')}")
            print(f"  From Account:   {data.get('sender_account')}")
            print(f"  To Account:     {data.get('receiver_account')}")
            print("=" * 70)
            
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {PDF_PATH}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extraction()
