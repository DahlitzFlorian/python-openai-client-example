import argparse
import configparser
import time
from pathlib import Path

import openai
import pydantic
from openai import OpenAI


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
    print("="*20)
    print(f"Time: {delta} sec.")
    print(f"Prompt tokens: {statistics.prompt_n}")
    print(f"Predicted tokens: {statistics.predicted_n}")
    print(f"Total tokens: {statistics.prompt_n + statistics.predicted_n}")
    print(f"Prompt tokens/s: {statistics.prompt_per_second}")
    print(f"Prediction tokens/s: {statistics.predicted_per_second}")
    print(f"Total tokens/s (server): {(statistics.prompt_n + statistics.predicted_n) / (statistics.prompt_ms + statistics.predicted_ms) * 1000}")
    print(f"Total tokens/s (self): {(statistics.prompt_n + statistics.predicted_n) / delta}")


def get_parser() -> argparse.ArgumentParser:
    _parser = argparse.ArgumentParser()
    _parser.add_argument(
        "--config-path",
        help="Path to the config file (INI-format)",
        default=Path(__file__).parent / "config.ini",
        type=Path,
    )
    _parser.add_argument(
        "--prompt-file",
        help="Text file to read prompt from",
        default=None,
        type=Path,
    )
    _parser.add_argument(
        "--max-tokens",
        help="Maximum number of tokens",
        default=300,
        type=int,
    )
    _parser.add_argument(
        "--timeout",
        help="Timeout in seconds",
        default=300.0,
        type=float,
    )

    return _parser


def main(config_path: Path, prompt_file: Path, max_tokens: int, timeout: float):
    config = configparser.ConfigParser()
    with open(config_path) as f:
        config.read_file(f)

    client = OpenAI(
        api_key=config["host"]["api_key"],
        base_url=config["host"]["base_url"],
        default_headers={
            "Content-Type": "application/json",
        },
    )
    
    if prompt_file:
        with open(prompt_file) as f:
            prompt = f.read()
    else:
        prompt = input("Prompt: ")

    if not prompt:
        prompt = "Question: What is the capital city of Germany? Answer: "

    print(f"Prompt: {prompt}")

    start = time.time()
    print("Started...")
    response = client.completions.create(
        prompt=prompt,
        model="",
        max_tokens=max_tokens,
        timeout=timeout,
    )
    end = time.time()
    print("Done.")
    print("="*20)
    delta = end - start

    print_statistics(response, delta)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.config_path, args.prompt_file, args.max_tokens, args.timeout)
