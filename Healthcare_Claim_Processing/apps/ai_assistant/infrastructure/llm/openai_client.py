from openai import AsyncOpenAI


class OpenAIClient:

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5",
    ):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def chat(
        self,
        messages,
        tools=None,
        temperature=0.2,
        max_tokens=1024,
    ):
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            tools=tools,
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )

        return response