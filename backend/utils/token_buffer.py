import re
from typing import AsyncGenerator

class TokenBuffer:
    def __init__(self, min_words: int = 10, max_words: int = 20):
        self.buffer = ""
        self.word_count = 0
        self.min_words = min_words
        self.max_words = max_words
        # Sentence ending punctuation for Arabic and English
        self.sentence_end_pattern = re.compile(r'[.!؟?؛\n]')

    async def add_token(self, token: str) -> str | None:
        """Adds a token to the buffer. Returns a chunk if criteria are met, else None."""
        self.buffer += token
        
        # Count words (simple split by whitespace)
        words = token.strip().split()
        if words:
            self.word_count += len(words)

        # Check for sentence end or max words
        if self.word_count >= self.min_words:
            if self.sentence_end_pattern.search(token) or self.word_count >= self.max_words:
                chunk = self.buffer.strip()
                self.buffer = ""
                self.word_count = 0
                return chunk
        
        return None

    def flush(self) -> str | None:
        """Returns the remaining content in the buffer."""
        if self.buffer.strip():
            chunk = self.buffer.strip()
            self.buffer = ""
            self.word_count = 0
            return chunk
        return None
