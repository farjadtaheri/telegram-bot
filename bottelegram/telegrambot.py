import requests
import time
from telegram import Bot
import sys
import io
import asyncio

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOKEN = ""
CHANNEL_ID = ""  # شناسه عددی کانال

def get_price():
    try:
        url = ''
        response = requests.get(url)
        data = response.json()
        print("داده‌های دریافتی از API:", data)
        if 'stats' in data and '100k_floki-usdt' in data['stats'] and 'latest' in data['stats']['100k_floki-usdt']:
            return float(data['stats']['100k_floki-usdt']['latest']) / 100000  # تقسیم بر 100,000
        else:
            print("❌ داده قیمت یافت نشد.")
            return None
    except Exception as e:
        print(f"❌ خطا در دریافت قیمت: {e}")
        return None

async def send_message(bot, text):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='HTML')
        print("✅ پیام با موفقیت ارسال شد.")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")

async def main():
    bot = Bot(token=TOKEN)
    # بررسی دسترسی ربات به کانال
    try:
        await bot.get_chat(chat_id=CHANNEL_ID)
        print("✅ ربات به کانال دسترسی دارد.")
    except Exception as e:
        print(f"❌ ربات به کانال دسترسی ندارد: {e}")
        return

    while True:
        try:
            price = get_price()
            if price:
                message = f"💵 Floki: {price:,.8f} USDT"  # تغییر فرمت به 8 رقم اعشار
                await send_message(bot, message)
            else:
                print("❌ قیمت دریافت نشد.")
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            print("❌ برنامه با توقف دستی متوقف شد.")
            break
        except Exception as e:
            print(f"❌ خطای کلی: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("❌ برنامه توسط کاربر متوقف شد.")