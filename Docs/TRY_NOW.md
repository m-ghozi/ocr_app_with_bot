# 🎯 COBA SEKARANG - Portable Build

## ✨ Yang Sudah Siap:

1. ✅ **ocr_app_portable.py** - App dengan auto-detect Tesseract
2. ✅ **discord_bot.py** - Discord webhook (lightweight)
3. ✅ **copy_tesseract.bat** - Auto-copy Tesseract
4. ✅ **test_portable_tesseract.py** - Test setup
5. ✅ **Dokumentasi lengkap**

---

## 🚀 LANGKAH COBA (5-10 Menit):

### Step 1: Install Tesseract (Jika Belum)
Download dari: https://digi.bib.uni-mannheim.de/tesseract/

File: `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (atau versi terbaru)

Install ke lokasi default: `C:\Program Files\Tesseract-OCR`

---

### Step 2: Copy Tesseract ke Project

Double-click:
```
copy_tesseract.bat
```

Script akan:
- ✅ Auto-detect Tesseract di PC kamu
- ✅ Copy semua files ke folder `tesseract/`
- ✅ Verifikasi semua files ada

**Hasil:**
```
tesseract/
├── tesseract.exe
├── tessdata/
│   └── eng.traineddata
└── *.dll files
```

---

### Step 3: Test Setup

```bash
python test_portable_tesseract.py
```

**Expected output:**
```
✅ Found: tesseract\tesseract.exe
✅ Found: tesseract\tessdata
✅ Found: eng.traineddata
✅ pytesseract library installed
✅ PIL (Pillow) library installed
✅ OCR Test Successful!

✅ ALL TESTS PASSED!
```

Jika ada error, ikuti instruksi di screen.

---

### Step 4: Test Run App (Tanpa Build)

```bash
python ocr_app_portable.py
```

App akan:
- ✅ Auto-detect portable Tesseract
- ✅ Load Discord settings (jika ada)
- ✅ Load capture area settings
- ✅ Ready to use!

**Test OCR:**
1. Set capture area
2. Click "Show Overlay"
3. Position over some text
4. Click "Start OCR"
5. Check terminal output

Jika OCR works → Portable Tesseract SUCCESS! ✅

---

### Step 5: Build EXE (Optional)

#### Simple Build (~20 MB):
```bash
pyinstaller --onefile --windowed --add-data "tesseract;tesseract" ocr_app_portable.py
```

**Hasil:** `dist\ocr_app_portable.exe`

#### Full Portable (~200 MB):
```bash
pyinstaller --onedir --windowed --add-data "tesseract;tesseract" --collect-all pytesseract --collect-all PIL ocr_app_portable.py
```

**Hasil:** `dist\ocr_app_portable\` (folder lengkap)

---

## 📦 Distribusi Ke User

### Simple Build:
```
OCR-App-v1.0/
├── ocr_app_portable.exe
├── discord_bot.py
├── tesseract/
│   ├── tesseract.exe
│   └── tessdata/
└── README.txt
```

**README.txt untuk user:**
```
INSTALASI:
1. pip install pytesseract pillow requests
2. Double-click ocr_app_portable.exe
3. Done!

Tesseract sudah bundled, tidak perlu install!
```

### Full Portable Build:
```
OCR-App-v1.0/
└── (extract semua dari dist\ocr_app_portable\)
```

**User:** Extract & double-click EXE. No install needed! ✅

---

## ⚡ Quick Commands Summary

```bash
# 1. Copy Tesseract
copy_tesseract.bat

# 2. Test setup
python test_portable_tesseract.py

# 3. Test app
python ocr_app_portable.py

# 4. Build EXE (simple)
pyinstaller --onefile --windowed --add-data "tesseract;tesseract" ocr_app_portable.py

# 5. Build EXE (full portable)
pyinstaller --onedir --windowed --add-data "tesseract;tesseract" --collect-all pytesseract --collect-all PIL ocr_app_portable.py
```

---

## 🎁 What You Get

### For Users:
✅ No Tesseract install needed  
✅ Portable Tesseract bundled (~60-80 MB)  
✅ Discord webhook (lightweight)  
✅ Auto-save settings  
✅ Simple setup  

### App Features:
✅ Auto-detect portable Tesseract  
✅ Support webhook & bot token  
✅ Auto-save capture area  
✅ Auto-save Discord config  
✅ Better GUI layout  
✅ Proper error handling  

---

## 🆘 Common Issues

**"copy_tesseract.bat: Tesseract not found"**
→ Install Tesseract terlebih dahulu

**"test failed: pytesseract not installed"**
→ `pip install pytesseract pillow requests`

**"OCR error: tesseract.exe not found"**
→ Check folder `tesseract/` ada dan berisi tesseract.exe

**Build error: "pyinstaller not found"**
→ `pip install pyinstaller`

**EXE crash on startup**
→ Build with console untuk lihat error:
```bash
pyinstaller --onefile --console --add-data "tesseract;tesseract" ocr_app_portable.py
```

---

## 📊 Size Reference

| Component | Size |
|-----------|------|
| Tesseract portable | ~60-80 MB |
| Python EXE (simple) | ~15-25 MB |
| Python EXE (full) | ~150-200 MB |
| discord_bot.py | ~5 KB |

**Total Distribution:**
- Simple: ~100 MB
- Full: ~200 MB

---

## ✅ Success Checklist

- [ ] Tesseract installed di PC
- [ ] `copy_tesseract.bat` berhasil
- [ ] `test_portable_tesseract.py` passed
- [ ] `ocr_app_portable.py` jalan
- [ ] OCR berfungsi
- [ ] (Optional) EXE built
- [ ] (Optional) Tested di PC lain

---

**Ready to try!** Mulai dari Step 1 👆

Any questions? Check the detailed guides:
- `PORTABLE_README.md` - Quick guide
- `BUILD_PORTABLE_QUICKSTART.md` - Detailed options
- `BUILD_PORTABLE_GUIDE.md` - Complete guide
