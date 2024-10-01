import time

import openai
import pydantic
from openai import OpenAI

client = OpenAI(
    api_key="examplekey01",
    base_url="http://129.40.60.17:8080",
    default_headers={
        "Content-Type": "application/json",
    },
)


class Statistics(pydantic.BaseModel):
    prompt_n: int
    prompt_ms: float
    prompt_per_token_ms: float
    prompt_per_second: float
    predicted_n: int
    predicted_ms: float
    predicted_per_token_ms: float
    predicted_per_second: float


def print_statistics(response: openai.Completion, delta: float):
    statistics = Statistics(**response.timings)

    print(f"Answer: {response.content}")
    print(f"Prompt tokens: {statistics.prompt_n}")
    print(f"Predicted tokens: {statistics.predicted_n}")
    print(f"Total tokens: {statistics.prompt_n + statistics.predicted_n}")
    print(f"Prompt tokens/s: {statistics.prompt_per_second}")
    print(f"Prediction tokens/s: {statistics.predicted_per_second}")
    print(f"Total tokens/s (server): {(statistics.prompt_n + statistics.predicted_n) / (statistics.prompt_ms + statistics.predicted_ms) * 1000}")
    print(f"Total tokens/s (self): {(statistics.prompt_n + statistics.predicted_n) / delta}")


def main():
    prompt = input("Prompt: ")
    if not prompt:
        prompt = "Question: What is the capital city of Germany? Answer: "

    print(f"Prompt: {prompt}")

    start = time.time()
    print("Started...")
    response = client.completions.create(
        prompt=prompt,
        model="",
        max_tokens=100
    )
    end = time.time()
    print("Done.")
    print("="*20)
    delta = end - start

    print_statistics(response, delta)


if __name__ == "__main__":
    main()
