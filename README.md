# 🔍 OCR App with Discord Integration

Real-time screen OCR application yang bisa kirim hasil ke Discord otomatis. Ringan, portable, dan mudah digunakan!

![Version](https://img.shields.io/badge/version-1.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-0078d7)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### Core Features
- ✅ **Real-Time OCR** - Membaca text dari layar secara real-time
- ✅ **Customizable Area** - Atur posisi dan ukuran area tangkapan (auto-save!)
- ✅ **Visual Overlay** - Kotak merah semi-transparan untuk preview
- ✅ **Smart Detection** - Hanya output ketika text berubah

### Discord Integration
- ✅ **Discord Webhook** - Super ringan, hanya butuh `requests` (~1 MB)
- ✅ **Bot Token Support** - Support full bot jika mau fitur advanced
- ✅ **Auto-Save Config** - Token & settings tersimpan otomatis
- ✅ **Queue System** - Tidak ada message yang hilang

### Portable Version
- ✅ **Bundled Tesseract** - User tidak perlu install Tesseract!
- ✅ **Auto-Detect** - Otomatis detect Tesseract portable/installed
- ✅ **Small Dependencies** - Hanya 3 library (pytesseract, pillow, requests)

---

## 🚀 Quick Start

### Installation

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pytesseract
Pillow
requests
```

#### 2. Install Tesseract OCR
Download: https://github.com/UB-Mannheim/tesseract/wiki

Atau pakai portable version! (Lihat [Portable Build](#-portable-build))

#### 3. Run App
```bash
# Regular version
python ocr_app.py

# Portable version (auto-detect Tesseract)
python ocr_app_portable.py
```

---

## 🤖 Discord Setup

### ⚡ Method 1: Webhook (RECOMMENDED - Super Easy!)

**Setup hanya 30 detik:**

1. Discord → Klik kanan channel → **Edit Channel**
2. **Integrations** → **Create Webhook**
3. **Copy Webhook URL**
4. Paste di app → **Connect Discord**
5. ✅ Done!

**Keuntungan:**
- ✅ No `discord.py` needed (~200 MB saved!)
- ✅ Setup super cepat
- ✅ Lightweight (hanya butuh `requests`)

**Format:**
```
Webhook URL: https://discord.com/api/webhooks/123.../abc...
Channel ID: (kosongkan)
```

📖 **Tutorial lengkap:** [WEBHOOK_GUIDE.md](Docs/WEBHOOK_GUIDE.md)

---

### Method 2: Bot Token (Advanced)

<details>
<summary>Klik untuk expand</summary>

**Setup 5-10 menit:**

1. Buka https://discord.com/developers/applications
2. **New Application** → Buat bot
3. Copy **Token**
4. Aktifkan **MESSAGE CONTENT INTENT**
5. **OAuth2** → **URL Generator** → Invite bot
6. Copy **Channel ID** (klik kanan channel)
7. Paste di app

**Format:**
```
Bot Token: MTIzNDU2Nzg5...
Channel ID: 123456789012345678
```

**Catatan:** Butuh install `discord.py` (~200 MB)

</details>

---

## 📁 Files

```
📦 OCR-App/
├── 📄 ocr_app.py                    # Main app (regular)
├── 📄 ocr_app_portable.py           # Portable version (bundled Tesseract)
├── 📄 discord_bot.py                # Discord module (webhook + bot)
├── 📄 requirements.txt              # Dependencies (lightweight!)
├── 📄 ocr_config.json              # Auto-generated (JANGAN SHARE!)
│
├── 🛠️ copy_tesseract.bat           # Auto-copy Tesseract untuk portable
├── 🛠️ test_portable_tesseract.py   # Test portable setup
├── 🛠️ build_portable.bat           # Build portable EXE
│
└── 📚 Docs/
    ├── WEBHOOK_GUIDE.md             # Setup Discord webhook
    ├── PORTABLE_README.md           # Portable build guide
    └── TRY_NOW.md                   # Quick start portable
```

---

## ⚙️ Usage

### 1. Setup Capture Area
- Set **X, Y** position (pojok kiri atas)
- Set **Width, Height** (ukuran kotak)
- Klik **"Update Area"**
- ✅ **Auto-save!** Settings tersimpan otomatis

### 2. Visual Preview
- Klik **"👁 Show Overlay"**
- Kotak merah muncul di screen
- Posisikan di atas text yang mau dibaca

### 3. Connect Discord (Optional)
- Paste **Webhook URL** atau **Bot Token**
- Klik **"Connect Discord"**
- Tunggu status: **"● Connected"**

### 4. Start OCR
- Klik **"▶ Start OCR"**
- Text otomatis terbaca setiap 1 detik
- Output di terminal & Discord

### 5. Stop OCR
- Klik **"⏹ Stop OCR"**

---

## 📦 Portable Build

Build aplikasi portable yang **tidak perlu install Tesseract!**

### Quick Steps:

```bash
# 1. Copy Tesseract portable
copy_tesseract.bat

# 2. Test setup
python test_portable_tesseract.py

# 3. Build EXE
pyinstaller --onefile --windowed --add-data "tesseract;tesseract" ocr_app_portable.py
```

**Result:**
```
dist/
├── ocr_app_portable.exe  (~20 MB)
└── tesseract/            (~60-80 MB)
    ├── tesseract.exe
    └── tessdata/
```

**Total: ~100 MB** (normal untuk OCR app!)

📖 **Panduan lengkap:** [PORTABLE_README.md](Docs/PORTABLE_README.md) & [TRY_NOW.md](Docs/TRY_NOW.md)

---

## 🔧 Configuration

### Auto-Save Config
Semua settings otomatis tersimpan di `ocr_config.json`:

```json
{
  "token": "your_webhook_or_token",
  "channel_id": "optional_for_webhook",
  "capture_area": {
    "x": 215,
    "y": 60,
    "width": 973,
    "height": 160
  }
}
```

**Auto-save triggers:**
- ✅ Klik "Update Area" → Save capture area
- ✅ Klik "Connect Discord" → Save semua settings
- ✅ Klik "Clear Config" → Clear Discord only, preserve area

⚠️ **JANGAN share file ini!** (Ada token Discord kamu)

---

## 🎨 GUI Features

- **2-Column Layout** - Compact & efisien
- **Icons** - ▶ ⏹ 👁 untuk visual cues
- **Status Indicator** - ● Real-time status
- **Responsive** - Auto-resize sesuai konten
- **Clean Design** - Minimal tapi jelas

---

## 💡 Tips & Tricks

### Capture Area
- Gunakan **Win+Shift+S** untuk lihat koordinat screen
- Mulai dengan area besar, lalu perkecil untuk akurasi
- Position overlay sebelum start OCR

### OCR Accuracy
- Text harus jelas & kontras tinggi
- Hindari font fancy/dekoratif
- Perbesar area jika text terpotong

### Discord
- **Webhook** lebih ringan dari bot token
- Token auto-save, setup sekali saja
- Bisa pakai multiple webhooks untuk channel berbeda

### Performance
- Default interval: 1 detik (bisa diubah di code)
- Close apps lain untuk OCR lebih cepat
- Overlay bisa di-hide saat OCR running

---

## 🆘 Troubleshooting

### "tesseract not found"
**Solution:**
1. Install Tesseract dari link di atas, atau
2. Gunakan `ocr_app_portable.py` dengan bundled Tesseract, atau
3. Edit line 16 di `ocr_app.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\path\to\tesseract.exe"
   ```

### Discord tidak connect (webhook)
**Solution:**
- Cek webhook URL masih valid
- Test webhook di browser/Postman
- Pastikan webhook tidak di-delete di Discord

### Discord tidak connect (bot)
**Solution:**
- Pastikan **MESSAGE CONTENT INTENT** aktif
- Bot sudah di-invite ke server
- Channel ID benar (angka panjang)

### OCR tidak akurat
**Solution:**
- Perbesar capture area
- Pastikan text jelas & tidak blur
- Coba ubah tesseract config (advanced)

### Overlay posisi salah
**Solution:**
- Cek DPI scaling Windows (set 100%)
- Koordinat X,Y mungkin negatif di multi-monitor
- Update area lagi setelah ubah monitor setup

### "requests not found"
**Solution:**
```bash
pip install requests
```

---

## 📊 Size & Performance

| Metric | Value |
|--------|-------|
| **App Size** | ~20 MB (EXE) |
| **Tesseract** | ~60-80 MB |
| **Dependencies** | ~5-10 MB |
| **Total Portable** | ~100 MB |
| **RAM Usage** | ~50-100 MB |
| **CPU Usage** | Low (~5-10%) |

---

## 🔐 Security & Privacy

### What Gets Saved:
- ✅ Discord webhook/token (local only)
- ✅ Capture area settings
- ❌ **NO OCR results saved**
- ❌ **NO screenshots saved**

### Best Practices:
- 🔒 Don't share `ocr_config.json`
- 🔒 Don't commit config to Git (`.gitignore` included)
- 🔒 Revoke webhook if accidentally shared
- 🔒 Reset bot token if compromised

---

## 📚 Documentation

- **[WEBHOOK_GUIDE.md](Docs/WEBHOOK_GUIDE.md)** - Setup Discord webhook
- **[PORTABLE_README.md](Docs/PORTABLE_README.md)** - Portable build quick guide
- **[TRY_NOW.md](Docs/TRY_NOW.md)** - Try portable build sekarang
- **[AUTO_SAVE_CONFIG.md](Docs/AUTO_SAVE_CONFIG.md)** - Auto-save feature explained

---

## 🎯 Use Cases

### Gaming
- Baca event text otomatis (**THIS**)
- Translate game text real-time
- Log dialog/story ke Discord

### Work
- Extract text dari image/PDF
- Auto-log meeting notes
- Copy text dari video/stream

### Streaming
- Display OCR text di OBS
- Auto-translate subtitles
- Log chat ke Discord

### Automation
- Monitor app status via OCR
- Auto-respond berdasarkan text
- Data extraction from legacy apps

---

## 🚧 Roadmap

### v1.1 (Planned)
- [ ] Multiple capture areas
- [ ] Custom OCR intervals per area
- [ ] Screenshot save option
- [ ] OCR history log

### v1.2 (Future)
- [ ] Hotkey support
- [ ] System tray integration
- [ ] Auto-start with Windows
- [ ] Multiple Discord channels

### v2.0 (Ideas)
- [ ] Machine learning text classification
- [ ] Translation support
- [ ] Web interface
- [ ] Mobile companion app

---

## 🤝 Contributing

Contributions welcome! Ideas:
- Improve OCR accuracy
- Add new features
- Optimize performance
- Better UI/UX
- Bug fixes

---

## 📝 License

MIT License - Free to use, modify, and distribute!

---

## 💖 Credits

**Built with:**
- Python 3.8+
- Tesseract OCR
- Tkinter (GUI)
- Pillow (Screenshot)
- Requests (Discord webhook)
- PyInstaller (EXE build)

**Thanks to:**
- Tesseract team for amazing OCR engine
- Discord for webhook API
- Python community

---


## ⭐ Quick Links

| Link | Description |
|------|-------------|
| [Install](#-quick-start) | Get started |
| [Discord Setup](#-discord-setup) | Connect Discord |
| [Portable Build](#-portable-build) | Build portable app |
| [Troubleshooting](#-troubleshooting) | Fix issues |
| [Documentation](#-documentation) | Read docs |

---

**Made with ❤️ for easy OCR automation**

🎉 **Enjoy your OCR app!**
