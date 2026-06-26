from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PIL import Image

from capture.video_pipeline import (
    WorkflowRecorder,
    annotate_frames,
    assemble_webp,
    extract_frames,
    get_video_duration,
    is_frame_valid,
    map_frames_to_steps,
    validate_frames,
)


def _make_step(time_s: float, label: str, **kw) -> dict:
    step = {"time_s": time_s, "label": label, "highlights": []}
    step.update(kw)
    return step


class TestExtractFrames:
    def test_extracts_and_sorts_frames(self, tmp_path: Path):
        video = tmp_path / "video.webm"
        video.write_text("fake")
        out_dir = tmp_path / "frames"
        out_dir.mkdir()

        (out_dir / "f_0002.png").write_text("")
        (out_dir / "f_0001.png").write_text("")
        (out_dir / "f_0010.png").write_text("")
        (out_dir / "f_0003.png").write_text("")

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            result = extract_frames(video, out_dir, fps=10)

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "ffmpeg" in args[0]
        assert "-i" in args
        assert str(video) in args
        assert "fps=10" in " ".join(args)

        assert result == [
            out_dir / "f_0001.png",
            out_dir / "f_0002.png",
            out_dir / "f_0003.png",
            out_dir / "f_0010.png",
        ]

    def test_ffmpeg_failure_raises_error(self, tmp_path: Path):
        video = tmp_path / "video.webm"
        video.write_text("fake")
        out_dir = tmp_path / "frames"

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            from subprocess import CalledProcessError

            mock_run.side_effect = CalledProcessError(1, ["ffmpeg"], stderr="error")
            with pytest.raises(CalledProcessError):
                extract_frames(video, out_dir)

    def test_creates_output_dir(self, tmp_path: Path):
        video = tmp_path / "video.webm"
        video.write_text("fake")
        out_dir = tmp_path / "nonexistent" / "frames"

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            with patch(
                "capture.video_pipeline.Path.glob",
                return_value=[],
            ):
                extract_frames(video, out_dir)

        assert out_dir.exists()


class TestMapFramesToSteps:
    def test_single_frame(self):
        steps = [_make_step(0.0, "Start")]
        result = map_frames_to_steps(1, 10.0, steps)
        assert len(result) == 1
        assert result[0]["frame_idx"] == 0
        assert result[0]["time_s"] == 0.0
        assert result[0]["step_label"] == "Start"

    def test_step_before_and_after_timestamps(self):
        steps = [
            _make_step(2.0, "Middle"),
            _make_step(5.0, "End"),
        ]
        result = map_frames_to_steps(3, 10.0, steps)
        assert len(result) == 3
        assert result[0]["step_label"] == "Middle"
        assert result[1]["step_label"] == "End"
        assert result[2]["step_label"] == "End"

    def test_multiple_frames_multiple_steps(self):
        steps = [
            _make_step(0.0, "Step A"),
            _make_step(3.0, "Step B"),
            _make_step(7.0, "Step C"),
        ]
        result = map_frames_to_steps(5, 10.0, steps)
        assert result[0]["step_label"] == "Step A"
        assert result[1]["step_label"] == "Step A"
        assert result[2]["step_label"] == "Step B"
        assert result[3]["step_label"] == "Step C"
        assert result[4]["step_label"] == "Step C"

    def test_step_number_fallback(self):
        steps = [
            _make_step(0.0, "First"),
            _make_step(5.0, "Second"),
        ]
        for s in steps:
            s.pop("number", None)

        result = map_frames_to_steps(2, 5.0, steps)
        assert result[0]["step_number"] == 1
        assert result[1]["step_number"] == 2

    def test_explicit_step_number(self):
        steps = [
            _make_step(0.0, "First", number=10),
            _make_step(5.0, "Second", number=20),
        ]
        result = map_frames_to_steps(2, 5.0, steps)
        assert result[0]["step_number"] == 10
        assert result[1]["step_number"] == 20

    def test_empty_steps_raises(self):
        with pytest.raises(IndexError):
            map_frames_to_steps(3, 10.0, [])

    def test_zero_frame_count(self):
        steps = [_make_step(0.0, "Only")]
        result = map_frames_to_steps(0, 10.0, steps)
        assert result == []

    def test_highlights_carried_through(self):
        steps = [
            _make_step(0.0, "A", highlights=[{"type": "circle", "x": 10}]),
        ]
        result = map_frames_to_steps(1, 1.0, steps)
        assert result[0]["highlights"] == [{"type": "circle", "x": 10}]


