import os
from bale import Bot, Message
import requests

BOT_TOKEN = os.environ.get("BALE_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("متغیر محیطی BALE_BOT_TOKEN تنظیم نشده است.")

API_URL = "https://api.abantether.com/api/v1/manager/otc/ticker"

bot = Bot(token=BOT_TOKEN)


@bot.event
async def on_message(message: Message):
    text = message.content.strip()

    if text.lower() == "/start":
        await message.reply(
            "👋 سلام!\n\n"
            "🌟 من ابوالفضل علیزاده هستم، به ربات قیمت ارز خوش اومدی.\n\n"
            "💎 این ربات آخرین قیمت خرید ارزها را از آبان‌تتر برای شما نمایش می‌دهد.\n\n"
            "🪙 فقط نماد ارز را ارسال کنید.\n\n"
            "📌 مثال:\n"
            "BTC\n"
            "ETH\n"
            "USDT\n\n"
            "🚀 موفق باشید."
        )
        return

    symbol = text.upper()

    if not symbol.endswith("IRT"):
        symbol += "IRT"

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        markets = response.json()["data"]["markets"]

        if symbol not in markets:
            await message.reply(f"❌ ارز {symbol} پیدا نشد.")
            return

        price = float(markets[symbol]["buy_price"])

        price_text = f"{int(price):,}"

        await message.reply(
            f"""💹 استعلام قیمت ارز

🪙 ارز: {symbol}

💰 قیمت خرید:
{price_text} تومان

━━━━━━━━━━━━━━
📊 منبع: آبان‌تتر"""
        )

    except requests.exceptions.RequestException:
        await message.reply("❌ خطا در ارتباط با سرور.")

    except Exception as e:
        await message.reply(f"❌ خطا:\n{e}")


bot.run()
