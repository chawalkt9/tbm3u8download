import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Aapka HLS Worker Link
TARGET_M3U8_URL = "https://amzon.ktnetwork002.workers.dev/?hls=https%3A%2F%2F1024tera.com%2Fshare%2Fstreaming.m3u8%3Fuk%3D4400357464123%26shareid%3D68683755866%26type%3DM3U8_FLV_264_480%26fid%3D202323108919207%26sign%3Df06cc764fa758d062d8b7c8fecea90dd1137cce1%26timestamp%3D1757999473%26clienttype%3D0%26channel%3Ddubox"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! `/send` command bhejein rocket speed se video download karne ke liye.")

async def send_video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("🚀 Downloading at rocket speed... Please wait.")
    output_filename = "downloaded_video.mp4"

    try:
        ydl_opts = {
            'outtmpl': output_filename,
            'concurrent_fragment_downloads': 10,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([TARGET_M3U8_URL])

        if not os.path.exists(output_filename):
            await status_msg.edit_text("❌ Download failed! File was not created.")
            return

        await status_msg.edit_text("📤 Uploading video to Telegram...")

        with open(output_filename, "rb") as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="Here is your video! 🚀",
                supports_streaming=True
            )

        await status_msg.delete()

    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit_text(f"❌ An error occurred: {str(e)}")

    finally:
        if os.path.exists(output_filename):
            os.remove(output_filename)

def main():
    # Environment variable se token lena sabse safe tareeqa hai Render ke liye
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8281288211:AAGxCY7Kw9zSC2-FyGEuhEL6UH7I0Yu0XOE")
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send_video_handler))

    print("🤖 Bot is running on Render...")
    app.run_polling()

if __name__ == "__main__":
    main()
