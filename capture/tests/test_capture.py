from pathlib import Path

from capture.capture import (
    clean_dir,
    create_gif,
    ensure_dir,
    env_substitute,
    generate_playwright_script,
)


class TestEnvSubstitute:
    def test_substitutes_defined_var(self, monkeypatch):
        monkeypatch.setenv("SOGO_URL", "https://sogo.example.com")
        result = env_substitute("${SOGO_URL}/so/user/Mail")
        assert result == "https://sogo.example.com/so/user/Mail"

    def test_undefined_var_left_as_is(self):
        result = env_substitute("${UNDEFINED_VAR}")
        assert "${UNDEFINED_VAR}" in result

    def test_no_variables(self):
        result = env_substitute("plain string")
        assert result == "plain string"

    def test_multiple_vars(self, monkeypatch):
        monkeypatch.setenv("HOST", "demo")
        monkeypatch.setenv("DOMAIN", "sogo.nu")
        result = env_substitute("https://${HOST}.${DOMAIN}/SOGo/")
        assert result == "https://demo.sogo.nu/SOGo/"


class TestEnsureDir:
    def test_creates_directory(self, tmp_path: Path):
        d = tmp_path / "new" / "nested" / "dir"
        assert not d.exists()
        ensure_dir(d)
        assert d.exists()
        assert d.is_dir()

    def test_existing_directory_does_not_fail(self, tmp_path: Path):
        d = tmp_path / "existing"
        d.mkdir(parents=True)
        ensure_dir(d)
        assert d.exists()


class TestCleanDir:
    def test_recreates_directory(self, tmp_path: Path):
        d = tmp_path / "target"
        d.mkdir(parents=True)
        (d / "file.txt").write_text("content")
        clean_dir(d)
        assert d.exists()
        assert list(d.iterdir()) == []

    def test_creates_if_not_exists(self, tmp_path: Path):
        d = tmp_path / "newdir"
        assert not d.exists()
        clean_dir(d)
        assert d.exists()


class TestCreateGif:
    def test_no_images_does_not_fail(self, tmp_path: Path):
        out = tmp_path / "out.gif"
        create_gif([], out)
        assert not out.exists()

    def test_single_image_does_not_create_gif(self, tmp_path: Path, test_png: Path):
        out = tmp_path / "out.gif"
        create_gif([test_png], out)
        assert not out.exists()

    def test_two_images_creates_gif(self, tmp_path: Path, test_png: Path):
        out = tmp_path / "out.gif"
        create_gif([test_png, test_png], out)
        assert out.exists()
        assert out.stat().st_size > 100

    def test_missing_image_skipped(self, tmp_path: Path, test_png: Path):
        out = tmp_path / "out.gif"
        missing = tmp_path / "missing.png"
        create_gif([missing, test_png, test_png], out)
        assert out.exists()


class TestGeneratePlaywrightScript:
    def test_minimal_workflow(self):
        workflow = {"name": "test", "base_url": "https://example.com", "steps": []}
        script = generate_playwright_script(workflow)
        assert "async def run():" in script
        assert "test" in script
        assert "Workflow" not in script

    def test_with_navigate_step(self):
        workflow = {
            "name": "Login",
            "base_url": "${SOGO_URL}",
            "steps": [{"id": "goto-page", "action": "navigate", "url": "/login"}],
        }
        script = generate_playwright_script(workflow)
        assert "page.goto" in script

    def test_with_click_and_type_steps(self):
        workflow = {
            "name": "Form",
            "base_url": "https://example.com",
            "steps": [
                {"id": "click-btn", "action": "click", "selector": "#btn"},
                {"id": "type-name", "action": "type", "selector": "#name", "value": "John"},
            ],
        }
        script = generate_playwright_script(workflow)
        assert "page.click" in script
        assert "page.type" in script
        assert '"John"' in script

    def test_screenshot_step(self):
        workflow = {
            "name": "Shot",
            "base_url": "https://example.com",
            "steps": [
                {"id": "capture", "action": "wait", "value": "2", "screenshot": "shot.png"},
            ],
        }
        script = generate_playwright_script(workflow)
        assert "screenshot" in script
        assert "shot.png" in script

    def test_gif_workflow(self):
        workflow = {
            "name": "Animation",
            "base_url": "https://example.com",
            "steps": [
                {
                    "id": "start",
                    "action": "wait",
                    "value": "1",
                    "gif_start": True,
                    "gif_name": "test.gif",
                },
                {"id": "end", "action": "wait", "value": "1", "gif_end": True},
            ],
        }
        script = generate_playwright_script(workflow)
        assert "gif_frames" in script
        assert "GIF created" in script

    def test_dblclick_action(self):
        workflow = {
            "name": "DblClick",
            "base_url": "https://example.com",
            "steps": [{"id": "double", "action": "dblclick", "selector": ".cell"}],
        }
        script = generate_playwright_script(workflow)
        assert "page.dblclick" in script
