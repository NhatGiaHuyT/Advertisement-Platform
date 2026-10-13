from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RawPassword:
    value: str

    def __post_init__(self) -> None:
        value = self.value.encode("utf-8")

        if " " in self.value:
            raise ValueError("Password cannot have whitespaces.")

        if not self.value:
            raise ValueError("Password cannot be empty.")

        if len(self.value) < 8:
            raise ValueError(
                "Password must be at least 8 characters."
            )

        if len(self.value) > 64:
            raise ValueError(
                "Password cannot be longer than 64 characters."
            )
            
        object.__setattr__(self, "value", value)
