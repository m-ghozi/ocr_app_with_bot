"""
Simple Real-Time OCR Application with Discord Integration - PORTABLE VERSION
Captures a customizable screen area and performs OCR in real-time.
Works on Windows - No Tesseract installation required!
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


# Auto-detect Tesseract path (portable or installed)
def get_tesseract_path():
    """Auto-detect Tesseract executable path"""
    # Check if running as bundled EXE
    if getattr(sys, "frozen", False):
        # Running as EXE - check for bundled Tesseract
        exe_dir = os.path.dirname(sys.executable)
        portable_tesseract = os.path.join(exe_dir, "tesseract", "tesseract.exe")

        if os.path.exists(portable_tesseract):
            print(f"✅ Using portable Tesseract: {portable_tesseract}")
            return portable_tesseract

    # Check script directory for portable Tesseract
    script_dir = os.path.dirname(os.path.abspath(__file__))
    portable_tesseract = os.path.join(script_dir, "tesseract", "tesseract.exe")

    if os.path.exists(portable_tesseract):
        print(f"✅ Using portable Tesseract: {portable_tesseract}")
        return portable_tesseract

    # Default installation path
    default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_path):
        print(f"✅ Using installed Tesseract: {default_path}")
        return default_path

    # Not found - will use system PATH
    print("⚠️  Tesseract not found, using system PATH")
    return "tesseract"


# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

# Config file untuk menyimpan Discord settings
CONFIG_FILE = "ocr_config.json"

# Import Discord bot (webhook-based, lightweight)
try:
    from discord_webhook import DiscordOCRBot

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("ℹ️  discord_bot.py not found or import error")


class OCRConfig:
    """Configuration settings for the OCR application"""

    def __init__(self):
        self.capture_interval = 1.0  # seconds between captures
        self.tesseract_config = "--psm 6"  # Page segmentation mode


class CaptureArea:
    """Manages the screen capture area coordinates"""

    def __init__(self, x=215, y=60, width=973, height=160):
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
        self.root.title("OCR App - PORTABLE")

        # Sesuaikan tinggi window berdasarkan ketersediaan Discord
        height = "515" if DISCORD_AVAILABLE else "400"
        self.root.geometry(f"500x{height}")

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

        # Load saved config
        self.load_config()

    def load_config(self):
        """Load all settings from config file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)

                if DISCORD_AVAILABLE:
                    # Load Discord settings
                    if "token" in config and config["token"]:
                        self.token_var.set(config["token"])
                        print("✅ Discord webhook/token loaded")

                    if "channel_id" in config and config["channel_id"]:
                        self.channel_id_var.set(config["channel_id"])
                        print("✅ Channel ID loaded")

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
                    print("✅ Capture area settings loaded")

        except Exception as e:
            print(f"⚠️  Error loading config: {e}")

    def save_config(self):
        """Save all settings to config file"""
        try:
            config = {}

            # Save Discord settings if available
            if DISCORD_AVAILABLE:
                config["token"] = self.token_var.get().strip()
                config["channel_id"] = self.channel_id_var.get().strip()

            # Save capture area
            config["capture_area"] = {
                "x": self.x_var.get(),
                "y": self.y_var.get(),
                "width": self.width_var.get(),
                "height": self.height_var.get(),
            }

            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)

            print("✅ Config saved")
        except Exception as e:
            print(f"⚠️  Error saving config: {e}")

    def save_capture_area_config(self):
        """Save only capture area settings"""
        try:
            # Load existing config
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

            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)

            print("✅ Capture area saved")
        except Exception as e:
            print(f"⚠️  Error saving capture area: {e}")

    def clear_discord_config(self):
        """Clear Discord settings but keep capture area"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)

                # Clear only Discord settings
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

        # Configure grid weights
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

            # Channel ID
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

        # Status label
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

        # Auto-save
        self.save_capture_area_config()

    def toggle_overlay(self):
        """Shows or hides the capture area overlay"""
        if self.overlay.window:
            self.overlay.hide()
            self.overlay_button.config(text="👁 Show Overlay")
        else:
            self.overlay.show()
            self.overlay_button.config(text="👁 Hide Overlay")

    def connect_discord(self):
        """Connect to Discord"""
        if not DISCORD_AVAILABLE:
            print("❌ discord_bot.py not available!")
            return

        credential = self.token_var.get().strip()
        channel_id_str = self.channel_id_var.get().strip()

        if not credential:
            print("❌ Webhook URL or Token is empty!")
            self.discord_status.config(
                text="● Error - Missing credential", foreground="red"
            )
            return

        # Detect if webhook or bot token
        is_webhook = credential.startswith("https://discord.com/api/webhooks/")

        if not is_webhook and not channel_id_str:
            print("❌ Channel ID required for bot token!")
            self.discord_status.config(
                text="● Error - Need Channel ID", foreground="red"
            )
            return

        print(f"🔄 Connecting to Discord...")

        # Save config
        self.save_config()

        # Create Discord bot
        try:
            if is_webhook:
                self.discord_bot = DiscordOCRBot(credential)
            else:
                channel_id = int(channel_id_str)
                self.discord_bot = DiscordOCRBot(credential, channel_id)
        except ValueError:
            print("❌ Invalid Channel ID!")
            self.discord_status.config(
                text="● Error - Invalid Channel ID", foreground="red"
            )
            return
        except Exception as e:
            print(f"❌ Error creating Discord bot: {e}")
            self.discord_status.config(text="● Connection Failed", foreground="red")
            return

        # Start bot in background thread
        def start_bot_thread():
            try:
                asyncio.run(self.discord_bot.start_bot())
            except Exception as e:
                print(f"❌ Error starting Discord: {e}")
                self.root.after(
                    0,
                    lambda: self.discord_status.config(
                        text="● Connection Failed", foreground="red"
                    ),
                )

        threading.Thread(target=start_bot_thread, daemon=True).start()

        # Check status
        self.root.after(2000, self.check_discord_status)
        self.discord_status.config(text="● Connecting...", foreground="orange")
        self.discord_connect_button.config(state="disabled")

    def check_discord_status(self):
        """Check if Discord is connected"""
        if self.discord_bot and self.discord_bot.is_ready:
            self.discord_enabled = True
            self.discord_status.config(text="● Connected", foreground="green")
            print("✅ Discord connected!")
        else:
            self.discord_status.config(text="● Connecting...", foreground="orange")
            self.root.after(1500, self.check_discord_status)

    def start_ocr(self):
        """Starts the OCR capture loop"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="● Running", foreground="green")

            # Start capture thread
            self.capture_thread = threading.Thread(target=self.ocr_loop, daemon=True)
            self.capture_thread.start()

            print("\n" + "=" * 50)
            print("OCR Started")
            if self.discord_enabled:
                print("Discord: Enabled ✅")
            print("=" * 50 + "\n")

    def stop_ocr(self):
        """Stops the OCR capture loop"""
        if self.is_running:
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="● Stopped", foreground="orange")

            print("\n" + "=" * 50)
            print("OCR Stopped")
            print("=" * 50 + "\n")

    def ocr_loop(self):
        """Main OCR loop running in separate thread"""
        while self.is_running:
            # Capture and read text
            text = self.ocr_engine.capture_and_read(self.capture_area)

            # Only process if text has changed
            if text and self.ocr_engine.has_text_changed(text):
                print("\n--- OCR Output ---")
                print(text)
                print("------------------\n")

                # Send to Discord if enabled
                if self.discord_enabled and self.discord_bot:
                    try:
                        self.discord_bot.send_ocr_result(text)
                    except Exception as e:
                        print(f"❌ Error sending to Discord: {e}")

            # Wait before next capture
            time.sleep(self.config.capture_interval)

    def on_closing(self):
        """Cleanup when closing the application"""
        print("🔄 Closing application...")

        # Stop OCR
        self.stop_ocr()

        # Hide overlay
        self.overlay.hide()

        # Discord cleanup (webhook doesn't need async cleanup)
        if self.discord_bot:
            print("🔴 Discord disconnected")

        # Destroy window
        self.root.destroy()
        print("✅ Application closed")


def main():
    """Main entry point"""
    print("=" * 50)
    print("OCR App - PORTABLE VERSION")
    print("=" * 50)

    if not DISCORD_AVAILABLE:
        print("\n⚠️  Discord features not available")
        print("   Make sure discord_bot.py is in the same folder\n")

    root = tk.Tk()
    app = OCRApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
