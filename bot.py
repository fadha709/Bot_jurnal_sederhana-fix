
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim data trading kamu dengan format:
PAIR,TIPE,LOT,ENTRY,SL,TP,CLOSE,PNL,CATATAN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = update.message.text
    data = pesan.split(",")

    if len(data) < 9:
        await update.message.reply_text("❌ Format salah!
Gunakan:
PAIR,TIPE,LOT,ENTRY,SL,TP,CLOSE,PNL,CATATAN")
        return

    balasan = f"✅ Data dicatat!\n" + "\n".join([
        f"PAIR: {data[0]}",
        f"TIPE: {data[1]}",
        f"LOT: {data[2]}",
        f"ENTRY: {data[3]}",
        f"SL: {data[4]}",
        f"TP: {data[5]}",
        f"CLOSE: {data[6]}",
        f"PNL: {data[7]}",
        f"CATATAN: {data[8]}",
    ])

    print(f"[LOG] {data}")  # Simpan ke log server (Railway log)
    await update.message.reply_text(balasan)

app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
