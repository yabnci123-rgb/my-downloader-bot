import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# جلب التوكن من إعدادات Render (لا تغير هذا السطر)
API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# إعدادات التحميل (تدعم يوتيوب، إنستغرام، تيك توك)
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video_file.mp4',
        'noplaylist': True,
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'video_file.mp4'

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("مرحباً بك! أرسل لي رابطاً من يوتيوب، تيك توك، أو إنستغرام وسأقوم بتحميله لك.")

@dp.message(F.text.startswith("http"))
async def handle_link(message: types.Message):
    msg = await message.reply("جاري التحميل... انتظر لحظة ⏳")
    try:
        # تنفيذ عملية التحميل
        file_path = download_video(message.text)
        video = types.FSInputFile(file_path)
        
        # إرسال الفيديو للمستخدم
        await message.answer_video(video, caption="تم التحميل بنجاح ✅")
        
        # حذف الفيديو من السيرفر بعد الإرسال لتوفير المساحة
        os.remove(file_path)
        await msg.delete()
    except Exception as e:
        await message.reply(f"عذراً، حدث خطأ أثناء التحميل. تأكد من أن الرابط صحيح.\nالخطأ: {str(e)}")

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