class TestAnnotateFrames:
    def test_annotates_with_valid_mapping(self, tmp_path: Path):
        raw_frames = [
            tmp_path / "f_0001.png",
            tmp_path / "f_0002.png",
        ]
        for f in raw_frames:
            f.write_text("fake-png")

        mapping = [
            {
                "frame_idx": 0,
                "time_s": 0.0,
                "step_label": "Start",
                "step_number": 1,
                "highlights": [],
            },
            {
                "frame_idx": 1,
                "time_s": 1.0,
                "step_label": "End",
                "step_number": 2,
                "highlights": [],
            },
        ]
        annotated_dir = tmp_path / "annotated"

        with patch("capture.video_pipeline.annotate_frame") as mock_af:
            mock_af.return_value = MagicMock()
            result = annotate_frames(raw_frames, mapping, annotated_dir)

        assert len(result) == 2
        assert result[0] == annotated_dir / "f_0001.png"
        assert result[1] == annotated_dir / "f_0002.png"

        assert mock_af.call_count == 2
        assert mock_af.call_args_list[0].args[1] == "Start"
        assert mock_af.call_args_list[0].args[2] == 1

    def test_skips_failed_annotations(self, tmp_path: Path):
        raw_frames = [
            tmp_path / "f_0001.png",
            tmp_path / "f_0002.png",
            tmp_path / "f_0003.png",
        ]
        for f in raw_frames:
            f.write_text("fake-png")

        mapping = [
            {
                "frame_idx": i,
                "time_s": float(i),
                "step_label": "S",
                "step_number": 1,
                "highlights": [],
            }
            for i in range(3)
        ]
        annotated_dir = tmp_path / "annotated"

        with patch("capture.video_pipeline.annotate_frame") as mock_af:
            mock_af.side_effect = [MagicMock(), None, MagicMock()]
            result = annotate_frames(raw_frames, mapping, annotated_dir)

        assert len(result) == 2

    def test_file_count_mismatch_truncates(self, tmp_path: Path):
        raw_frames = [tmp_path / "f_0001.png"]
        raw_frames[0].write_text("fake-png")
        mapping = [
            {"frame_idx": 0, "time_s": 0.0, "step_label": "S", "step_number": 1, "highlights": []},
            {"frame_idx": 1, "time_s": 1.0, "step_label": "T", "step_number": 2, "highlights": []},
        ]
        annotated_dir = tmp_path / "annotated"

        with patch("capture.video_pipeline.annotate_frame") as mock_af:
            mock_af.return_value = MagicMock()
            result = annotate_frames(raw_frames, mapping, annotated_dir)

        assert len(result) == 1


class TestAssembleWebP:
    def test_assembles_with_two_frames(self, tmp_path: Path):
        frame_paths = [tmp_path / f"f_{i:04d}.png" for i in range(2)]
        for fp in frame_paths:
            fp.write_text("fake")

        output_path = tmp_path / "out.webp"

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            output_path.write_text("x" * 200)
            assemble_webp(frame_paths, output_path, fps=12, quality=90)

        assert mock_run.call_count == 3

        first_args = mock_run.call_args_list[0][0][0]
        assert "ffmpeg" in first_args[0]
        assert "drawtext" in str(first_args)

        last_args = mock_run.call_args_list[-1][0][0]
        assert "-framerate" in last_args
        assert "12" in last_args

    def test_keep_frames_preserves_frames(self, tmp_path: Path):
        frame_paths = [tmp_path / f"keep_{i}.png" for i in range(2)]
        for fp in frame_paths:
            fp.write_text("fake")

        output_path = tmp_path / "kept.webp"

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            output_path.write_text("x" * 200)
            assemble_webp(frame_paths, output_path, keep_frames=True)

        for fp in frame_paths:
            assert fp.exists()

    def test_frames_deleted_by_default(self, tmp_path: Path):
        frame_paths = [tmp_path / f"del_{i}.png" for i in range(2)]
        for fp in frame_paths:
            fp.write_text("fake")

        output_path = tmp_path / "deleted.webp"

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            output_path.write_text("x" * 200)
            assemble_webp(frame_paths, output_path, keep_frames=False)

        for fp in frame_paths:
            assert not fp.exists()

    def test_missing_output_raises_runtime_error(self, tmp_path: Path):
        frame_paths = [tmp_path / "err.png"]
        frame_paths[0].write_text("fake")
        output_path = tmp_path / "missing.webp"

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            with pytest.raises(RuntimeError, match="WebP assembly failed"):
                assemble_webp(frame_paths, output_path)

    def test_small_output_raises_runtime_error(self, tmp_path: Path):
        frame_paths = [tmp_path / "small.png"]
        frame_paths[0].write_text("fake")
        output_path = tmp_path / "small.webp"

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            output_path.write_text("x" * 50)
            with pytest.raises(RuntimeError, match="WebP assembly failed"):
                assemble_webp(frame_paths, output_path)


