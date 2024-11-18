from telegram import Update, Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import os

# Direktori untuk menyimpan file sementara
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

TOKEN = "7749846413:AAHCCJBVH9g3QM3x07W_3g0rQpFLAAb_4PU"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Selamat datang di bot edit video!\n\n"
        "Kirimkan video untuk memulai editing. Anda dapat menggunakan perintah:\n"
        "/watermark [x_pos] [y_pos] - Tambah watermark\n"
        "/add_ads - Tambah iklan\n"
        "/running_text [text] [start_time] [duration] - Tambah teks berjalan"
    )

def add_watermark(video_path, watermark_path, x, y):
    video = VideoFileClip(video_path)
    watermark = VideoFileClip(watermark_path).set_position((x, y)).set_duration(video.duration)
    result = CompositeVideoClip([video, watermark])
    output_path = os.path.join(TEMP_DIR, "watermarked_video.mp4")
    result.write_videofile(output_path, codec="libx264")
    return output_path

def process_video(update: Update, context: CallbackContext):
    video_file = update.message.video
    if not video_file:
        update.message.reply_text("Harap kirimkan video terlebih dahulu.")
        return

    file_path = os.path.join(TEMP_DIR, video_file.file_id + ".mp4")
    video_file.get_file().download(file_path)
    context.user_data["video_path"] = file_path
    update.message.reply_text("Video telah diunggah. Anda dapat mulai mengeditnya.")

def watermark_command(update: Update, context: CallbackContext):
    try:
        args = context.args
        x_pos = int(args[0])
        y_pos = int(args[1])
        watermark_path = "path/to/your/watermark.png"  # Ganti dengan path watermark

        video_path = context.user_data.get("video_path")
        if not video_path:
            update.message.reply_text("Kirimkan video terlebih dahulu.")
            return

        output_path = add_watermark(video_path, watermark_path, x_pos, y_pos)
        update.message.reply_text("Watermark ditambahkan!")
        update.message.reply_video(video=open(output_path, "rb"))
    except Exception as e:
        update.message.reply_text(f"Terjadi kesalahan: {e}")

# Tambah fungsi untuk iklan dan running text di sini.

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video, process_video))
    dp.add_handler(CommandHandler("watermark", watermark_command))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()