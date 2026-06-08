"""Pydantic v2 data models for the generator layer."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class StepResult(BaseModel):
    """Result of a single captured step, matching the capture layer's schema."""

    id: str
    action: str
    url: Optional[str] = None
    description: str
    screenshot_path: Optional[str] = None
    selector: Optional[str] = None
    success: bool
    error: Optional[str] = None


class CaptureResult(BaseModel):
    """Capture result loaded from JSON, consumed by the generator."""

    workflow_name: str
    base_url: str
    timestamp: str
    duration_ms: int
    steps: list[StepResult]
    output_dir: str


class TutorialStep(BaseModel):
    """A single step in the generated tutorial."""

    id: str
    title: str = Field(description="Short, action-oriented title (5-10 words)")
    description: str = Field(description="Detailed step description (2-4 sentences)")
    tip: Optional[str] = Field(None, description="Helpful tip or warning")
    screenshot_path: Optional[str] = Field(None, description="Path to screenshot image")
    expected_outcome: Optional[str] = Field(None, description="What the user should see after this step")


class Tutorial(BaseModel):
    """Complete tutorial ready for template rendering."""

    title: str = Field(description="Tutorial title")
    description: str = Field(description="Short description/abstract")
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")
    date: str = Field(description="ISO 8601 date string")
    introduction: str = Field(description="Introduction section text")
    prerequisites: list[str] = Field(default_factory=list, description="Prerequisite items")
    steps: list[TutorialStep] = Field(description="Ordered tutorial steps")
    workflow_diagram: str = Field(description="Mermaid.js workflow diagram code")
    conclusion: str = Field(description="Conclusion / next steps")

    @classmethod
    def new(cls, title: str, description: str) -> Tutorial:
        return cls(
            title=title,
            description=description,
            date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            introduction="",
            steps=[],
            workflow_diagram="",
            conclusion="",
        )


class ProviderConfig(BaseModel):
    """LLM provider configuration."""

    api_key_env: Optional[str] = None
    api_key: Optional[str] = None
    model: str = "gpt-4o"
    base_url: str = "https://api.openai.com/v1"


class GeneratorConfig(BaseModel):
    """Generator configuration loaded from config/providers.yaml."""

    default_provider: str = "openai"
    providers: dict[str, ProviderConfig] = Field(default_factory=dict)
