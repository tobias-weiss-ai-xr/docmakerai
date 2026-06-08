"""LLM client abstraction for tutorial generation.

Supports any OpenAI-compatible API endpoint (OpenAI, Anthropic via proxy,
Ollama, vLLM, etc.).
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Optional

from openai import OpenAI

from generator.schema import GeneratorConfig, ProviderConfig

SYSTEM_PROMPT = """You are a technical documentation expert. Your task is to analyze web application screenshots and generate clear, educational tutorial content for end users.

For each step in the workflow, provide:
1. A short title (5-10 words) describing the action
2. A detailed description (2-4 sentences) explaining what to do and why
3. A practical tip or warning
4. The expected outcome after completing the step

Write from the perspective of a first-time user. Use simple, direct language.
Assume no prior knowledge of the application.
Focus on the task, not the interface — explain what the user is accomplishing.
"""


def _encode_image(image_path: str) -> str:
    """Read and base64-encode an image file."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Screenshot not found: {image_path}")
    return base64.b64encode(path.read_bytes()).decode("utf-8")


class LLMClient:
    """Client for OpenAI-compatible LLM APIs."""

    def __init__(self, config: GeneratorConfig) -> None:
        provider_name = config.default_provider
        provider = config.providers.get(provider_name)
        if not provider:
            raise ValueError(f"Provider '{provider_name}' not found in config")

        self._provider = provider
        self._client = self._build_client(provider)

    def _build_client(self, provider: ProviderConfig) -> OpenAI:
        api_key = provider.api_key
        if provider.api_key_env:
            api_key = os.environ.get(provider.api_key_env, api_key or "")
        return OpenAI(api_key=api_key or "sk-placeholder", base_url=provider.base_url)

    @property
    def model(self) -> str:
        return self._provider.model

    def analyze_step_screenshot(
        self,
        screenshot_path: str,
        step_description: str,
        step_action: str,
    ) -> str:
        """Send a screenshot to the LLM and get a natural language analysis."""
        try:
            image_b64 = _encode_image(screenshot_path)
        except FileNotFoundError:
            return self._fallback_description(step_description)

        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"This screenshot shows step '{step_action}': {step_description}\n\n"
                                "Describe what the user sees in this screenshot in 1-2 sentences. "
                                "Focus on the visual elements relevant to the task."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}",
                                "detail": "low",
                            },
                        },
                    ],
                },
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content or ""

    def _fallback_description(self, step_description: str) -> str:
        """Return step description when no screenshot is available."""
        return step_description
