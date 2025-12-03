"""
Create a simple text-based PDF for testing
This creates a mock receipt PDF that can be used to test the API
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def create_sample_receipt():
    """Create a sample Maybank receipt PDF for testing"""
    
    filename = "sample_receipt.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "MAYBANK2U")
    
    # Receipt Header
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Online Banking Receipt")
    c.drawString(100, 700, "=" * 50)
    
    # Transaction Details
    y = 670
    c.drawString(100, y, "Transaction Type: DuitNow Transfer")
    y -= 25
    c.drawString(100, y, "Transaction ID: M2U_20251203_0937")
    y -= 25
    c.drawString(100, y, "Date: 03/12/2025")
    y -= 25
    c.drawString(100, y, "Time: 09:37:45")
    y -= 25
    c.drawString(100, y, "=" * 50)
    y -= 30
    
    # Amount
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "Amount: RM 100.00")
    y -= 30
    
    # Account Details
    c.setFont("Helvetica", 12)
    c.drawString(100, y, "From Account: 5641917750991")
    y -= 25
    c.drawString(100, y, "To Account: 1234567890")
    y -= 25
    c.drawString(100, y, "Recipient Name: Tuesday Gambino Gym")
    y -= 30
    
    # Status
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, "Status: SUCCESSFUL")
    y -= 30
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(100, y, "Reference: This is a computer-generated receipt")
    y -= 20
    c.drawString(100, y, "Thank you for banking with Maybank")
    
    c.save()
    print(f"✅ Created sample receipt: {filename}")
    return filename

if __name__ == "__main__":
    try:
        create_sample_receipt()
        print("\n📄 Sample receipt created successfully!")
        print("You can now test the API with this file.")
    except ImportError:
        print("❌ reportlab not installed. Installing...")
        print("Run: pip install reportlab")
        print("\nAlternatively, test with your own PDF receipt.")
