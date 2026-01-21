"""
Discord Webhook Integration (Lightweight Alternative)
Tidak perlu discord.py - hanya pakai requests library!
"""

import json
import threading
import time
from queue import Queue

import requests


class DiscordWebhook:
    """Lightweight Discord integration using webhooks - NO discord.py needed!"""

    def __init__(self, webhook_url):
        """
        Initialize Discord webhook

        Args:
            webhook_url (str): Discord webhook URL
        """
        self.webhook_url = webhook_url
        self.is_ready = True
        self.message_queue = Queue()

        # Start message queue processor
        self.processor_thread = threading.Thread(
            target=self._process_queue, daemon=True
        )
        self.processor_thread.start()

        print("✅ Discord webhook ready")

    def _process_queue(self):
        """Process messages from queue and send to Discord"""
        while True:
            try:
                if not self.message_queue.empty():
                    text = self.message_queue.get()
                    self._send_message(text)
                time.sleep(0.1)  # Small delay to prevent CPU spinning
            except Exception as e:
                print(f"❌ Error in message queue: {e}")
                time.sleep(1)

    def _send_message(self, text, max_length=2000):
        """Internal method to send message via webhook"""
        try:
            # Split long messages if needed
            if len(text) > max_length:
                chunks = [
                    text[i : i + max_length] for i in range(0, len(text), max_length)
                ]
                for chunk in chunks:
                    self._send_single_message(chunk)
            else:
                self._send_single_message(text)

            print("✅ Sent to Discord")
        except Exception as e:
            print(f"❌ Error sending to Discord: {e}")

    def _send_single_message(self, text):
        """Send a single message to Discord webhook"""
        payload = {"content": f"```\n{text}\n```", "username": "OCR Bot"}

        response = requests.post(
            self.webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code not in [200, 204]:
            raise Exception(f"Webhook returned status {response.status_code}")

    def send_ocr_result(self, text):
        """
        Queue OCR text to be sent to Discord
        This is a synchronous method that can be called from any thread

        Args:
            text (str): The OCR text to send
        """
        if self.is_ready:
            self.message_queue.put(text)
        else:
            print("⏳ Discord not ready, message not sent")

    def test_connection(self):
        """Test webhook connection"""
        try:
            self._send_single_message("🤖 OCR Bot connected!")
            return True
        except Exception as e:
            print(f"❌ Webhook test failed: {e}")
            return False


# Untuk backward compatibility dengan discord_bot.py
class DiscordOCRBot:
    """Wrapper class for compatibility"""

    def __init__(self, webhook_url_or_token, channel_id=None):
        """
        Initialize Discord integration

        Args:
            webhook_url_or_token: Either webhook URL or bot token (for compatibility)
            channel_id: Ignored if webhook_url is provided
        """
        # Detect if it's webhook URL or bot token
        if webhook_url_or_token.startswith("https://discord.com/api/webhooks/"):
            # It's a webhook URL - use lightweight method
            self.webhook = DiscordWebhook(webhook_url_or_token)
            self.is_ready = True
            self.use_webhook = True
            print("✅ Using lightweight webhook method (no discord.py needed)")
        else:
            # It's a bot token - need discord.py
            print("⚠️ Bot token detected - discord.py required")
            print("   Switch to webhook URL for lightweight version!")
            self.webhook = None
            self.is_ready = False
            self.use_webhook = False

    async def start_bot(self):
        """Compatibility method - webhooks don't need to start"""
        if self.use_webhook:
            # Test connection
            if self.webhook.test_connection():
                print("✅ Webhook connection successful")
            else:
                print("❌ Webhook connection failed")
        pass

    def send_ocr_result(self, text):
        """Send OCR result to Discord"""
        if self.use_webhook and self.webhook:
            self.webhook.send_ocr_result(text)
        else:
            print("❌ Discord not properly initialized")

    async def stop_bot(self):
        """Compatibility method"""
        pass


if __name__ == "__main__":
    # Example usage
    print("=" * 50)
    print("Discord Webhook Example")
    print("=" * 50)

    # Replace with your actual webhook URL
    WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

    webhook = DiscordWebhook(WEBHOOK_URL)

    # Test message
    webhook.send_ocr_result("Test OCR result from lightweight webhook!")

    # Keep alive for a moment
    time.sleep(2)

    print("\nWebhook test complete!")
