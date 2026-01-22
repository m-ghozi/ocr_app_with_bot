"""
OCR Output Filter
Filter dan clean OCR output sebelum dikirim ke Discord
Menghilangkan noise, duplicate, dan text yang tidak penting
"""

import re
from datetime import datetime


class OCRFilter:
    """Filter OCR output untuk menghilangkan noise dan duplicate"""

    def __init__(self):
        # Track text yang sudah dikirim untuk avoid duplicate
        self.sent_messages = []
        self.max_history = 50  # Keep last 50 messages

        # Keyword yang ingin di-capture (customize sesuai kebutuhan)
        self.important_keywords = [
            # Game events
            "event",
            "spotted",
            "manifests",
            "emerged",
            "vanished",
            "begun",
            "ended",
            "Aurora Borealis",
            "Megalodon",
            "Cursed Isle",
            "Divine Secret",
            "Sunken",
            "Coral",
            "Omnithal",
            "Awakened Omnithal",
            "Kraken",
            "Narwhal",
            "Statue",
            "fish",
            "Forsaken"
            # Actions
            "used",
            "joined",
            "caught",
            "Totem",
        ]

        # Pattern untuk filter noise
        self.noise_patterns = [
            r"^[^\w\s]+$",  # Hanya simbol
            r"^\s*[.]\s*$",  # Hanya dots
            r"^[a-zA-Z]{1,2}$",  # Single/double char
            r"^\d+$",  # Hanya angka
            r"^[@#$%^&*()]+$",  # Hanya special chars
        ]

        # Minimum length untuk dianggap valid
        self.min_length = 10

        # Save to file options
        self.save_to_file = False
        self.output_file = "ocr_output.txt"

    def is_noise(self, text):
        """Check if text is noise/garbage"""
        # Empty or too short
        if not text or len(text.strip()) < self.min_length:
            return True

        # Check noise patterns
        for pattern in self.noise_patterns:
            if re.match(pattern, text.strip()):
                return True

        # Too many special characters
        special_char_ratio = sum(
            not c.isalnum() and not c.isspace() for c in text
        ) / len(text)
        if special_char_ratio > 0.5:  # More than 50% special chars
            return True

        return False

    def is_duplicate(self, text, threshold=0.8):
        """Check if text is duplicate (similar to recent messages)"""
        text_clean = text.strip().lower()

        for sent_msg in self.sent_messages[-10:]:  # Check last 10 messages
            sent_clean = sent_msg.strip().lower()

            # Exact match
            if text_clean == sent_clean:
                return True

            # Similar match (simple similarity check)
            if len(text_clean) > 20 and len(sent_clean) > 20:
                # Check if one contains the other
                if text_clean in sent_clean or sent_clean in text_clean:
                    return True

        return False

    def has_important_keyword(self, text):
        """Check if text contains important keywords"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.important_keywords)

    def clean_text(self, text):
        """Clean OCR text"""
        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove leading/trailing special chars
        text = text.strip(".,;:!?-_*+=@#$%^&()[]{}|\\/")

        # Remove multiple dots/dashes
        text = re.sub(r"\.{3,}", "...", text)
        text = re.sub(r"-{3,}", "---", text)

        return text.strip()

    def extract_important_lines(self, text):
        """Extract only important lines from multi-line text"""
        lines = text.split("\n")
        important_lines = []

        for line in lines:
            line = line.strip()

            # Skip noise lines
            if self.is_noise(line):
                continue

            # Keep lines with important keywords
            if self.has_important_keyword(line):
                important_lines.append(line)

        return important_lines

    def should_send(self, text):
        """Determine if text should be sent to Discord"""
        # Clean first
        text = self.clean_text(text)

        # Check noise
        if self.is_noise(text):
            return False, "Filtered: Noise"

        # Check duplicate
        if self.is_duplicate(text):
            return False, "Filtered: Duplicate"

        # Check if has important content
        if not self.has_important_keyword(text):
            return False, "Filtered: No important keywords"

        return True, "Passed"

    def filter(self, text, mode="smart"):
        """
        Filter OCR output

        Args:
            text (str): Raw OCR output
            mode (str): Filter mode
                - 'smart': Smart filtering with keywords
                - 'all': Send everything (no filter)
                - 'important': Only send with important keywords
                - 'lines': Extract important lines only

        Returns:
            tuple: (should_send, filtered_text, reason)
        """
        # Mode: All (no filter)
        if mode == "all":
            cleaned = self.clean_text(text)
            if cleaned:
                self._add_to_history(cleaned)
                return True, cleaned, "Mode: All"
            return False, "", "Empty after cleaning"

        # Mode: Important keywords only
        if mode == "important":
            if self.has_important_keyword(text):
                cleaned = self.clean_text(text)
                if cleaned and not self.is_duplicate(cleaned):
                    self._add_to_history(cleaned)
                    return True, cleaned, "Mode: Important"
            return False, "", "No important keywords"

        # Mode: Extract important lines
        if mode == "lines":
            important_lines = self.extract_important_lines(text)
            if important_lines:
                result = "\n".join(important_lines)
                if not self.is_duplicate(result):
                    self._add_to_history(result)
                    return True, result, "Mode: Lines"
            return False, "", "No important lines"

        # Mode: Smart (default)
        should_send, reason = self.should_send(text)
        if should_send:
            cleaned = self.clean_text(text)
            self._add_to_history(cleaned)
            return True, cleaned, reason

        return False, "", reason

    def _add_to_history(self, text):
        """Add text to sent history"""
        self.sent_messages.append(text)

        # Keep only recent messages
        if len(self.sent_messages) > self.max_history:
            self.sent_messages.pop(0)

        # Save to file if enabled
        if self.save_to_file:
            self.save_output(text)

    def save_output(self, text, filename=None):
        """Save OCR output to file"""
        if filename:
            self.output_file = filename

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {text}\n")
        except Exception as e:
            print(f"⚠️  Error saving to file: {e}")

    def enable_file_output(self, filename="ocr_output.txt"):
        """Enable saving output to file"""
        self.save_to_file = True
        self.output_file = filename
        print(f"✅ File output enabled: {filename}")

    def disable_file_output(self):
        """Disable saving output to file"""
        self.save_to_file = False
        print("❌ File output disabled")

    def add_keyword(self, keyword):
        """Add custom important keyword"""
        if keyword not in self.important_keywords:
            self.important_keywords.append(keyword)
            print(f"✅ Added keyword: {keyword}")

    def remove_keyword(self, keyword):
        """Remove keyword"""
        if keyword in self.important_keywords:
            self.important_keywords.remove(keyword)
            print(f"❌ Removed keyword: {keyword}")

    def clear_history(self):
        """Clear sent message history"""
        self.sent_messages.clear()
        print("✅ History cleared")


# Example usage
if __name__ == "__main__":
    # Test filter
    ocr_filter = OCRFilter()

    # Enable file output
    ocr_filter.enable_file_output("test_output.txt")

    # Test cases
    test_texts = [
        "Shiro used a Sundial Totem to speed up the celestial cycle.",
        "Events Catches",  # Noise
        "Divine Secret 1/1000 Aetherfin!.",
        "Shiro used a Sundial Totem to speed up the celestial cycle.",  # Duplicate
        "The Cursed Isle has emerged from the fog!",
        "...",  # Noise
        "A Megalocdon has been spotted past Ancient Isle!",
        "scan chat with you",  # No important keyword
        "âŒ Error in message queue",  # Noise
        "Aurora Borealis! Luck is drastically",
    ]

    print("Testing OCR Filter:")
    print("=" * 60)

    for text in test_texts:
        should_send, filtered, reason = ocr_filter.filter(text, mode="smart")
        status = "✅ SEND" if should_send else "❌ BLOCK"
        print(f"{status} | {reason}")
        print(f"   Input:  {text[:50]}...")
        if filtered:
            print(f"   Output: {filtered[:50]}...")
        print()

    print("=" * 60)
    print(f"Messages in history: {len(ocr_filter.sent_messages)}")
