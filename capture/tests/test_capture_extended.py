import os
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from capture.capture import (
    generate_playwright_script,
    list_workflows,
    load_env,
    main,
    run_all,
    run_workflow,
)


class TestLoadEnv:
    def test_loads_env_file(self, monkeypatch, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("SOGO_URL=https://example.com\nSOGO_USERNAME=admin\n")
        load_env(env_file)
        assert os.environ["SOGO_URL"] == "https://example.com"
        assert os.environ["SOGO_USERNAME"] == "admin"
        monkeypatch.delenv("SOGO_URL", raising=False)
        monkeypatch.delenv("SOGO_USERNAME", raising=False)

    def test_skips_comments(self, monkeypatch, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("# This is a comment\nTEST_KEY=value\n")
        load_env(env_file)
        assert os.environ.get("TEST_KEY") == "value"
        monkeypatch.delenv("TEST_KEY", raising=False)

    def test_skips_blank_lines(self, monkeypatch, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("\n\n\nTEST_KEY=value\n\n")
        load_env(env_file)
        assert os.environ["TEST_KEY"] == "value"
        monkeypatch.delenv("TEST_KEY", raising=False)

    def test_skips_line_without_equals(self, monkeypatch, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("NOT_AN_ASSIGNMENT\nTEST_SKIP_EQ_KEY=value\n")
        load_env(env_file)
        assert os.environ.get("TEST_SKIP_EQ_KEY") == "value"
        assert os.environ.get("NOT_AN_ASSIGNMENT") is None
        monkeypatch.delenv("TEST_SKIP_EQ_KEY", raising=False)

    def test_strips_quotes_from_value(self, monkeypatch, tmp_path):
        monkeypatch.delenv("TEST_QUOTED_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text('TEST_QUOTED_KEY="quoted value"\n')
        load_env(env_file)
        assert os.environ.get("TEST_QUOTED_KEY") == "quoted value"
        monkeypatch.delenv("TEST_QUOTED_KEY", raising=False)

    def test_strips_single_quotes_from_value(self, monkeypatch, tmp_path):
        monkeypatch.delenv("TEST_SINGLE_QUOTED_KEY", raising=False)
        env_file = tmp_path / ".env"
        env_file.write_text("TEST_SINGLE_QUOTED_KEY='single quoted'\n")
        load_env(env_file)
        assert os.environ.get("TEST_SINGLE_QUOTED_KEY") == "single quoted"
        monkeypatch.delenv("TEST_SINGLE_QUOTED_KEY", raising=False)

    def test_does_not_override_existing_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("TEST_KEY", "original")
        env_file = tmp_path / ".env"
        env_file.write_text("TEST_KEY=override\n")
        load_env(env_file)
        assert os.environ["TEST_KEY"] == "original"

    def test_nonexistent_env_path_does_not_error(self):
        load_env(Path("/nonexistent_dir_12345/.env"))

    def test_load_env_without_args(self):
        load_env()

    def test_load_env_without_args_uses_default_path(self, tmp_path, monkeypatch):
        env_file = tmp_path / ".env"
        env_file.write_text("NOARG_KEY=loaded\n")

        mock_resolved_parent = MagicMock()
        mock_resolved_parent.__truediv__.return_value = env_file
        mock_first_parent = MagicMock()
        mock_first_parent.parent = mock_resolved_parent
        mock_self_resolved = MagicMock()
        mock_self_resolved.parent = mock_first_parent
        mock_self = MagicMock()
        mock_self.resolve.return_value = mock_self_resolved

        with patch("capture.capture.Path", return_value=mock_self):
            load_env()

        assert os.environ.get("NOARG_KEY") == "loaded"
        monkeypatch.delenv("NOARG_KEY", raising=False)


class TestGeneratePlaywrightScriptExtended:
    def test_select_action(self):
        workflow = {
            "name": "Select",
            "base_url": "https://example.com",
            "steps": [
                {
                    "id": "choose",
                    "action": "select",
                    "selector": "#dropdown",
                    "value": "option1",
                }
            ],
        }
        script = generate_playwright_script(workflow)
        assert "page.select_option" in script
        assert '"#dropdown"' in script
        assert '"option1"' in script

    def test_toggle_action(self):
        workflow = {
            "name": "Toggle",
            "base_url": "https://example.com",
            "steps": [{"id": "tog", "action": "toggle", "selector": "#checkbox"}],
        }
        script = generate_playwright_script(workflow)
        assert "page.click" in script
        assert "wait_for_timeout(300)" in script

    def test_wait_before(self):
        workflow = {
            "name": "WaitBefore",
            "base_url": "https://example.com",
            "steps": [
                {
                    "id": "step1",
                    "action": "click",
                    "selector": "#btn",
                    "wait_before": 2,
                }
            ],
        }
        script = generate_playwright_script(workflow)
        assert "wait_for_timeout(2000)" in script

    def test_wait_after(self):
        workflow = {
            "name": "WaitAfter",
            "base_url": "https://example.com",
            "steps": [
                {
                    "id": "step1",
                    "action": "click",
                    "selector": "#btn",
                    "wait_after": 3,
                }
            ],
        }
        script = generate_playwright_script(workflow)
        assert "wait_for_timeout(3000)" in script

    def test_wait_before_and_wait_after(self):
        workflow = {
            "name": "WaitBoth",
            "base_url": "https://example.com",
            "steps": [
                {
                    "id": "step1",
                    "action": "click",
                    "selector": "#btn",
                    "wait_before": 2,
                    "wait_after": 5,
                }
            ],
        }
        script = generate_playwright_script(workflow)
        assert "wait_for_timeout(2000)" in script
        assert "wait_for_timeout(5000)" in script

    def test_wait_action(self):
        workflow = {
            "name": "WaitAction",
            "base_url": "https://example.com",
            "steps": [{"id": "pause", "action": "wait", "value": "5"}],
        }
        script = generate_playwright_script(workflow)
        assert "wait_for_timeout(5000)" in script

    def test_wait_action_default_value(self):
        workflow = {
            "name": "WaitDefault",
            "base_url": "https://example.com",
            "steps": [{"id": "pause", "action": "wait", "value": "0"}],
        }
        script = generate_playwright_script(workflow)
        assert "wait_for_timeout(0)" in script

    def test_env_substitution_in_url_and_value(self, monkeypatch):
        monkeypatch.setenv("SOGO_URL", "https://demo.sogo.nu")
        monkeypatch.setenv("SECRET", "supersecret")
        workflow = {
            "name": "EnvSub",
            "base_url": "${SOGO_URL}",
            "steps": [
                {
                    "id": "nav",
                    "action": "navigate",
                    "url": "${SOGO_URL}/login",
                },
                {
                    "id": "type",
                    "action": "type",
                    "selector": "#input",
                    "value": "${SECRET}",
                },
            ],
        }
        script = generate_playwright_script(workflow)
        assert "https://demo.sogo.nu/login" in script
        assert "supersecret" in script

    def test_env_substitution_in_selector_value(self, monkeypatch):
        monkeypatch.setenv("OPTION", "opt2")
        workflow = {
            "name": "SelectEnv",
            "base_url": "https://example.com",
            "steps": [
                {
                    "id": "choose",
                    "action": "select",
                    "selector": "#dropdown",
                    "value": "${OPTION}",
                }
            ],
        }
        script = generate_playwright_script(workflow)
        assert '"opt2"' in script

    def test_screenshot_with_env_substitution(self, monkeypatch):
        monkeypatch.setenv("RUN_ID", "test123")
        workflow = {
            "name": "ScreenshotEnv",
            "base_url": "https://example.com",
            "steps": [
                {
                    "id": "capture",
                    "action": "wait",
                    "value": "1",
                    "screenshot": "shot_${RUN_ID}.png",
                }
            ],
        }
        script = generate_playwright_script(workflow)
        assert "shot_test123.png" in script

    def test_gif_name_on_end_step(self):
        workflow = {
            "name": "Animation",
            "base_url": "https://example.com",
            "steps": [
                {"id": "start", "action": "wait", "value": "1",
                 "gif_start": True},
                {"id": "end", "action": "wait", "value": "1",
                 "gif_end": True, "gif_name": "output.gif"},
            ],
        }
        script = generate_playwright_script(workflow)
        assert 'gif_name = "output.gif"' in script


class TestRunWorkflow:
    def test_valid_workflow(self, monkeypatch, tmp_path):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        screenshots_dir = tmp_path / "screenshots"
        monkeypatch.setattr("capture.capture.SCREENSHOT_DIR", screenshots_dir)

        wf = workflows_dir / "test.yaml"
        wf.write_text(
            yaml.dump(
                {
                    "name": "Test Workflow",
                    "base_url": "https://example.com",
                    "steps": [{"action": "navigate", "url": "/"}],
                }
            )
        )

        with patch(
            "subprocess.run",
            return_value=MagicMock(returncode=0, stdout="Success", stderr=""),
        ) as mock_run:
            result = run_workflow(wf)

        assert result is True
        mock_run.assert_called_once()
        assert (screenshots_dir / "_run_test.py").exists()

    def test_empty_workflow_returns_false(self, monkeypatch, tmp_path):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        monkeypatch.setattr("capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots")

        wf = workflows_dir / "empty.yaml"
        wf.write_text("")

        result = run_workflow(wf)
        assert result is False

    def test_subprocess_failure_returns_false(self, monkeypatch, tmp_path):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        monkeypatch.setattr("capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots")

        wf = workflows_dir / "test.yaml"
        wf.write_text(
            yaml.dump(
                {
                    "name": "Failing Workflow",
                    "base_url": "https://example.com",
                    "steps": [{"action": "navigate", "url": "/"}],
                }
            )
        )

        with patch(
            "subprocess.run",
            return_value=MagicMock(returncode=1, stdout="", stderr="Error occurred"),
        ):
            result = run_workflow(wf)

        assert result is False

    def test_subprocess_timeout_propagates(self, monkeypatch, tmp_path):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        monkeypatch.setattr("capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots")

        wf = workflows_dir / "test.yaml"
        wf.write_text(
            yaml.dump(
                {
                    "name": "Timeout Workflow",
                    "base_url": "https://example.com",
                    "steps": [{"action": "navigate", "url": "/"}],
                }
            )
        )

        with patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="python", timeout=120),
        ):
            with pytest.raises(subprocess.TimeoutExpired):
                run_workflow(wf)

    def test_workflow_with_stderr_output(self, monkeypatch, tmp_path):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        monkeypatch.setattr("capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots")

        wf = workflows_dir / "test.yaml"
        wf.write_text(
            yaml.dump(
                {
                    "name": "Stderr Test",
                    "base_url": "https://example.com",
                    "steps": [{"action": "navigate", "url": "/"}],
                }
            )
        )

        with patch(
            "subprocess.run",
            return_value=MagicMock(
                returncode=0, stdout="Done\n", stderr="Some warning\n"
            ),
        ):
            result = run_workflow(wf)

        assert result is True


class TestListWorkflows:
    def test_lists_workflows(self, monkeypatch, tmp_path, capsys):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)

        (workflows_dir / "wf1.yaml").write_text(
            yaml.dump(
                {"name": "Workflow One", "steps": [{"action": "navigate", "url": "/"}]}
            )
        )
        (workflows_dir / "wf2.yaml").write_text(
            yaml.dump({"name": "Workflow Two", "steps": []})
        )

        list_workflows()
        captured = capsys.readouterr()

        assert "Available workflows" in captured.out
        assert "wf1.yaml" in captured.out
        assert "Workflow One" in captured.out
        assert "wf2.yaml" in captured.out
        assert "Workflow Two" in captured.out

    def test_empty_directory(self, monkeypatch, tmp_path, capsys):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)

        list_workflows()
        captured = capsys.readouterr()

        assert "No workflows found" in captured.out

    def test_lists_workflows_with_empty_yaml(self, monkeypatch, tmp_path, capsys):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)

        (workflows_dir / "empty.yaml").write_text("")

        list_workflows()
        captured = capsys.readouterr()

        assert "empty.yaml" in captured.out
        assert "Name:  N/A" in captured.out


