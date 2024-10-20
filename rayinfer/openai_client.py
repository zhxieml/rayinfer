from openai import AsyncAzureOpenAI, AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential


def create_client(api_key, base_url, api_version=None, **kwargs):
    if api_version is None:
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    else:  # use Azure API
        client = AsyncAzureOpenAI(
            azure_endpoint=base_url, api_version=api_version, api_key=api_key
        )

    return client


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def async_chat_api_response(client, messages, **kwargs):
    try:
        response = await client.chat.completions.create(
            messages=messages, stream=False, **kwargs
        )
        if response is not None:
            choices = response.choices

            if len(choices) == 1:
                result = choices[0].message.content
            else:
                result = [c.message.content for c in choices]
        else:
            result = None
        return result

    finally:
        await client.close()
