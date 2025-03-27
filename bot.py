import json
import asyncio
from pyrogram import Client, filters
from playwright.async_api import async_playwright

# Telegram Bot Token (Get from @BotFather)
BOT_TOKEN = "7983703501:AAEfBt_-hAwQj5BvhNWPWBCulfnZbZs0w2I"

# Setup Telegram Client
app = Client("youtube_cookie_bot", bot_token=BOT_TOKEN)

# Command to Extract YouTube Cookies
@app.on_message(filters.command("getcookies"))
async def get_youtube_cookies(client, message):
    await message.reply_text("🔄 Extracting YouTube cookies, please wait...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Open YouTube
        await page.goto("https://www.youtube.com")
        await asyncio.sleep(5)  # Wait for page to load

        # Extract Cookies
        cookies = await page.context.cookies()

        # Save Cookies to JSON file
        cookies_file = "youtube_cookies.json"
        with open(cookies_file, "w") as file:
            json.dump(cookies, file, indent=4)

        await browser.close()

    # Send Cookies File to Telegram
    await client.send_document(message.chat.id, cookies_file)

# Start the Bot
app.run()
