# 💾 Auto-Save Config Feature

## Fitur Baru: Token, Channel ID, & Capture Area Otomatis Tersimpan!

### Cara Kerja:

1. **Pertama kali:**
   - Isi Bot Token dan Channel ID
   - Klik "Connect Discord"
   - ✅ **Otomatis tersimpan ke file `ocr_config.json`**
   
2. **Atur Capture Area:**
   - Set X, Y, Width, Height
   - Klik "Update Area"
   - ✅ **Otomatis tersimpan juga!**

3. **Buka app lagi:**
   - Token, Channel ID, dan Capture Area **otomatis muncul**
   - Tinggal klik "Connect Discord" dan "Start OCR"
   - Tidak perlu setup ulang! 🎉

### File Config:

Config disimpan di file `ocr_config.json` di folder yang sama dengan app:

```json
{
  "token": "your_bot_token_here",
  "channel_id": "123456789",
  "capture_area": {
    "x": 215,
    "y": 60,
    "width": 973,
    "height": 160
  }
}
```

### Button Baru:

**"Clear Saved Config"** - Hapus token dan channel ID yang tersimpan (Capture Area tetap preserved)

### ⚠️ KEAMANAN PENTING!

1. **JANGAN share file `ocr_config.json`**
   - File ini berisi token bot kamu
   - Token = password bot

2. **JANGAN commit ke Git/GitHub**
   - File `.gitignore` sudah dibuat
   - `ocr_config.json` sudah masuk .gitignore

3. **Jika token bocor:**
   - Reset token di Discord Developer Portal
   - Klik "Clear Saved Config" di app
   - Connect ulang dengan token baru

### Tips:

- **Discord config** auto-save saat klik "Connect Discord"
- **Capture area** auto-save saat klik "Update Area"
- Aman untuk multi-user PC: setiap user punya config sendiri
- File config ada di folder app, bukan di system folder
- "Clear Saved Config" hanya menghapus Discord settings, Capture Area tetap tersimpan

### Struktur File:

```
folder-kamu/
├── ocr_app.py
├── discord_bot.py
├── ocr_config.json      ← CONFIG FILE (AUTO-CREATED)
└── .gitignore           ← PROTECT CONFIG
```

Sekarang kamu tidak perlu copy-paste token setiap kali buka app! 🚀
