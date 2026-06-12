from pathlib import Path


class PromptManager:

    PROMPTS_DIR = Path("app/prompts")

    _cache = {}

    @classmethod
    def load(cls, filename: str) -> str:

        if filename in cls._cache:
            return cls._cache[filename]

        path = cls.PROMPTS_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Prompt not found: {filename}"
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        cls._cache[filename] = content

        return content