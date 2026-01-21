# 🔍 OCR App with Discord

Aplikasi OCR real-time yang bisa kirim hasil ke Discord otomatis.

---

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Jalankan App
```bash
python ocr_app.py
```

### 3. Setup
1. **Atur Capture Area** (X, Y, Width, Height)
2. Klik **"Show Overlay"** untuk lihat area
3. Klik **"Start OCR"** untuk mulai

---

## 🤖 Discord Setup (Opsional)

### ⚡ Method 1: Webhook (RECOMMENDED - Super Ringan!)

1. Discord → Klik kanan channel → **Edit Channel**
2. **Integrations** → **Create Webhook**
3. **Copy Webhook URL**
4. Di app: Paste webhook URL
5. ✅ Selesai! (30 detik)

**Keuntungan:**
- ✅ Tidak perlu install `discord.py` (~200 MB)
- ✅ Setup super cepat
- ✅ Portable app lebih kecil

📖 **Panduan lengkap**: `WEBHOOK_GUIDE.md`

### Method 2: Bot Token (Advanced)

<details>
<summary>Klik untuk lihat (tidak recommended)</summary>
1. Buka https://discord.com/developers/applications
2. **New Application** → Buat bot
3. Copy **Token** (save!)
4. Aktifkan **MESSAGE CONTENT INTENT**
5. **OAuth2** → **URL Generator** → Centang **bot** + **Send Messages**
6. Copy URL → Paste di browser → Invite bot ke server

### Dapatkan Channel ID:
1. Discord Settings → **Advanced** → Aktifkan **Developer Mode**
2. Klik kanan channel → **Copy Channel ID**

### Connect di App:
1. Paste **Webhook URL** atau **Bot Token**
2. (Optional) Paste **Channel ID** (jika pakai bot token)
3. Klik **"Connect Discord"**
4. Tunggu sampai **✅ Connected**

**App auto-detect** webhook atau bot token!

</details>

---

## 📁 Files

```
ocr_app.py          # Main app
discord_bot.py      # Discord module (supports webhook & bot)
requirements.txt    # Dependencies (lightweight!)
ocr_config.json     # Auto-generated config (JANGAN SHARE!)
```

**Dependencies:**
- `pytesseract` - OCR engine
- `Pillow` - Screenshot
- `requests` - Discord webhook (hanya 1 MB!)
- ~~`discord.py`~~ - Tidak perlu lagi! ✅

---

## ⚙️ Features

✅ Real-time OCR dari screen  
✅ Customizable capture area  
✅ Visual overlay (kotak merah)  
✅ Kirim otomatis ke Discord  
✅ Auto-save Token & Channel ID  
✅ Smart detection (no spam)  

---

## 🔧 Troubleshooting

**"tesseract not found"**  
→ Edit `ocr_app.py` line 16, uncomment & set path Tesseract

**Discord tidak connect (webhook)**  
→ Cek webhook URL masih valid, test di browser

**Discord tidak connect (bot token)**  
→ Pastikan MESSAGE CONTENT INTENT aktif di Developer Portal

**Overlay posisi salah**  
→ Cek DPI scaling Windows, set ke 100%

**"requests not found"**  
→ `pip install requests`

---

## 💡 Tips

- Test bot dulu dengan `test_discord_bot.py` (opsional)
- Gunakan **Win+Shift+S** untuk lihat koordinat screen
- Default capture interval: 1 detik (bisa diubah di code)
- Token tersimpan di `ocr_config.json` - JANGAN share file ini!

---

## 📦 Build EXE

Ingin distribusikan sebagai EXE? Mudah!

### Quick Build:
```bash
# Install PyInstaller
pip install pyinstaller

# Build EXE
pyinstaller --onefile --windowed --name "OCR-Discord-App" ocr_app.py
```

Atau gunakan script otomatis:
```bash
build_exe.bat
```

**EXE file** akan ada di folder `dist/`

⚠️ **PENTING:** Copy `discord_bot.py` ke folder yang sama dengan EXE!

📖 **Panduan lengkap:** Baca `BUILD_EXE_GUIDE.md`

---

## 📝 Notes

- Token & Channel ID auto-save setelah connect
- Klik **"Clear Saved Config"** untuk hapus config
- File `.gitignore` sudah protect `ocr_config.json`

---

**Made with ❤️ for easy OCR automation**
