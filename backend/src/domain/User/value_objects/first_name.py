from dataclasses import dataclass
import unicodedata
import regex

_FIRST_NAME_PATTERN = regex.compile(r"^[\p{L}\s'-]+$")

@dataclass(frozen=True, slots=True)
class FirstName:
    value: str

    def __post_init__(self):
        value = self.value.strip()
        value = unicodedata.normalize('NFC', value)
        
        if not self.value:
            raise ValueError("First name cannot be empty.")

        if len(self.value) > 50:
            raise ValueError("First name cannot be longer than 50 characters.")

        if not _FIRST_NAME_PATTERN.match(value):
            raise ValueError("First name can only contain letters, spaces, hyphens, or apostrophes.")

        object.__setattr__(self, "value", value)
        