class TestGetVideoDuration:
    def test_returns_duration(self, tmp_path: Path):
        video = tmp_path / "test.webm"
        video.write_text("fake")

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "12.345\n"
            mock_run.return_value = mock_result

            duration = get_video_duration(video)

        assert duration == 12.345
        mock_run.assert_called_once()

    def test_ffprobe_args(self, tmp_path: Path):
        video = tmp_path / "test.webm"
        video.write_text("fake")

        with patch("capture.video_pipeline.subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "5.0\n"
            mock_run.return_value = mock_result

            get_video_duration(video)

        args = mock_run.call_args[0][0]
        assert "ffprobe" in args[0]
        assert str(video) in args


class TestWorkflowRecorder:
    def test_constructor_sets_attributes(self, tmp_path: Path):
        recorder = WorkflowRecorder(
            workflow_name="test_wf",
            video_dir=tmp_path / "videos",
            gif_dir=tmp_path / "gifs",
            fps=15,
            locale="de",
        )
        assert recorder.workflow_name == "test_wf"
        assert recorder.video_dir == tmp_path / "videos"
        assert recorder.gif_dir == tmp_path / "gifs"
        assert recorder.fps == 15
        assert recorder.locale == "de"
        assert recorder.steps == []
        assert recorder._start_time is None
        assert recorder._page_created_time is None

    @pytest.mark.asyncio
    async def test_start_creates_page_and_records_time(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_context.new_page = AsyncMock(return_value=mock_page)
        mock_page.evaluate = AsyncMock(return_value=5000.0)

        page = await recorder.start(mock_context)

        assert page is mock_page
        assert recorder._page_created_time == 5000.0
        mock_context.new_page.assert_awaited_once()
        mock_page.evaluate.assert_awaited_once_with("performance.now()")

    @pytest.mark.asyncio
    async def test_step_records_timestamp_and_label(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")
        recorder._page_created_time = 1000.0

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value=7000.0)

        await recorder.step(mock_page, "My Step", highlights=[{"x": 1}])

        assert len(recorder.steps) == 1
        step = recorder.steps[0]
        assert step["label"] == "My Step"
        assert step["number"] == 1
        assert step["time_s"] == pytest.approx(6.0)
        assert step["highlights"] == [{"x": 1}]

    @pytest.mark.asyncio
    async def test_step_default_highlights_empty_list(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")
        recorder._page_created_time = 1000.0

        mock_page = MagicMock()
        mock_page.evaluate = AsyncMock(return_value=2000.0)

        await recorder.step(mock_page, "No Highlights")

        assert recorder.steps[0]["highlights"] == []

    @pytest.mark.asyncio
    async def test_finish_no_video_returns_none(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        mock_page = AsyncMock()
        mock_page.video = None

        result = await recorder.finish(mock_page)
        assert result is None
        mock_page.close.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_finish_small_video_returns_none(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        video_path = tmp_path / "videos" / "test.webm"
        video_path.parent.mkdir(parents=True)
        video_path.write_text("x" * 500)

        mock_page = AsyncMock()
        mock_page.video = MagicMock()
        mock_page.video.path = AsyncMock(return_value=str(video_path))

        result = await recorder.finish(mock_page)
        assert result is None

    @pytest.mark.asyncio
    async def test_finish_too_few_frames_returns_none(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        video_path = tmp_path / "videos" / "test.webm"
        video_path.parent.mkdir(parents=True)
        video_path.write_text("x" * 2000)

        mock_page = AsyncMock()
        mock_page.video = MagicMock()
        mock_page.video.path = AsyncMock(return_value=str(video_path))

        with patch("capture.video_pipeline.get_video_duration", return_value=5.0):
            with patch("capture.video_pipeline.extract_frames", return_value=[]):
                result = await recorder.finish(mock_page)

        assert result is None

    @pytest.mark.asyncio
    async def test_finish_success_path(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        video_path = tmp_path / "videos" / "test.webm"
        video_path.parent.mkdir(parents=True)
        video_path.write_text("x" * 2000)

        mock_page = AsyncMock()
        mock_page.video = MagicMock()
        mock_page.video.path = AsyncMock(return_value=str(video_path))

        raw_frames = [tmp_path / f"f_{i:04d}.png" for i in range(6)]
        for f in raw_frames:
            f.write_text("fake")
        annotated_frames = [tmp_path / f"a_{i:04d}.png" for i in range(6)]
        for f in annotated_frames:
            f.write_text("fake")

        webp_path = tmp_path / "gifs" / "test.webp"
        webp_path.parent.mkdir(parents=True)
        webp_path.write_text("x" * 200)

        with (
            patch(
                "capture.video_pipeline.get_video_duration",
                return_value=5.0,
            ) as mock_dur,
            patch(
                "capture.video_pipeline.extract_frames",
                return_value=raw_frames,
            ) as mock_extract,
            patch(
                "capture.video_pipeline.validate_frames",
                return_value=(True, ""),
            ) as mock_val,
            patch(
                "capture.video_pipeline.map_frames_to_steps",
                return_value=[{"step_label": "S", "step_number": 1, "highlights": []}] * 6,
            ) as mock_map,
            patch(
                "capture.video_pipeline.annotate_frames",
                return_value=annotated_frames,
            ) as mock_annotate,
            patch("capture.video_pipeline.assemble_webp") as mock_assemble,
        ):
            result = await recorder.finish(mock_page)

        assert result == webp_path
        mock_dur.assert_called_once()
        mock_extract.assert_called_once()
        mock_val.assert_called_once()
        mock_map.assert_called_once()
        mock_annotate.assert_called_once()
        mock_assemble.assert_called_once()

    @pytest.mark.asyncio
    async def test_finish_validation_failure_cleans_up(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        video_path = tmp_path / "videos" / "test.webm"
        video_path.parent.mkdir(parents=True)
        video_path.write_text("x" * 2000)

        mock_page = AsyncMock()
        mock_page.video = MagicMock()
        mock_page.video.path = AsyncMock(return_value=str(video_path))

        raw_frames = [tmp_path / f"f_{i:04d}.png" for i in range(6)]
        for f in raw_frames:
            f.write_text("fake")

        with (
            patch(
                "capture.video_pipeline.get_video_duration",
                return_value=5.0,
            ),
            patch(
                "capture.video_pipeline.extract_frames",
                return_value=raw_frames,
            ),
            patch(
                "capture.video_pipeline.validate_frames",
                return_value=(False, "Frame validation failed"),
            ),
        ):
            result = await recorder.finish(mock_page)

        assert result is None
        mock_page.close.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_finish_duration_below_threshold_returns_none(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        video_path = tmp_path / "videos" / "test.webm"
        video_path.parent.mkdir(parents=True)
        video_path.write_text("x" * 2000)

        mock_page = AsyncMock()
        mock_page.video = MagicMock()
        mock_page.video.path = AsyncMock(return_value=str(video_path))

        with patch("capture.video_pipeline.get_video_duration", return_value=0.3):
            result = await recorder.finish(mock_page)

        assert result is None

    @pytest.mark.asyncio
    async def test_finish_too_few_annotated_frames_cleans_up(self, tmp_path: Path):
        recorder = WorkflowRecorder("test", tmp_path / "videos", tmp_path / "gifs")

        video_path = tmp_path / "videos" / "test.webm"
        video_path.parent.mkdir(parents=True)
        video_path.write_text("x" * 2000)

        mock_page = AsyncMock()
        mock_page.video = MagicMock()
        mock_page.video.path = AsyncMock(return_value=str(video_path))

        raw_frames = [tmp_path / f"f_{i:04d}.png" for i in range(6)]
        for f in raw_frames:
            f.write_text("fake")

        with (
            patch(
                "capture.video_pipeline.get_video_duration",
                return_value=5.0,
            ),
            patch(
                "capture.video_pipeline.extract_frames",
                return_value=raw_frames,
            ),
            patch(
                "capture.video_pipeline.validate_frames",
                return_value=(True, ""),
            ),
            patch(
                "capture.video_pipeline.map_frames_to_steps",
                return_value=[{"step_label": "S", "step_number": 1, "highlights": []}] * 6,
            ),
            patch(
                "capture.video_pipeline.annotate_frames",
                return_value=[],
            ),
        ):
            result = await recorder.finish(mock_page)

        assert result is None
        mock_page.close.assert_awaited_once()


class TestIsFrameValid:
    def test_valid_frame(self, tmp_path: Path):
        fp = tmp_path / "valid.png"
        img = Image.new("L", (10, 10))
        for x in range(10):
            for y in range(10):
                img.putpixel((x, y), x * 25)
        img.save(fp)
        assert is_frame_valid(fp) is True

    def test_single_color_rejected(self, tmp_path: Path):
        for color in (0, 128, 255):
            fp = tmp_path / f"solid_{color}.png"
            Image.new("L", (10, 10), color).save(fp)
            assert is_frame_valid(fp) is False

    def test_near_white_rejected(self, tmp_path: Path):
        fp = tmp_path / "near_white.png"
        img = Image.new("L", (100, 100))
        for y in range(100):
            for x in range(99):
                img.putpixel((x, y), 250)
            img.putpixel((99, y), 128)
        img.save(fp)
        assert is_frame_valid(fp) is False

    def test_near_black_rejected(self, tmp_path: Path):
        fp = tmp_path / "near_black.png"
        img = Image.new("L", (100, 100))
        for y in range(100):
            for x in range(99):
                img.putpixel((x, y), 5)
            img.putpixel((99, y), 128)
        img.save(fp)
        assert is_frame_valid(fp) is False

    def test_low_bright_pixels_rejected(self, tmp_path: Path):
        fp = tmp_path / "low_bright.png"
        img = Image.new("L", (10, 10))
        for y in range(10):
            for x in range(10):
                img.putpixel((x, y), 240 if (x + y) % 2 == 0 else 10)
        img.save(fp)
        assert is_frame_valid(fp) is False

    def test_small_pixel_range_rejected(self, tmp_path: Path):
        fp = tmp_path / "flat.png"
        img = Image.new("L", (10, 10), 100)
        pixels = img.load()
        assert pixels is not None
        for x in range(10):
            for y in range(10):
                pixels[x, y] = 100 + (x + y) % 15
        img.save(fp)
        assert is_frame_valid(fp) is False

    def test_corrupt_file_returns_false(self, tmp_path: Path):
        fp = tmp_path / "corrupt.png"
        fp.write_text("not an image")
        assert is_frame_valid(fp) is False


class TestValidateFrames:
    def test_too_few_frames_rejected(self, tmp_path: Path):
        frames = [tmp_path / f"f_{i}.png" for i in range(3)]
        for f in frames:
            f.write_text("fake")
        valid, msg = validate_frames(frames, "test")
        assert valid is False
        assert "Too few frames" in msg

    def test_sampling_failure_rejected(self, tmp_path: Path):
        frames = [tmp_path / f"f_{i:04d}.png" for i in range(20)]
        for f in frames:
            f.write_text("fake")

        # 3 for check_indices + 9 for sample loop — make 3 fail in sampling
        side_effects = [True] * 3 + [True, True, True, False, True, True, False, True, False]
        with patch(
            "capture.video_pipeline.is_frame_valid",
            side_effect=side_effects,
        ):
            valid, msg = validate_frames(frames, "test")
        assert valid is False
        assert "blank" in msg.lower()

    def test_all_frames_valid(self, tmp_path: Path):
        frames = [tmp_path / f"f_{i:04d}.png" for i in range(10)]
        for f in frames:
            f.write_text("fake")
        with patch("capture.video_pipeline.is_frame_valid", return_value=True):
            valid, msg = validate_frames(frames, "test")
        assert valid is True
        assert msg == ""
