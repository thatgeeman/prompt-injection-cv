import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


def get_client():
    """Load the API key from the .env file and return the client."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set the GOOGLE_API_KEY environment variable."
        )
    return genai.Client(api_key=api_key)


def load_system_prompt():
    path = Path(__file__).parent.parent.parent / "prompts" / "system_instruction.md"
    if not path.exists():
        raise FileNotFoundError(f"System instruction file not found at {path}")
    return path.read_text(encoding="utf-8")


def load_user_prompt():
    path = Path(__file__).parent.parent.parent / "prompts" / "user_instruction.md"
    if not path.exists():
        raise FileNotFoundError(f"User instruction file not found at {path}")
    return path.read_text(encoding="utf-8")


def get_thinking_config(include_thoughts):
    """Get the thinking configuration for the model."""
    return types.ThinkingConfig(
        include_thoughts=include_thoughts,
        thinking_budget=1000,  # maximum number of tokens for thinking
    )


def get_config(include_thoughts=False):
    """Get the configuration for the model."""

    sytem_prompt = load_system_prompt()
    user_prompt = load_user_prompt()

    system_instruction = f"""
    <SYSTEM>
    {sytem_prompt}
    </SYSTEM>

    <USER>
    {user_prompt}
    </USER>
    """

    return types.GenerateContentConfig(
        system_instruction=system_instruction,
        max_output_tokens=5000,
        top_k=1,
        top_p=1,
        temperature=0,
        response_mime_type="application/json",
        # stop_sequences=["<|endoftext|>"],
        candidate_count=1,  # Generate a single response
        thinking_config=get_thinking_config(include_thoughts=include_thoughts),
        # response_json_schema= # for structured output  [JSON Schema](https://json-schema.org/)
        seed=42,
    )
