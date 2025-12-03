"""
Quick test script for the PDF Receipt Processing API
Run this after starting the API with: python app.py
"""

import requests
import os

API_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_docs():
    """Test the API documentation endpoint"""
    print("\n📚 Testing API documentation endpoint...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_process_receipt(pdf_path):
    """Test the receipt processing endpoint"""
    print(f"\n📄 Testing receipt processing with: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return False
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/process-receipt", files=files)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print("\n✅ Receipt processed successfully!")
            print("\n📊 Extracted Data:")
            data = result.get('data', {})
            print(f"   Bank: {data.get('bank')}")
            print(f"   Transaction ID: {data.get('transaction_id')}")
            print(f"   Amount: RM {data.get('amount')}")
            print(f"   Date: {data.get('date')}")
            print(f"   Time: {data.get('time')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"\n❌ Processing failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_file():
    """Test with invalid file type"""
    print("\n⚠️ Testing with invalid file (should fail gracefully)...")
    try:
        # Create a temporary text file
        test_file = "test.txt"
        with open(test_file, 'w') as f:
            f.write("This is not a PDF")
        
        with open(test_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/process-receipt", files=files)
        
        os.remove(test_file)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if not result.get('success'):
            print(f"✅ Correctly rejected invalid file: {result.get('error')}")
            return True
        else:
            print("❌ Should have rejected non-PDF file")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("PDF Receipt Processing API - Test Suite")
    print("=" * 60)
    print(f"Testing API at: {API_URL}")
    
    # Test 1: Health Check
    test1 = test_health_check()
    
    # Test 2: API Documentation
    test2 = test_api_docs()
    
    # Test 3: Invalid file
    test3 = test_invalid_file()
    
    # Test 4: Process actual PDF (if available)
    print("\n" + "=" * 60)
    pdf_path = input("\nEnter path to a test PDF receipt (or press Enter to skip): ").strip()
    test4 = True
    if pdf_path:
        test4 = test_process_receipt(pdf_path)
    else:
        print("⏭️ Skipping PDF test")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Health Check: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"  API Docs: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"  Invalid File: {'✅ PASS' if test3 else '❌ FAIL'}")
    print(f"  PDF Processing: {'✅ PASS' if test4 else '⏭️ SKIPPED' if not pdf_path else '❌ FAIL'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
