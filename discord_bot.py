"""
Discord Bot Integration (Optional)
Add this to your OCR app when you're ready to send data to Discord
"""

import asyncio
from queue import Queue

import discord
from discord.ext import commands


class DiscordOCRBot:
    """Handles sending OCR results to Discord"""

    def __init__(self, token, channel_id):
        """
        Initialize Discord bot

        Args:
            token (str): Your Discord bot token
            channel_id (int): The channel ID to send messages to
        """
        self.token = token
        self.channel_id = channel_id
        self.bot = None
        self.channel = None
        self.is_ready = False
        self.message_queue = Queue()

    async def start_bot(self):
        """Start the Discord bot"""
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)

        @self.bot.event
        async def on_ready():
            print(f"✅ Discord bot logged in as {self.bot.user}")
            self.channel = self.bot.get_channel(self.channel_id)
            if self.channel:
                self.is_ready = True
                print(f"✅ Connected to channel: #{self.channel.name}")
                # Start message queue processor
                self.bot.loop.create_task(self.process_message_queue())
            else:
                print(f"❌ Channel {self.channel_id} not found!")

        # Start bot
        await self.bot.start(self.token)

    async def process_message_queue(self):
        """Process messages from queue and send to Discord"""
        while True:
            try:
                if not self.message_queue.empty():
                    text = self.message_queue.get()
                    await self._send_message(text)
                await asyncio.sleep(0.1)  # Small delay to prevent CPU spinning
            except Exception as e:
                print(f"❌ Error in message queue: {e}")
                await asyncio.sleep(1)

    async def _send_message(self, text, max_length=2000):
        """Internal method to send message to Discord"""
        if not self.is_ready or not self.channel:
            print("⏳ Discord bot not ready yet")
            return

        try:
            # Split long messages if needed
            if len(text) > max_length:
                chunks = [
                    text[i : i + max_length] for i in range(0, len(text), max_length)
                ]
                for chunk in chunks:
                    await self.channel.send(f"```\n{chunk}\n```")
            else:
                await self.channel.send(f"```\n{text}\n```")

            print("✅ Sent to Discord")
        except Exception as e:
            print(f"❌ Error sending to Discord: {e}")

    def send_ocr_result(self, text):
        """
        Queue OCR text to be sent to Discord channel
        This is a synchronous method that can be called from any thread

        Args:
            text (str): The OCR text to send
        """
        if self.is_ready:
            self.message_queue.put(text)
        else:
            print("⏳ Discord not ready, message not sent")

    async def stop_bot(self):
        """Stop the Discord bot"""
        if self.bot:
            await self.bot.close()
            print("🔴 Discord bot disconnected")


# Standalone test
if __name__ == "__main__":
    # Example usage
    TOKEN = "TOKEN"
    CHANNEL_ID = 1234567890  # Your channel ID

    async def test():
        bot = DiscordOCRBot(TOKEN, CHANNEL_ID)
        await bot.start_bot()

        # Wait for bot to be ready
        while not bot.is_ready:
            await asyncio.sleep(1)

        # Send test message
        await bot.send_ocr_result("Test OCR result from screen capture")

        # Keep alive
        await asyncio.sleep(5)
        await bot.stop_bot()

    # Run test
    asyncio.run(test())
