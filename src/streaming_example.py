import argparse
import configparser
import time
from pathlib import Path

from openai import OpenAI


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

    print(f"Prompt: \n\n{prompt}")
    print("="*20)
    print("Started...")
    print("="*20)

    start = time.time()
    response = client.completions.create(
        prompt=prompt,
        model="",
        max_tokens=max_tokens,
        timeout=timeout,
        stream=True,
    )

    for chunk in response:
        print(chunk.content, end="", flush=True)
    
    end = time.time()
    print("\n")
    print("="*20)
    print("Done.")
    print("="*20)
    delta = end - start
    print(f"Time: {delta} sec.")


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.config_path, args.prompt_file, args.max_tokens, args.timeout)
