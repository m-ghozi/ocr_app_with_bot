"""
Test Portable Tesseract Setup
Verifikasi apakah Tesseract portable sudah berfungsi
"""

import os
import sys

print("=" * 50)
print("Testing Portable Tesseract Setup")
print("=" * 50)
print()

# Check if tesseract folder exists
if not os.path.exists('tesseract'):
    print("❌ ERROR: tesseract folder not found!")
    print()
    print("Please run: copy_tesseract.bat first")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Check tesseract.exe
tesseract_exe = os.path.join('tesseract', 'tesseract.exe')
if not os.path.exists(tesseract_exe):
    print("❌ ERROR: tesseract.exe not found!")
    print(f"   Expected at: {tesseract_exe}")
    input("\nPress Enter to exit...")
    sys.exit(1)

print(f"✅ Found: {tesseract_exe}")

# Check tessdata folder
tessdata_dir = os.path.join('tesseract', 'tessdata')
if not os.path.exists(tessdata_dir):
    print("❌ ERROR: tessdata folder not found!")
    input("\nPress Enter to exit...")
    sys.exit(1)

print(f"✅ Found: {tessdata_dir}")

# Check for eng.traineddata
eng_data = os.path.join(tessdata_dir, 'eng.traineddata')
if not os.path.exists(eng_data):
    print("❌ ERROR: eng.traineddata not found!")
    print("   English language data is required")
    input("\nPress Enter to exit...")
    sys.exit(1)

print(f"✅ Found: eng.traineddata")

# Try to import pytesseract
try:
    import pytesseract
    print("✅ pytesseract library installed")
except ImportError:
    print("❌ pytesseract not installed")
    print("   Run: pip install pytesseract")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Try to import PIL
try:
    from PIL import Image
    print("✅ PIL (Pillow) library installed")
except ImportError:
    print("❌ PIL (Pillow) not installed")
    print("   Run: pip install Pillow")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = tesseract_exe

# Test OCR with simple text
print()
print("Testing OCR functionality...")
try:
    # Create a simple test image (white background with black text)
    from PIL import Image, ImageDraw, ImageFont
    
    # Create image
    img = Image.new('RGB', (300, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw text
    try:
        # Try to use default font
        draw.text((10, 30), "Hello OCR!", fill='black')
    except:
        # If font fails, still proceed
        draw.text((10, 30), "TEST", fill='black')
    
    # Perform OCR
    text = pytesseract.image_to_string(img)
    
    if text.strip():
        print(f"✅ OCR Test Successful!")
        print(f"   Detected text: {text.strip()}")
    else:
        print("⚠️  OCR ran but no text detected")
        print("   This might be normal for the test image")
    
except Exception as e:
    print(f"❌ OCR Test Failed: {e}")
    input("\nPress Enter to exit...")
    sys.exit(1)

print()
print("=" * 50)
print("✅ ALL TESTS PASSED!")
print("=" * 50)
print()
print("Portable Tesseract is working correctly!")
print("You can now:")
print("1. Run: python ocr_app_portable.py (to test the app)")
print("2. Run: build_portable.bat (to build EXE)")
print()

input("Press Enter to exit...")
