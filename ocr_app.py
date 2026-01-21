"""
Simple Real-Time OCR Application with Discord Integration
Captures a customizable screen area and performs OCR in real-time.
Works on Windows!
"""

import asyncio
import json
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk

import pytesseract
from PIL import ImageGrab

# Windows-specific: Set tesseract path if needed
# Uncomment and adjust path if you get "tesseract not found" error
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Config file untuk menyimpan Discord settings
CONFIG_FILE = "ocr_config.json"

# Import Discord bot (akan gagal secara graceful jika discord.py belum terinstall)
try:
    # from discord_bot import DiscordOCRBot     # Bot Version
    from discord_webhook import DiscordOCRBot  # Webhook Version

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("ℹ️  discord.py belum terinstall. Fitur Discord dinonaktifkan.")
    print("   Install dengan: pip install discord.py")


class OCRConfig:
    """Configuration settings for the OCR application"""

    def __init__(self):
        self.capture_interval = 1.0  # seconds between captures
        self.tesseract_config = "--psm 6"  # Page segmentation mode


class CaptureArea:
    """Manages the screen capture area coordinates"""

    def __init__(self, x=215, y=40, width=973, height=160):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_bbox(self):
        """Returns bounding box tuple for PIL ImageGrab"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def update(self, x, y, width, height):
        """Update capture area coordinates"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class OCREngine:
    """Handles OCR processing"""

    def __init__(self, config):
        self.config = config
        self.last_text = ""

    def capture_and_read(self, capture_area):
        """Captures screen area and performs OCR"""
        try:
            # Capture the screen area
            screenshot = ImageGrab.grab(bbox=capture_area.get_bbox())

            # Perform OCR
            text = pytesseract.image_to_string(
                screenshot, config=self.config.tesseract_config
            )

            # Clean up the text
            text = text.strip()

            return text
        except Exception as e:
            return f"Error: {str(e)}"

    def has_text_changed(self, new_text):
        """Check if text has changed since last capture"""
        changed = new_text != self.last_text
        self.last_text = new_text
        return changed


class OverlayWindow:
    """Visual overlay to show capture area"""

    def __init__(self, capture_area):
        self.capture_area = capture_area
        self.window = None

    def show(self):
        """Display the overlay window"""
        self.window = tk.Toplevel()
        self.window.attributes("-topmost", True)
        self.window.overrideredirect(True)

        # Windows-specific transparency
        if sys.platform == "win32":
            self.window.attributes("-transparentcolor", "white")
            self.window.attributes("-alpha", 0.3)
        else:
            self.window.attributes("-alpha", 0.3)

        # Set window background color
        self.window.configure(bg="red")

        # Position and size the overlay
        self.update_position()

    def update_position(self):
        """Update overlay position based on capture area"""
        if self.window:
            self.window.geometry(
                f"{self.capture_area.width}x{self.capture_area.height}"
                f"+{self.capture_area.x}+{self.capture_area.y}"
            )

    def hide(self):
        """Hide the overlay window"""
        if self.window:
            self.window.destroy()
            self.window = None


