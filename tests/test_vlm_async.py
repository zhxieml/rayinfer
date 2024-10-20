import asyncio
import base64
import time

import aiohttp
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
from tqdm.asyncio import tqdm_asyncio

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

async_client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

model = "microsoft/Phi-3.5-vision-instruct"

# Single-image input inference
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

semaphore = asyncio.Semaphore(100)

async def encode_image_base64_from_url(image_url: str) -> str:
    """Encode an image retrieved from a remote url to base64 format."""
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            response.raise_for_status()
            content = await response.read()
            result = base64.b64encode(content).decode("utf-8")
    return result


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def run_chat_completion(messages):
    async with semaphore:
        chat_completion = await async_client.chat.completions.create(
            messages=messages,
            model=model,
            max_tokens=64,
        )
    return chat_completion.choices[0].message.content


async def run_test(messages, test_name, num_iterations=5000):
    start_time = time.time()
    tasks = [run_chat_completion(messages) for _ in range(num_iterations)]

    test_res = await tqdm_asyncio.gather(*tasks, desc="Running test")

    end_time = time.time()
    total_time = end_time - start_time
    print(
        f"\n{test_name} - Total time for {num_iterations} iterations: {total_time:.2f} seconds"
    )
    print(
        f"{test_name} - Average time per iteration: {total_time/num_iterations:.4f} seconds"
    )


async def main():
    # Prepare messages for URL test
    url_messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
            ],
        }
    ]

    # Prepare messages for base64 test
    print("Encoding image to base64...")
    image_base64 = await encode_image_base64_from_url(image_url=image_url)
    base64_messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                },
            ],
        }
    ]

    # Run tests
    print("Starting URL test...")
    await run_test(url_messages, "URL Test")

    print("\nStarting Base64 test...")
    await run_test(base64_messages, "Base64 Test")


if __name__ == "__main__":
    asyncio.run(main())
