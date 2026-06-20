# capture-pipeline Specification

> Source files: capture/run_captures.py, capture/video_pipeline.py, capture/annotate.py, capture/capture.py
> Last updated: 2025-06-20

## Purpose

Define the behavior of the SOGo documentation capture pipeline: a Playwright-
driven system that records UI workflows, annotates frames with step indicators
and UI highlights, and outputs WebP animations and PNG screenshots to the
Docusaurus assets directory.

## Requirements

### Requirement: Workflow Recorder

The pipeline SHALL provide a `WorkflowRecorder` class that manages video
recording for a single workflow, including context creation, step tracking,
and WebP assembly.

#### Scenario: Record a workflow

- **GIVEN** a `WorkflowRecorder` instance with a name, video directory, output directory, FPS, and locale
- **WHEN** the recorder starts a browser context with video recording enabled
- **THEN** each call to `rec.step()` SHALL capture the current page state as an annotated frame
- **AND** on `rec.finish()`, the frames SHALL be assembled into a WebP animation

#### Scenario: Step tracking

- **GIVEN** a workflow is being recorded
- **WHEN** `rec.step(page, label, highlights)` is called
- **THEN** the step label SHALL be drawn as a header bar on the frame
- **AND** any highlights (circles, arrows) SHALL be drawn at the specified coordinates
- **AND** the annotated frame SHALL be added to the WebP sequence

### Requirement: Annotation Engine

The pipeline SHALL provide an annotation engine (`annotate.py`) that uses Pillow
to overlay step headers, UI highlights, and fade effects onto captured frames.

#### Scenario: Step header rendering

- **GIVEN** a captured frame and a step label
- **WHEN** the annotation engine processes the frame
- **THEN** a semi-transparent dark bar SHALL be drawn at the top
- **AND** the step number and label SHALL be rendered in white text
- **AND** the bar SHALL cover the full width of the frame

#### Scenario: UI highlight rendering

- **GIVEN** a captured frame and a list of highlight dictionaries
- **WHEN** the annotation engine processes highlights
- **THEN** circles SHALL be drawn as red outlines at the specified bounding boxes
- **AND** arrows SHALL be drawn from the top edge to the target element
- **AND** the highlight color SHALL indicate the interaction type (red=click target, green=result)

#### Scenario: Locale support

- **GIVEN** the annotation locale is set to `de` or `en`
- **WHEN** step labels are rendered
- **THEN** the labels SHALL use the appropriate language
- **AND** two WebP sets MAY be generated (`*-de.webp`, `*-en.webp`)

### Requirement: Asset Output

The pipeline SHALL output WebP animations and PNG screenshots to the
Docusaurus assets directory (`site/docs/assets/`).

#### Scenario: WebP output

- **GIVEN** a workflow has completed recording
- **WHEN** the recorder finishes assembly
- **THEN** the WebP file SHALL be copied to `site/docs/assets/<workflow-name>.webp`
- **AND** a metadata JSON SHALL be written with frame count and file size

#### Scenario: Metadata generation

- **GIVEN** a workflow has produced annotated frames
- **WHEN** the recorder writes metadata
- **THEN** the metadata JSON SHALL contain `annotated_frames` (count) and `webp_size_kb` (size)
- **AND** the metadata SHALL be written to `<video_dir>/<workflow_name>_metadata.json`

### Requirement: Pipeline Orchestration

The pipeline SHALL orchestrate all workflow captures in a single run, sharing
a login session across all workflow contexts.

#### Scenario: Full pipeline run

- **GIVEN** the capture pipeline is started via `python run_captures.py`
- **WHEN** the main function executes
- **THEN** a browser SHALL launch in headless mode
- **AND** a login session SHALL be established and storage state extracted
- **THEN** each workflow in the workflow list SHALL run in its own video-recording context
- **AND** each successful WebP SHALL be copied to the assets directory
- **AND** a results summary SHALL print showing success/failure per workflow

#### Scenario: Sequential execution

- **GIVEN** the workflow list contains 22 workflows
- **WHEN** the pipeline runs
- **THEN** workflows SHALL execute sequentially (one at a time)
- **AND** each workflow SHALL get its own browser context for video isolation

#### Scenario: Error handling

- **GIVEN** a workflow raises an exception during execution
- **WHEN** the exception is caught
- **THEN** the error SHALL be printed
- **AND** the workflow SHALL be marked as failed in the results
- **AND** the pipeline SHALL continue to the next workflow

### Requirement: Capture Quality Validation

The pipeline SHALL detect blank captures (>90% white frames) and report them.

#### Scenario: Blank frame detection

- **GIVEN** a captured frame from a workflow
- **WHEN** the frame is >90% white pixels
- **THEN** the frame SHALL be flagged as blank
- **AND** the workflow SHALL be reported as producing a blank capture

#### Scenario: Known blank captures

- **GIVEN** the following workflows are known to produce blank captures:
  password-change, mail-read, mail-reply-forward-delete, mail-folder-management,
  mail-signatures, preferences, vacation, mail-filters
- **WHEN** the pipeline runs these workflows
- **THEN** the documentation SHALL either use PNG fallbacks or remove image references
- **AND** a capture report SHALL list which workflows produced blanks

### Requirement: Directory Management

The pipeline SHALL manage output directories for videos, GIFs, screenshots,
and assets.

#### Scenario: Clean directories on start

- **GIVEN** the pipeline is starting a fresh run
- **WHEN** `clean_dirs()` is called
- **THEN** the video, GIF, assets, and screenshot directories SHALL be cleared
- **AND** the directories SHALL be recreated

#### Scenario: Asset directory location

- **GIVEN** the pipeline outputs assets
- **WHEN** files are copied to the assets directory
- **THEN** the target SHALL be `site/docs/assets/`
- **AND** the directory SHALL exist before copying

## Technical Notes

- **Implementation**:
  - `capture/run_captures.py` — main orchestrator, workflow functions, login/logout
  - `capture/video_pipeline.py` — `WorkflowRecorder` class, video → frame extraction → WebP assembly
  - `capture/annotate.py` — Pillow annotation engine (step headers, circles, arrows)
  - `capture/capture.py` — legacy capture workflows
- **Dependencies**: playwright, Pillow (PIL), ffmpeg
- **Configuration**: `FPS=6`, `LOCALE="de"`, viewport `1280x800`
- **Current limitations**: Sequential execution only, no retry on failure, blank capture detection is manual