class OCRApp:
    """Main application class"""

    def __init__(self, root):
        self.root = root
        self.root.title("Simple OCR App with Discord")

        # Sesuaikan tinggi window berdasarkan ketersediaan Discord
        height = "530" if DISCORD_AVAILABLE else "350"
        self.root.geometry(f"450x{height}")

        # Initialize components
        self.config = OCRConfig()
        self.capture_area = CaptureArea()
        self.ocr_engine = OCREngine(self.config)
        self.overlay = OverlayWindow(self.capture_area)

        # Discord bot components
        self.discord_bot = None
        self.discord_enabled = False

        # State variables
        self.is_running = False
        self.capture_thread = None

        # Build GUI
        self.build_gui()

        # Load saved Discord config
        self.load_discord_config()

    def load_discord_config(self):
        """Load Discord token and channel ID from config file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)

                if DISCORD_AVAILABLE:
                    # Load token and channel ID into GUI
                    if "token" in config and config["token"]:
                        self.token_var.set(config["token"])
                        print("✅ Discord token loaded from config")

                    if "channel_id" in config and config["channel_id"]:
                        self.channel_id_var.set(config["channel_id"])
                        print("✅ Discord channel ID loaded from config")

                # Load capture area settings
                if "capture_area" in config:
                    area = config["capture_area"]
                    if "x" in area:
                        self.x_var.set(area["x"])
                        self.capture_area.x = area["x"]
                    if "y" in area:
                        self.y_var.set(area["y"])
                        self.capture_area.y = area["y"]
                    if "width" in area:
                        self.width_var.set(area["width"])
                        self.capture_area.width = area["width"]
                    if "height" in area:
                        self.height_var.set(area["height"])
                        self.capture_area.height = area["height"]
                    print("✅ Capture area settings loaded from config")

        except Exception as e:
            print(f"⚠️  Error loading config: {e}")

    def save_discord_config(self):
        """Save Discord token and channel ID to config file"""
        try:
            config = {
                "token": self.token_var.get().strip(),
                "channel_id": self.channel_id_var.get().strip(),
                "capture_area": {
                    "x": self.x_var.get(),
                    "y": self.y_var.get(),
                    "width": self.width_var.get(),
                    "height": self.height_var.get(),
                },
            }

            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)

            print("✅ Discord config saved")
        except Exception as e:
            print(f"⚠️  Error saving config: {e}")

    def clear_discord_config(self):
        """Clear saved Discord config"""
        try:
            if os.path.exists(CONFIG_FILE):
                # Load config to preserve capture area if user wants
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)

                # Keep capture area, only clear Discord settings
                config["token"] = ""
                config["channel_id"] = ""

                with open(CONFIG_FILE, "w") as f:
                    json.dump(config, f, indent=2)

                print("✅ Discord config cleared (capture area preserved)")

            # Clear GUI fields
            if DISCORD_AVAILABLE:
                self.token_var.set("")
                self.channel_id_var.set("")

        except Exception as e:
            print(f"⚠️  Error clearing config: {e}")

    def build_gui(self):
        """Constructs the GUI elements"""
        # Title
        title_label = ttk.Label(
            self.root, text="Real-Time OCR Screen Reader", font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)

        # Capture Area Settings Frame
        settings_frame = ttk.LabelFrame(
            self.root, text="Capture Area Settings", padding=10
        )
        settings_frame.pack(padx=10, pady=5, fill="x")

        # X Position
        ttk.Label(settings_frame, text="X Position:").grid(
            row=0, column=0, sticky="w", pady=2, padx=(0, 5)
        )
        self.x_var = tk.IntVar(value=self.capture_area.x)
        ttk.Spinbox(
            settings_frame, from_=0, to=5000, textvariable=self.x_var, width=12
        ).grid(row=0, column=1, pady=2, sticky="ew")

        # Y Position
        ttk.Label(settings_frame, text="Y Position:").grid(
            row=0, column=2, sticky="w", pady=2, padx=(15, 5)
        )
        self.y_var = tk.IntVar(value=self.capture_area.y)
        ttk.Spinbox(
            settings_frame, from_=0, to=5000, textvariable=self.y_var, width=12
        ).grid(row=0, column=3, pady=2, sticky="ew")

        # Width
        ttk.Label(settings_frame, text="Width:").grid(
            row=1, column=0, sticky="w", pady=2, padx=(0, 5)
        )
        self.width_var = tk.IntVar(value=self.capture_area.width)
        ttk.Spinbox(
            settings_frame, from_=50, to=5000, textvariable=self.width_var, width=12
        ).grid(row=1, column=1, pady=2, sticky="ew")

        # Height
        ttk.Label(settings_frame, text="Height:").grid(
            row=1, column=2, sticky="w", pady=2, padx=(15, 5)
        )
        self.height_var = tk.IntVar(value=self.capture_area.height)
        ttk.Spinbox(
            settings_frame, from_=50, to=5000, textvariable=self.height_var, width=12
        ).grid(row=1, column=3, pady=2, sticky="ew")

        # Update button - full width
        ttk.Button(
            settings_frame, text="Update Area", command=self.update_capture_area
        ).grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

        # Configure grid weights for responsive layout
        settings_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(3, weight=1)

        # Discord Settings Frame
        if DISCORD_AVAILABLE:
            discord_frame = ttk.LabelFrame(
                self.root, text="Discord Settings (Optional)", padding=10
            )
            discord_frame.pack(padx=10, pady=5, fill="x")

            # Webhook URL / Bot Token
            ttk.Label(discord_frame, text="Webhook URL / Bot Token:").grid(
                row=0, column=0, sticky="w", pady=(0, 5)
            )
            self.token_var = tk.StringVar()
            token_entry = ttk.Entry(
                discord_frame, textvariable=self.token_var, show="*"
            )
            token_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

            # Channel ID (optional for webhook)
            ttk.Label(discord_frame, text="Channel ID (optional for webhook):").grid(
                row=2, column=0, sticky="w", pady=(0, 5)
            )
            self.channel_id_var = tk.StringVar()
            ttk.Entry(discord_frame, textvariable=self.channel_id_var).grid(
                row=3, column=0, columnspan=2, pady=(0, 10), sticky="ew"
            )

            # Buttons row
            button_container = ttk.Frame(discord_frame)
            button_container.grid(
                row=4, column=0, columnspan=2, pady=(5, 0), sticky="ew"
            )

            self.discord_connect_button = ttk.Button(
                button_container, text="Connect Discord", command=self.connect_discord
            )
            self.discord_connect_button.pack(
                side="left", padx=(0, 5), fill="x", expand=True
            )

            ttk.Button(
                button_container,
                text="Clear Config",
                command=self.clear_discord_config,
            ).pack(side="left", fill="x", expand=True)

            # Discord status
            self.discord_status = ttk.Label(
                discord_frame,
                text="● Not Connected",
                foreground="gray",
                font=("Arial", 9),
            )
            self.discord_status.grid(row=5, column=0, columnspan=2, pady=(10, 0))

            # Configure grid
            discord_frame.columnconfigure(0, weight=1)

        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15, padx=10, fill="x")

        self.start_button = ttk.Button(
            button_frame, text="▶ Start OCR", command=self.start_ocr
        )
        self.start_button.pack(side="left", padx=2, fill="x", expand=True)

        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop OCR",
            command=self.stop_ocr,
            state="disabled",
        )
        self.stop_button.pack(side="left", padx=2, fill="x", expand=True)

        self.overlay_button = ttk.Button(
            button_frame, text="👁 Show Overlay", command=self.toggle_overlay
        )
        self.overlay_button.pack(side="left", padx=2, fill="x", expand=True)

        # Status label with better styling
        self.status_label = ttk.Label(
            self.root, text="● Idle", font=("Arial", 10, "bold"), foreground="#666"
        )
        self.status_label.pack(pady=(5, 2))

        # Info label
        info_text = "OCR output → Terminal" + (
            " & Discord" if DISCORD_AVAILABLE else ""
        )
        info_label = ttk.Label(
            self.root, text=info_text, font=("Arial", 8), foreground="gray"
        )
        info_label.pack(pady=(0, 10))

    def update_capture_area(self):
        """Updates the capture area with new coordinates"""
        self.capture_area.update(
            self.x_var.get(),
            self.y_var.get(),
            self.width_var.get(),
            self.height_var.get(),
        )
        self.overlay.update_position()
        print(f"✅ Capture area updated: {self.capture_area.get_bbox()}")

        # Auto-save capture area settings
        self.save_capture_area_config()

    def save_capture_area_config(self):
        """Save only capture area settings to config"""
        try:
            # Load existing config if exists
            config = {}
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)

            # Update capture area
            config["capture_area"] = {
                "x": self.x_var.get(),
                "y": self.y_var.get(),
                "width": self.width_var.get(),
                "height": self.height_var.get(),
            }

            # Save config
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)

            print("✅ Capture area settings saved")
        except Exception as e:
            print(f"⚠️  Error saving capture area: {e}")

    def toggle_overlay(self):
        """Shows or hides the capture area overlay"""
        if self.overlay.window:
            self.overlay.hide()
            self.overlay_button.config(text="Show Overlay")
        else:
            self.overlay.show()
            self.overlay_button.config(text="Hide Overlay")

    def connect_discord(self):
        """Connect to Discord bot"""
        if not DISCORD_AVAILABLE:
            print("❌ discord.py belum terinstall!")
            return

        token = self.token_var.get().strip()
        channel_id_str = self.channel_id_var.get().strip()

        if not token or not channel_id_str:
            print("❌ Token atau Channel ID kosong!")
            self.discord_status.config(
                text="Discord: Error - Missing info", foreground="red"
            )
            return

        try:
            channel_id = int(channel_id_str)
        except ValueError:
            print("❌ Channel ID harus berupa angka!")
            self.discord_status.config(
                text="Discord: Error - Invalid Channel ID", foreground="red"
            )
            return

        print("🔄 Connecting to Discord...")

        # Save config untuk next time
        self.save_discord_config()

        # Create Discord bot dari discord_bot.py
        self.discord_bot = DiscordOCRBot(token, channel_id)

        # Start bot in background thread
        def start_bot_thread():
            try:
                asyncio.run(self.discord_bot.start_bot())
            except Exception as e:
                print(f"❌ Error starting Discord bot: {e}")
                self.root.after(
                    0,
                    lambda: self.discord_status.config(
                        text="Discord: Connection Failed", foreground="red"
                    ),
                )

        threading.Thread(target=start_bot_thread, daemon=True).start()

        # Wait a bit and check status
        self.root.after(3000, self.check_discord_status)
        self.discord_status.config(text="Discord: Connecting...", foreground="orange")
        self.discord_connect_button.config(state="disabled")

    def check_discord_status(self):
        """Check if Discord bot is connected"""
        if self.discord_bot and self.discord_bot.is_ready:
            self.discord_enabled = True
            self.discord_status.config(text="Discord: ✅ Connected", foreground="green")
            print("✅ Discord bot connected successfully!")
        else:
            self.discord_status.config(
                text="Discord: ⏳ Connecting...", foreground="orange"
            )
            self.root.after(2000, self.check_discord_status)

    def start_ocr(self):
        """Starts the OCR capture loop"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="Status: Running...")

            # Start capture thread
            self.capture_thread = threading.Thread(target=self.ocr_loop, daemon=True)
            self.capture_thread.start()

            print("\n" + "=" * 50)
            print("OCR Started - Reading from screen...")
            if self.discord_enabled:
                print("Discord: Enabled ✅")
            print("=" * 50 + "\n")

    def stop_ocr(self):
        """Stops the OCR capture loop"""
        if self.is_running:
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="Status: Stopped")

            print("\n" + "=" * 50)
            print("OCR Stopped")
            print("=" * 50 + "\n")

    def ocr_loop(self):
        """Main OCR loop running in separate thread"""
        while self.is_running:
            # Capture and read text
            text = self.ocr_engine.capture_and_read(self.capture_area)

            # Only print if text has changed
            if text and self.ocr_engine.has_text_changed(text):
                print("\n--- OCR Output ---")
                print(text)
                print("------------------\n")

                # Send to Discord if enabled (now synchronous!)
                if self.discord_enabled and self.discord_bot:
                    try:
                        self.discord_bot.send_ocr_result(text)
                    except Exception as e:
                        print(f"❌ Error queueing Discord message: {e}")

            # Wait before next capture
            time.sleep(self.config.capture_interval)

    def on_closing(self):
        """Cleanup when closing the application"""
        self.stop_ocr()
        self.overlay.hide()

        # Stop Discord bot if running
        if self.discord_bot:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.discord_bot.stop_bot())
                loop.close()
            except Exception as e:
                print(f"⚠️ Error stopping Discord bot: {e}")

        self.root.destroy()


def main():
    """Main entry point"""
    print("=" * 50)
    print("Simple OCR App with Discord Integration")
    print("=" * 50)

    if not DISCORD_AVAILABLE:
        print("\n⚠️  Discord features tidak tersedia")
        print("   Install dengan: pip install discord.py\n")

    root = tk.Tk()
    app = OCRApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
