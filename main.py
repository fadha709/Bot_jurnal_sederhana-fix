
import logging
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Autentikasi Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Ambil ID sheet dari variabel lingkungan
SHEET_ID = os.getenv("SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

# Fungsi bantu parsing data dari pesan Telegram
def parse_message(text):
    parts = text.strip().split(",")
    if len(parts) < 10:
        return None
    return parts[:10]

# Handler /start
    await update.message.reply_text(
        """Halo! Kirim data tradingmu dengan format:

Tanggal, Pair, Posisi, Lot, Entry, TP, SL, Close, Hasil, Catatan

Contoh:

2025-06-07, XAU/USD, Buy, 0.01, 2350.0, 2360.0, 2340.0, 2355.0, Profit, Entry sesuai setup"""
    )
      #  "2025-06-07, XAU/USD, Buy, 0.01, 2350.0, 2360.0, 2340.0, 2355.0, Profit, Entry sesuai setup"
    )

# Handler pesan masuk
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    data = parse_message(msg)
    if data:
        sheet.append_row(data)
        await update.message.reply_text("✅ Data berhasil dicatat di Google Sheets!")
    else:
        await update.message.reply_text("❌ Format salah. Pastikan memisahkan dengan koma dan lengkap 10 kolom.")

# Fungsi utama
def main():
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