class TestRunAll:
    def test_with_workflows(self, monkeypatch, tmp_path):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        monkeypatch.setattr("capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots")
        monkeypatch.setattr("capture.capture.GIF_DIR", tmp_path / "gifs")
        monkeypatch.setattr("capture.capture.ASSETS_DIR", tmp_path / "assets")

        (workflows_dir / "wf1.yaml").write_text(
            yaml.dump({"name": "WF1", "steps": []})
        )
        (workflows_dir / "wf2.yaml").write_text(
            yaml.dump({"name": "WF2", "steps": []})
        )

        with patch(
            "subprocess.run",
            return_value=MagicMock(returncode=0, stdout="", stderr=""),
        ):
            run_all()

    def test_no_workflows(self, monkeypatch, tmp_path, capsys):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)

        run_all()
        captured = capsys.readouterr()
        assert "No workflows found" in captured.out

    def test_counts_success(self, monkeypatch, tmp_path, capsys):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        monkeypatch.setattr("capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots")
        monkeypatch.setattr("capture.capture.GIF_DIR", tmp_path / "gifs")
        monkeypatch.setattr("capture.capture.ASSETS_DIR", tmp_path / "assets")

        (workflows_dir / "ok.yaml").write_text(
            yaml.dump({"name": "OK", "steps": []})
        )
        (workflows_dir / "fail.yaml").write_text(
            yaml.dump({"name": "Fail", "steps": []})
        )

        call_count = [0]

        def mock_subprocess_run(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return MagicMock(returncode=0, stdout="", stderr="")
            return MagicMock(returncode=1, stdout="", stderr="error")

        with patch("subprocess.run", mock_subprocess_run):
            run_all()

        captured = capsys.readouterr()
        assert "Completed: 1/2 workflows" in captured.out


class TestMain:
    def test_list_flag(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["capture.py", "--list"])
        monkeypatch.setattr("capture.capture.load_env", MagicMock())
        mock_list = MagicMock()
        monkeypatch.setattr("capture.capture.list_workflows", mock_list)
        main()
        mock_list.assert_called_once()

    def test_install_flag(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["capture.py", "--install"])
        monkeypatch.setattr("capture.capture.load_env", MagicMock())
        with patch("subprocess.run") as mock_run:
            main()
        mock_run.assert_called_once_with(
            [sys.executable, "-m", "playwright", "install", "chromium"]
        )

    def test_all_flag(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["capture.py", "--all"])
        monkeypatch.setattr("capture.capture.load_env", MagicMock())
        mock_run_all = MagicMock()
        monkeypatch.setattr("capture.capture.run_all", mock_run_all)
        main()
        mock_run_all.assert_called_once()

    def test_with_workflow_path(self, monkeypatch, tmp_path):
        wf_path = tmp_path / "custom.yaml"
        wf_path.write_text(yaml.dump({"name": "Custom", "steps": []}))

        monkeypatch.setattr("sys.argv", ["capture.py", str(wf_path)])
        monkeypatch.setattr("capture.capture.load_env", MagicMock())
        monkeypatch.setattr(
            "capture.capture.WORKFLOW_DIR", tmp_path / "workflows"
        )
        monkeypatch.setattr(
            "capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots"
        )
        monkeypatch.setattr("capture.capture.GIF_DIR", tmp_path / "gifs")
        monkeypatch.setattr("capture.capture.ASSETS_DIR", tmp_path / "assets")
        mock_run_wf = MagicMock(return_value=True)
        monkeypatch.setattr("capture.capture.run_workflow", mock_run_wf)
        main()
        mock_run_wf.assert_called_once_with(wf_path)

    def test_with_workflow_name_resolved_to_dir(self, monkeypatch, tmp_path):
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir(parents=True)
        wf_path = workflows_dir / "myworkflow.yaml"
        wf_path.write_text(yaml.dump({"name": "Resolved", "steps": []}))

        monkeypatch.setattr("sys.argv", ["capture.py", "myworkflow.yaml"])
        monkeypatch.setattr("capture.capture.load_env", MagicMock())
        monkeypatch.setattr("capture.capture.WORKFLOW_DIR", workflows_dir)
        monkeypatch.setattr(
            "capture.capture.SCREENSHOT_DIR", tmp_path / "screenshots"
        )
        monkeypatch.setattr("capture.capture.GIF_DIR", tmp_path / "gifs")
        monkeypatch.setattr("capture.capture.ASSETS_DIR", tmp_path / "assets")
        mock_run_wf = MagicMock(return_value=True)
        monkeypatch.setattr("capture.capture.run_workflow", mock_run_wf)
        main()
        mock_run_wf.assert_called_once_with(wf_path)

    def test_workflow_not_found(self, monkeypatch, tmp_path):
        monkeypatch.setattr("sys.argv", ["capture.py", "nonexistent.yaml"])
        monkeypatch.setattr("capture.capture.load_env", MagicMock())
        monkeypatch.setattr(
            "capture.capture.WORKFLOW_DIR", tmp_path / "workflows"
        )
        with pytest.raises(SystemExit):
            main()

    def test_no_args_prints_help(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["capture.py"])
        monkeypatch.setattr("capture.capture.load_env", MagicMock())
        mock_print_help = MagicMock()
        monkeypatch.setattr(
            "argparse.ArgumentParser.print_help", mock_print_help
        )
        main()
        mock_print_help.assert_called_once()

    def test___name__guard_calls_main(self):
        capture_py = Path(__file__).resolve().parent.parent / "capture.py"
        old_argv = sys.argv
        sys.argv = ["capture.py", "--help"]
        try:
            runpy.run_path(str(capture_py), run_name="__main__")
        except SystemExit:
            pass
        finally:
            sys.argv = old_argv
