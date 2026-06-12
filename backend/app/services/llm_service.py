import httpx

from models.llm_response import LLMResponse


class LLMService:

    def __init__(
        self,
        model: str = "llama3.2:3b"
    ):

        self.model = model

        self.url = (
            "http://localhost:11434/api/generate"
        )

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_tokens: int = 500
    ) -> LLMResponse:

        try:

            async with httpx.AsyncClient(
                timeout=120.0
            ) as client:

                response = await client.post(
                    self.url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens
                        }
                    }
                )

                response.raise_for_status()

                content = (
                    response.json()
                    .get("response", "")
                    .strip()
                )

                return LLMResponse(
                    success=True,
                    content=content,
                    model=self.model
                )

        except Exception as e:

            return LLMResponse(
                success=False,
                content=str(e),
                model=self.model
            )