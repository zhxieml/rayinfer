# RayInfer: Serving vLLM with Ray for Flexible Inference

## Note
It's now archived - use [`ray.serve.llm`](https://docs.ray.io/en/latest/serve/llm/serving-llms.html) instead!

## Getting Started
Install rayinfer with pip:

```bash
pip install .
```

Launch Ray:
```bash
ray start --head
```

Launch a vLLM server:
```bash
export RAY_RESTART_JOB=0
export RAY_JOB_NAME=vllm
export RAY_ROUTE_PREFIX="/"
export RAY_BLOCKING=0
export RAY_NUM_REPLICAS=8
export RAY_MAX_REQUESTS=100

rayinfer vllm microsoft/Phi-3.5-vision-instruct --trust-remote-code --max-model-len 8192
```

Send a request:
```bash
curl http://localhost:8000/v1/chat/completions   -H "Content-Type: application/json"   -H "Authorization: Bearer $OPENAI_API_KEY"   -d '{
    "model": "microsoft/Phi-3.5-vision-instruct",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What’s in this image?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }'
```
