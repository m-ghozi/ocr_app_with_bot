# 🚀 QUICK START - Build Portable OCR App

## 3 Langkah Simple:

### 1️⃣ Setup Tesseract (Pilih salah satu)

#### Option A: Auto-Copy (Jika sudah install Tesseract)
```bash
copy_tesseract.bat
```
Script akan auto-detect dan copy files.

#### Option B: Manual Copy
1. Install Tesseract dari: https://digi.bib.uni-mannheim.de/tesseract/
2. Copy folder instalasi ke project:
   ```
   C:\Program Files\Tesseract-OCR\
   →
   your-project\tesseract\
   ```

---

### 2️⃣ Test Setup
```bash
python test_portable_tesseract.py
```

Jika muncul **"✅ ALL TESTS PASSED!"** → Lanjut step 3

---

### 3️⃣ Build EXE (Pilih salah satu)

#### Option A: Simple Build (Tanpa bundled libraries)
```bash
pyinstaller --onefile --windowed ^
    --add-data "discord_bot.py;." ^
    --add-data "tesseract;tesseract" ^
    ocr_app_portable.py
```

**Hasil:** `dist\ocr_app_portable.exe` (~15-25 MB)

**User perlu:**
```bash
pip install pytesseract pillow requests
```

---

#### Option B: Full Portable (Bundled semua)
```bash
pyinstaller --onedir --windowed ^
    --add-data "discord_bot.py;." ^
    --add-data "tesseract;tesseract" ^
    --collect-all pytesseract ^
    --collect-all PIL ^
    --collect-all requests ^
    ocr_app_portable.py
```

**Hasil:** `dist\ocr_app_portable\` folder (~150-200 MB)

**User tidak perlu install apapun!** Extract & run ✅

---

## 📦 Distribusi

### Simple Build:
```
OCR-App/
├── ocr_app_portable.exe
├── discord_bot.py
├── tesseract/
└── README.txt (instruksi pip install)
```

### Full Portable:
```
OCR-App/
└── (semua files dari dist\ocr_app_portable\)
```

ZIP dan kirim ke user!

---

## ✅ Checklist

- [ ] Tesseract folder exists dengan tesseract.exe
- [ ] tessdata/eng.traineddata exists
- [ ] Test script passed
- [ ] EXE built successfully
- [ ] Tested EXE on another PC

---

## 🆘 Troubleshooting

**"tesseract folder not found"**
→ Run `copy_tesseract.bat` atau copy manual

**"pytesseract not installed"**
→ `pip install pytesseract pillow requests`

**Build failed**
→ `pip install pyinstaller`

**EXE crashes**
→ Run with console: `pyinstaller --onefile --console ...`

---

## 📊 Size Comparison

| Build Type | EXE Size | Total Size | User Install |
|------------|----------|------------|--------------|
| Simple | ~20 MB | ~100 MB | pip install |
| Full Portable | - | ~200 MB | Nothing ✅ |

---

**Need help?** Check `BUILD_PORTABLE_QUICKSTART.md` for details
