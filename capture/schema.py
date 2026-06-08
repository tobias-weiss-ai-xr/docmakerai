"""Pydantic v2 data models for the capture layer."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class StepAction(str, Enum):
    """Supported Playwright actions for a workflow step."""

    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    WAIT = "wait"
    WAIT_FOR_SELECTOR = "wait_for_selector"
    SCREENSHOT = "screenshot"
    FILL_FORM = "fill_form"
    SELECT_OPTION = "select_option"


class WorkflowStep(BaseModel):
    """A single step within a capture workflow."""

    id: str = Field(description="Unique identifier for the step within the workflow")
    action: StepAction = Field(description="Playwright action to perform")
    selector: Optional[str] = Field(None, description="CSS selector for the target element")
    value: Optional[str] = Field(None, description="Value to type or select")
    url: Optional[str] = Field(None, description="URL or path for navigate actions")
    description: str = Field(description="User-facing description of what this step does")
    screenshot: bool = Field(True, description="Whether to capture a screenshot after the action")
    wait_after: Optional[int] = Field(None, description="Milliseconds to wait after action")
    tip: Optional[str] = Field(None, description="Optional tip shown in the generated tutorial")


class Workflow(BaseModel):
    """A complete capture workflow definition, loaded from a YAML file."""

    name: str = Field(description="Human-readable workflow name")
    description: str = Field(description="Description of what this workflow covers")
    base_url: str = Field(description="Base URL of the target web application")
    steps: list[WorkflowStep] = Field(description="Ordered list of steps to execute")


class StepResult(BaseModel):
    """Result of executing a single workflow step."""

    id: str = Field(description="Step identifier (matches WorkflowStep.id)")
    action: str = Field(description="Action that was performed")
    url: Optional[str] = Field(None, description="Page URL after the step")
    description: str = Field(description="Step description")
    screenshot_path: Optional[str] = Field(None, description="Path to saved screenshot")
    selector: Optional[str] = Field(None, description="CSS selector used (if applicable)")
    success: bool = Field(description="Whether the step completed successfully")
    error: Optional[str] = Field(None, description="Error message if the step failed")


class CaptureResult(BaseModel):
    """Complete result of running a capture workflow."""

    workflow_name: str = Field(description="Name of the workflow that was executed")
    base_url: str = Field(description="Base URL used during capture")
    timestamp: str = Field(description="ISO 8601 timestamp of capture start")
    duration_ms: int = Field(description="Total duration of the capture in milliseconds")
    steps: list[StepResult] = Field(description="Results for each step in the workflow")
    output_dir: str = Field(description="Directory where capture artifacts are stored")

    @classmethod
    def new(cls, workflow: Workflow, output_dir: str) -> "CaptureResult":
        """Create a new CaptureResult with current timestamp."""
        return cls(
            workflow_name=workflow.name,
            base_url=workflow.base_url,
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=0,
            steps=[],
            output_dir=output_dir,
        )
