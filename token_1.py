import re 
from enum import Enum 
from typing import List, Optional, Set
from token_type import TokenType

class Token:
    def __init__(self, type: TokenType, value: Optional[str] = None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"