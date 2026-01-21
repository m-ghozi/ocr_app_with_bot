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

### Buat Bot:
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
1. Paste **Bot Token**
2. Paste **Channel ID**
3. Klik **"Connect Discord"**
4. Tunggu sampai **✅ Connected**

**Token & Channel ID auto-save!** Cukup setup sekali.

---

## 📁 Files

```
ocr_app.py          # Main app
discord_bot.py      # Discord module
requirements.txt    # Dependencies
ocr_config.json     # Auto-generated config (JANGAN SHARE!)
```

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

**Discord tidak connect**  
→ Pastikan MESSAGE CONTENT INTENT aktif di Developer Portal

**Overlay posisi salah**  
→ Cek DPI scaling Windows, set ke 100%

**"discord.py not found"**  
→ `pip install discord.py`

---

## 💡 Tips

- Test bot dulu dengan `test_discord_bot.py` (opsional)
- Gunakan **Win+Shift+S** untuk lihat koordinat screen
- Default capture interval: 1 detik (bisa diubah di code)
- Token tersimpan di `ocr_config.json` - JANGAN share file ini!

---

## 📝 Notes

- Token & Channel ID auto-save setelah connect
- Klik **"Clear Saved Config"** untuk hapus config
- File `.gitignore` sudah protect `ocr_config.json`

---

**Made with ❤️ for easy OCR automation**
