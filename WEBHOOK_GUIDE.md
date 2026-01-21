# 🚀 Setup Discord dengan Webhook (Super Ringan!)

## ✨ Keuntungan Webhook vs Bot Token

| Feature | Webhook | Bot Token |
|---------|---------|-----------|
| Install discord.py | ❌ TIDAK | ✅ Ya (~200 MB) |
| Setup complexity | ⭐ Super Mudah | ⭐⭐⭐ Ribet |
| Dependencies | requests only | discord.py + 10+ libs |
| App size (portable) | ~100 MB | ~300-400 MB |
| Features | Kirim message | Full bot features |

**Rekomendasi: Pakai Webhook!** (Lebih ringan & mudah)

---

## 🎯 Cara Setup Webhook (5 Menit!)

### Step 1: Buat Webhook di Discord

1. **Buka Discord** → Pilih server kamu
2. **Klik kanan** pada channel yang ingin dipakai
3. Pilih **"Edit Channel"**
4. Klik tab **"Integrations"**
5. Klik **"Create Webhook"** atau **"View Webhooks"**
6. Klik **"New Webhook"**
7. (Optional) Ganti nama: "OCR Bot"
8. **COPY WEBHOOK URL** 
   - Format: `https://discord.com/api/webhooks/123456789/abcdefg...`
9. Klik **"Save Changes"**

✅ **Selesai!** Tidak perlu bot token, invite bot, atau setting permissions!

---

### Step 2: Pakai di OCR App

1. Buka OCR App
2. Di **"Discord Settings"**:
   - **Paste Webhook URL** (bukan bot token!)
   - **Channel ID**: Kosongkan saja (tidak perlu!)
3. Klik **"Connect Discord"**
4. ✅ Langsung connected!

---

## 📋 Perbandingan Setup

### Webhook Method (RECOMMENDED ✅):
```
1. Klik kanan channel → Edit Channel
2. Integrations → Create Webhook
3. Copy URL
4. Paste di app
✅ SELESAI! (30 detik)
```

### Bot Token Method (Old Way):
```
1. Buat app di Discord Developer Portal
2. Buat bot
3. Copy token
4. Enable intents
5. Generate OAuth URL
6. Invite bot ke server
7. Copy channel ID
8. Paste token & channel ID di app
9. Install discord.py (~200 MB)
❌ Ribet! (5-10 menit)
```

---

## 🔧 Format Input di App

### Jika Pakai Webhook:
```
Bot Token/Webhook: https://discord.com/api/webhooks/123.../abc...
Channel ID: (kosongkan atau isi apa saja)
```

### Jika Pakai Bot Token (Old):
```
Bot Token: MTIzNDU2Nzg5MDEyMzQ1Njc4.GhIjKl.MnOp...
Channel ID: 123456789012345678
```

**App auto-detect** mana yang kamu pakai!

---

## 💡 FAQ

**Q: Webhook vs Bot Token, mana lebih baik?**  
A: **Webhook!** Lebih ringan, lebih mudah, cukup untuk kirim message.

**Q: Apakah webhook bisa read message?**  
A: Tidak, webhook hanya bisa KIRIM message. Untuk OCR app ini sudah cukup!

**Q: Apakah webhook aman?**  
A: Ya, selama URL tidak di-share. Treat webhook URL seperti password!

**Q: Bisa pakai bot token juga?**  
A: Bisa! App support kedua metode. Tapi webhook lebih recommended.

**Q: Webhook bisa di-revoke?**  
A: Ya! Delete webhook di Discord channel settings kapan saja.

---

## ⚠️ Keamanan Webhook

### DO ✅:
- Simpan webhook URL seperti password
- Jangan share webhook URL
- Revoke & buat baru jika bocor

### DON'T ❌:
- Jangan commit webhook URL ke Git
- Jangan share screenshot yang ada webhook URL
- Jangan post webhook URL di forum/Discord

---

## 🎁 Contoh Webhook URL

```
Format:
https://discord.com/api/webhooks/[WEBHOOK_ID]/[WEBHOOK_TOKEN]

Contoh (FAKE):
https://discord.com/api/webhooks/123456789012345678/abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJ

Panjang: ~120 karakter
```

---

## 📦 Dependencies

### Dengan Webhook (Lightweight):
```bash
pip install requests
```
**Total size: ~1 MB**

### Dengan Bot Token (Full):
```bash
pip install discord.py
```
**Total size: ~200 MB+**

---

## 🚀 Kesimpulan

✅ **Pakai Webhook!**
- Super mudah (30 detik setup)
- Super ringan (1 MB vs 200 MB)
- Cukup untuk OCR app
- Portable app jadi lebih kecil (~100 MB vs ~400 MB)

**Perfect untuk distribusi ke user!** 🎉
