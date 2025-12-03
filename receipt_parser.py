import re
from datetime import datetime

def parse_receipt_data(text):
    """
    Parse receipt text to extract structured transaction data
    
    Args:
        text (str): Extracted text from PDF receipt
        
    Returns:
        dict: Structured receipt information including:
            - transaction_id: Transaction reference number
            - amount: Transaction amount (float)
            - date: Transaction date
            - time: Transaction time
            - sender_account: Sender account number
            - receiver_account: Receiver account number
            - bank: Bank name
            - status: Transaction status
            - raw_text: Original extracted text (first 500 chars)
    """
    
    # Initialize result
    result = {
        'transaction_id': None,
        'amount': None,
        'date': None,
        'time': None,
        'sender_account': None,
        'receiver_account': None,
        'bank': None,
        'status': None,
        'raw_text': text[:500] if text else None  # First 500 chars for debugging
    }
    
    print("🔍 Parsing receipt data...")
    
    # === BANK DETECTION ===
    banks = [
        'Maybank', 'CIMB', 'Public Bank', 'RHB', 'Hong Leong', 
        'AmBank', 'Bank Islam', 'HSBC', 'Standard Chartered',
        'Alliance Bank', 'Affin Bank', 'UOB', 'OCBC'
    ]
    
    for bank in banks:
        if bank.lower() in text.lower():
            result['bank'] = bank
            print(f"✅ Bank detected: {bank}")
            break
    
    # === TRANSACTION ID EXTRACTION ===
    # Pattern: M2U_20251203_0937 or 290121492M or REF: 1234567890
    trans_id_patterns = [
        r'M2U_\d+_\d+',  # Maybank M2U format
        r'\b\d{9,12}[A-Z]\b',  # Maybank format: 290121492M (9-12 digits + letter)
        r'(?:REF|Reference|Reference ID)[:\s]+([A-Z0-9-]+)',
        r'Transaction\s+(?:No|Number|ID)[:\s]+([A-Z0-9-]+)',
        r'Receipt\s+(?:No|Number)[:\s]+([A-Z0-9-]+)'
    ]
    
    for pattern in trans_id_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if 'M2U' in pattern or r'\b\d{9,12}[A-Z]\b' == pattern:
                result['transaction_id'] = match.group(0)
            else:
                result['transaction_id'] = match.group(1)
            print(f"✅ Transaction ID: {result['transaction_id']}")
            break
    
    # === AMOUNT EXTRACTION ===
    # Pattern: RM 100.00 or RM100.00 or MYR 100 or Amount: 100.00
    # Handle cases where "Amount" and "RM 100.00" are on separate lines
    amount_patterns = [
        r'Amount[:\s]*\n?\s*RM\s*(\d+(?:[,.]\d+)*(?:\.\d{2})?)',  # Amount\nRM 100.00
        r'RM\s*(\d+(?:[,.]\d+)*(?:\.\d{2})?)',  # RM 100.00 or RM100.00
        r'MYR\s*(\d+(?:[,.]\d+)*(?:\.\d{2})?)',  # MYR 100.00
        r'Total[:\s]+RM\s*(\d+(?:[,.]\d+)*(?:\.\d{2})?)',  # Total: RM 100.00
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            # Clean amount (remove commas, keep dots for decimals)
            amount_str = match.group(1).replace(',', '')
            try:
                amount_value = float(amount_str)
                # Store as float, but ensure 2 decimal places
                result['amount'] = round(amount_value, 2)
                print(f"✅ Amount: RM {result['amount']:.2f}")
                break
            except ValueError:
                continue
    
    # === DATE EXTRACTION ===
    # Pattern: 03/12/2025 or 2025-12-03 or 03 Dec 2025 or 03-Dec-2025
    date_patterns = [
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # 03/12/2025 or 03-12-2025
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',    # 2025-12-03
        r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})',  # 03 Dec 2025
        r'(\d{1,2}[-](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d{4})'  # 03-Dec-2025
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['date'] = match.group(1)
            print(f"✅ Date: {result['date']}")
            break
    
    # === TIME EXTRACTION ===
    # Pattern: 09:37:45 or 09:37 AM or 21:30
    time_patterns = [
        r'(\d{1,2}:\d{2}:\d{2})',  # 09:37:45
        r'(\d{1,2}:\d{2}\s*[AP]M)',  # 09:37 AM
        r'Time[:\s]+(\d{1,2}:\d{2}(?::\d{2})?)'  # Time: 09:37
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['time'] = match.group(1)
            print(f"✅ Time: {result['time']}")
            break
    
    # === ACCOUNT NUMBER EXTRACTION ===
    # Look for beneficiary account number (often has spaces like "5641 9177 5091")
    beneficiary_pattern = r'Beneficiary account number[:\s]*\n?\s*(\d{4}\s*\d{4}\s*\d{4}|\d{10,16})'
    beneficiary_match = re.search(beneficiary_pattern, text, re.IGNORECASE | re.MULTILINE)
    
    if beneficiary_match:
        # Remove spaces from account number
        account = beneficiary_match.group(1).replace(' ', '')
        result['receiver_account'] = account
        print(f"✅ Beneficiary account: {account}")
    else:
        # Fallback: Look for any account numbers (10-16 digits, may have spaces)
        # First try to find space-separated format
        space_accounts = re.findall(r'\b\d{4}\s+\d{3,4}\s+\d{4}\b', text)
        if space_accounts:
            result['receiver_account'] = space_accounts[0].replace(' ', '')
            print(f"✅ Account found: {result['receiver_account']}")
        else:
            # Try continuous digits
            accounts = re.findall(r'\b\d{10,16}\b', text)
            # Filter out company registration numbers and dates
            valid_accounts = [acc for acc in accounts if not ('196' in acc or '200' in acc)]
            if valid_accounts:
                result['receiver_account'] = valid_accounts[0]
                print(f"✅ Account found: {result['receiver_account']}")
    
    # === STATUS DETECTION ===
    success_keywords = ['successful', 'completed', 'approved', 'success', 'paid']
    failed_keywords = ['failed', 'rejected', 'declined', 'cancelled']
    pending_keywords = ['pending', 'processing', 'waiting']
    
    text_lower = text.lower()
    
    for keyword in success_keywords:
        if keyword in text_lower:
            result['status'] = 'successful'
            print(f"✅ Status: successful (keyword: {keyword})")
            break
    
    if not result['status']:
        for keyword in failed_keywords:
            if keyword in text_lower:
                result['status'] = 'failed'
                print(f"❌ Status: failed (keyword: {keyword})")
                break
    
    if not result['status']:
        for keyword in pending_keywords:
            if keyword in text_lower:
                result['status'] = 'pending'
                print(f"⏳ Status: pending (keyword: {keyword})")
                break
    
    # Default to successful if amount is present
    if not result['status'] and result['amount']:
        result['status'] = 'successful'
        print("✅ Status: successful (default, amount present)")
    
    # === SUMMARY ===
    print("\n📊 Parsing Results:")
    print(f"   Bank: {result['bank']}")
    print(f"   Transaction ID: {result['transaction_id']}")
    if result['amount'] is not None:
        print(f"   Amount: RM {result['amount']:.2f}")
    else:
        print(f"   Amount: RM {result['amount']}")
    print(f"   Date: {result['date']}")
    print(f"   Time: {result['time']}")
    print(f"   Status: {result['status']}")
    
    return result
