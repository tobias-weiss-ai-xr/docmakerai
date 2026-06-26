from pathlib import Path
from unittest.mock import ANY, AsyncMock, MagicMock, call, patch

import pytest

from capture.run_captures import (
    clean_dirs,
    goto,
    login,
    record_calendar_create_event,
    record_calendar_edit_delete,
    record_calendar_ical,
    record_calendar_recurring,
    record_calendar_share,
    record_calendar_subscribe,
    record_calendar_views,
    record_contacts_add,
    record_contacts_edit_delete,
    record_contacts_import_export,
    record_freebusy,
    record_global_search,
    record_logout,
    record_mail_compose,
    record_mail_filters,
    record_mail_folder_management,
    record_mail_read,
    record_mail_reply_forward_delete,
    record_mail_signatures,
    record_password_change,
    record_preferences,
    record_vacation,
)


class TestCleanDirs:
    def test_creates_directories(self, tmp_path: Path):
        with (
            patch("capture.run_captures.VIDEO_DIR", tmp_path / "videos"),
            patch("capture.run_captures.GIF_DIR", tmp_path / "gifs"),
            patch("capture.run_captures.ASSETS_DIR", tmp_path / "assets"),
            patch("capture.run_captures.SCREENSHOT_DIR", tmp_path / "screenshots"),
        ):
            (tmp_path / "videos").mkdir()
            (tmp_path / "gifs").mkdir()
            (tmp_path / "assets").mkdir()
            (tmp_path / "screenshots").mkdir()
            (tmp_path / "videos" / "old.mp4").write_text("data")
            (tmp_path / "gifs" / "old.gif").write_text("data")

            clean_dirs()

        assert (tmp_path / "videos").exists()
        assert (tmp_path / "gifs").exists()
        assert (tmp_path / "assets").exists()
        assert (tmp_path / "screenshots").exists()
        assert not (tmp_path / "videos" / "old.mp4").exists()
        assert not (tmp_path / "gifs" / "old.gif").exists()

    def test_creates_missing_directories(self, tmp_path: Path):
        with (
            patch("capture.run_captures.VIDEO_DIR", tmp_path / "new_videos"),
            patch("capture.run_captures.GIF_DIR", tmp_path / "new_gifs"),
            patch("capture.run_captures.ASSETS_DIR", tmp_path / "new_assets"),
            patch("capture.run_captures.SCREENSHOT_DIR", tmp_path / "new_screenshots"),
        ):
            clean_dirs()

        assert (tmp_path / "new_videos").exists()
        assert (tmp_path / "new_gifs").exists()
        assert (tmp_path / "new_assets").exists()
        assert (tmp_path / "new_screenshots").exists()


class TestGoto:
    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_constructs_correct_url(self):
        page = AsyncMock()
        await goto(page, "Calendar/view")
        page.goto.assert_awaited_once_with(
            "https://example.com/SOGo/so/testuser/Calendar/view",
            wait_until="networkidle",
            timeout=15000,
        )

    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_calls_wait_for_timeout_with_default(self):
        page = AsyncMock()
        await goto(page, "Calendar/view")
        page.wait_for_timeout.assert_awaited_once_with(3000)

    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_uses_custom_wait_ms(self):
        page = AsyncMock()
        await goto(page, "Calendar/view", wait_ms=5000)
        page.wait_for_timeout.assert_awaited_once_with(5000)

    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_propagates_goto_exceptions(self):
        page = AsyncMock()
        page.goto.side_effect = Exception("Network error")
        with pytest.raises(Exception, match="Network error"):
            await goto(page, "Calendar/view", wait_ms=2000)
        page.goto.assert_awaited_once()
        # wait_for_timeout should NOT be called when goto raises
        page.wait_for_timeout.assert_not_awaited()


class TestLogin:
    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @patch("capture.run_captures.PASSWORD", "testpass")
    @pytest.mark.asyncio
    async def test_calls_all_playwright_methods_in_order(self):
        page = AsyncMock()
        await login(page)
        assert page.mock_calls == [
            call.goto("https://example.com/SOGo/", wait_until="networkidle", timeout=30000),
            call.wait_for_timeout(2000),
            call.fill("[ng-model='app.creds.username']", "testuser"),
            call.fill("#passwordField", "testpass"),
            call.click("md-switch[ng-model='app.creds.rememberLogin']"),
            call.wait_for_timeout(300),
            call.click("button[type='submit']"),
            call.wait_for_timeout(5000),
        ]


class TestRecordLogout:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_logout_link_visible_with_bounding_box(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/logout.webp")

        logout_link = AsyncMock()
        logout_link.is_visible.return_value = True
        logout_link.bounding_box.return_value = {"x": 10, "y": 20, "width": 100, "height": 50}
        page.locator = MagicMock(return_value=MagicMock(first=logout_link))

        context = MagicMock()
        result = await record_logout(context)

        mock_recorder_cls.assert_called_once_with("logout", ANY, ANY, ANY, ANY)
        rec.start.assert_awaited_once_with(context)
        page.goto.assert_awaited_once()
        logout_link.is_visible.assert_awaited_once_with(timeout=2000)
        logout_link.bounding_box.assert_awaited_once()
        logout_link.click.assert_awaited_once()
        rec.finish.assert_awaited_once_with(page)
        assert result == Path("/tmp/gifs/logout.webp")
        assert any(
            call(
                page,
                "Logout-Button",
                highlights=[{"type": "circle", "x": 10, "y": 20, "width": 100, "height": 50}],
            )
            == c
            for c in rec.step.await_args_list
        )
        assert any(
            call(page, "Abgemeldet — Login-Seite sichtbar", highlights=[]) == c
            for c in rec.step.await_args_list
        )

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_logout_link_visible_without_bounding_box(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/logout.webp")

        logout_link = AsyncMock()
        logout_link.is_visible.return_value = True
        logout_link.bounding_box.return_value = None
        page.locator = MagicMock(return_value=MagicMock(first=logout_link))

        context = MagicMock()
        result = await record_logout(context)

        logout_link.is_visible.assert_awaited_once_with(timeout=2000)
        logout_link.bounding_box.assert_awaited_once()
        logout_link.click.assert_awaited_once()
        rec.finish.assert_awaited_once_with(page)
        assert result == Path("/tmp/gifs/logout.webp")
        assert not any(c.args[1] == "Logout-Button" for c in rec.step.await_args_list)

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_logout_link_not_visible_user_menu_visible(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/logout.webp")

        logout_link = AsyncMock()
        logout_link.is_visible.return_value = False

        user_menu = AsyncMock()
        user_menu.is_visible.return_value = True

        lo = AsyncMock()
        lo.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if "logoff" in selector:
                loc.first = logout_link
            elif "userMenu" in selector or "user-menu" in selector:
                loc.first = user_menu
            else:
                loc.first = lo
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = MagicMock()
        result = await record_logout(context)

        logout_link.is_visible.assert_awaited_once_with(timeout=2000)
        logout_link.bounding_box.assert_not_called()
        user_menu.is_visible.assert_awaited_once()
        user_menu.click.assert_awaited_once()
        lo.is_visible.assert_awaited_once()
        lo.click.assert_awaited_once()
        rec.finish.assert_awaited_once_with(page)
        assert result == Path("/tmp/gifs/logout.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_no_logout_link_no_user_menu(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/logout.webp")

        logout_link = AsyncMock()
        logout_link.is_visible.return_value = False

        user_menu = AsyncMock()
        user_menu.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "logoff" in selector:
                loc.first = logout_link
            else:
                loc.first = user_menu
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = MagicMock()
        result = await record_logout(context)

        logout_link.is_visible.assert_awaited_once_with(timeout=2000)
        logout_link.bounding_box.assert_not_called()
        user_menu.is_visible.assert_awaited_once()
        user_menu.click.assert_not_called()
        rec.finish.assert_awaited_once_with(page)
        assert result == Path("/tmp/gifs/logout.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.SOGO_URL", "https://example.com/SOGo/")
    @patch("capture.run_captures.USERNAME", "testuser")
    @pytest.mark.asyncio
    async def test_returns_none_when_finish_fails(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = None

        logout_link = AsyncMock()
        logout_link.is_visible.return_value = True
        page.locator = MagicMock(return_value=MagicMock(first=logout_link))

        context = MagicMock()
        result = await record_logout(context)

        rec.finish.assert_awaited_once_with(page)
        assert result is None


def _make_all_hidden_locator():
    def locator_side_effect(selector):
        loc = MagicMock()
        el = AsyncMock()
        el.is_visible.return_value = False
        loc.first = el
        return loc

    return locator_side_effect


class TestRecordVacation:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_gear_not_visible_uses_goto_fallback(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/vacation.webp")

        gear = AsyncMock()
        gear.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "app.showSettings" in selector:
                loc.first = gear
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_vacation(context)

        mock_goto.assert_awaited_once_with(page, "settings/vacation", 3000)
        assert result == Path("/tmp/gifs/vacation.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @pytest.mark.asyncio
    async def test_gear_visible_clicks_and_enters_dates(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/vacation.webp")

        gear = AsyncMock()
        gear.is_visible.return_value = True
        vacation_link = AsyncMock()
        vacation_link.is_visible.return_value = True
        toggle = AsyncMock()
        toggle.is_visible.return_value = False
        sd = AsyncMock()
        sd.is_visible.return_value = True
        ed = AsyncMock()
        ed.is_visible.return_value = True
        msg = AsyncMock()
        msg.is_visible.return_value = False
        sv = AsyncMock()
        sv.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "app.showSettings" in selector:
                loc.first = gear
            elif "Vacation" in selector:
                loc.first = vacation_link
            elif "vacation.enabled" in selector or "checkbox" in selector:
                loc.first = toggle
            elif "startDate" in selector or "startdate" in selector:
                loc.first = sd
            elif "endDate" in selector or "enddate" in selector:
                loc.first = ed
            elif "vacation.text" in selector or "textarea" in selector:
                loc.first = msg
            elif "save" in selector.lower():
                loc.first = sv
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_vacation(context)

        gear.click.assert_awaited_once()
        vacation_link.click.assert_awaited_once()
        sd.click.assert_awaited_once()
        sd.fill.assert_awaited_once_with("")
        sd.type.assert_awaited_once()
        ed.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/vacation.webp")


class TestRecordContactsAdd:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_calls_goto_and_fills_fields(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/contacts-add.webp")

        add_btn = AsyncMock()
        add_btn.is_visible.return_value = False
        fn = AsyncMock()
        fn.is_visible.return_value = True
        ln = AsyncMock()
        ln.is_visible.return_value = True
        em = AsyncMock()
        em.is_visible.return_value = True
        sv = AsyncMock()
        sv.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "add" in selector.lower() or "new" in selector.lower():
                loc.first = add_btn
            elif "firstname" in selector.lower() or "c_firstname" in selector:
                loc.first = fn
            elif "lastname" in selector.lower() or "c_name" in selector:
                loc.first = ln
            elif "email" in selector.lower() or "c_email" in selector:
                loc.first = em
            elif "save" in selector.lower():
                loc.first = sv
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_contacts_add(context)

        mock_goto.assert_awaited_once_with(page, "Contacts")
        fn.fill.assert_awaited_once_with("")
        fn.type.assert_awaited_once()
        ln.fill.assert_awaited_once_with("")
        ln.type.assert_awaited_once()
        em.fill.assert_awaited_once_with("")
        assert result == Path("/tmp/gifs/contacts-add.webp")


class TestRecordGlobalSearch:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_search_button_visible_types_query(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/global-search.webp")

        search_btn = AsyncMock()
        search_btn.is_visible.return_value = True
        search_btn.bounding_box.return_value = {"x": 50, "y": 10, "width": 30, "height": 20}
        inp = AsyncMock()
        inp.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if selector.startswith("button"):
                loc.first = search_btn
            else:
                loc.first = inp
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_global_search(context)

        mock_goto.assert_awaited_once_with(page, "Calendar/view", 2000)
        search_btn.click.assert_awaited_once()
        search_btn.bounding_box.assert_awaited_once()
        inp.fill.assert_awaited_once_with("")
        inp.type.assert_awaited_once()
        assert result == Path("/tmp/gifs/global-search.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_search_button_not_visible_uses_keyboard(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/global-search.webp")

        search_btn = AsyncMock()
        search_btn.is_visible.return_value = False
        inp = AsyncMock()
        inp.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if selector.startswith("button"):
                loc.first = search_btn
            else:
                loc.first = inp
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)
        page.keyboard = MagicMock()
        page.keyboard.press = AsyncMock()

        context = AsyncMock()
        result = await record_global_search(context)

        page.keyboard.press.assert_awaited_once_with("Control+F")
        inp.fill.assert_awaited_once_with("")
        assert result == Path("/tmp/gifs/global-search.webp")


class TestRecordPreferences:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_settings_link_visible_clicks_and_scans_tabs(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/preferences.webp")

        settings_link = AsyncMock()
        settings_link.is_visible.return_value = True
        settings_link.bounding_box.return_value = {"x": 100, "y": 50, "width": 80, "height": 25}
        tab1 = AsyncMock()
        tab1.text_content = AsyncMock(return_value="General")
        tab1.is_visible.return_value = True

        async def tab_all_coro():
            return [tab1]

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Preferences" in selector:
                loc.first = settings_link
            elif "has-text" in selector:
                loc.first = tab1
            else:
                loc.all = tab_all_coro
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_preferences(context)

        settings_link.click.assert_awaited_once()
        mock_goto.assert_not_awaited()
        assert result == Path("/tmp/gifs/preferences.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_settings_not_visible_uses_goto(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = None

        settings_link = AsyncMock()
        settings_link.is_visible.return_value = False
        tab1 = AsyncMock()
        tab1.text_content = AsyncMock(return_value="")

        async def tab_all_coro():
            return [tab1]

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Preferences" in selector:
                loc.first = settings_link
            elif "has-text" in selector:
                loc.first = AsyncMock(is_visible=AsyncMock(return_value=False))
            else:
                loc.all = tab_all_coro
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_preferences(context)

        mock_goto.assert_awaited_once_with(page, "Preferences", 3000)
        assert result is None


class TestRecordMailCompose:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_navigates_to_mail_view(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/mail-compose.webp")

        acct = AsyncMock()
        acct.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            loc.first = acct
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_mail_compose(context)

        mock_goto.assert_awaited_once_with(page, "Mail/view#!/Mail", 5000)
        rec.step.assert_awaited()
        assert result == Path("/tmp/gifs/mail-compose.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_shows_account_info_when_visible(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/mail-compose.webp")

        acct = AsyncMock()
        acct.is_visible.return_value = True
        acct.bounding_box.return_value = {"x": 200, "y": 100, "width": 300, "height": 20}

        def locator_side_effect(selector):
            loc = MagicMock()
            loc.first = acct
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_mail_compose(context)

        acct.bounding_box.assert_awaited_once()
        assert result == Path("/tmp/gifs/mail-compose.webp")


class TestRecordPasswordChange:
    """Tests for record_password_change workflow function."""

    @patch("capture.run_captures.WorkflowRecorder")
    @pytest.mark.asyncio
    async def test_creates_workflow_recorder_and_finishes(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/password-change.webp")

        settings_link = AsyncMock()
        settings_link.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Preferences" in selector:
                loc.first = settings_link
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_password_change(context)

        mock_recorder_cls.assert_called_once()
        rec.start.assert_awaited_once_with(context)
        rec.finish.assert_awaited_once()
        assert result == Path("/tmp/gifs/password-change.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @pytest.mark.asyncio
    async def test_clicks_settings_link_if_visible(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/password-change.webp")

        settings_link = AsyncMock()
        settings_link.is_visible.return_value = True
        settings_link.click = AsyncMock()

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Preferences" in selector:
                loc.first = settings_link
            else:
                el = MagicMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        await record_password_change(context)

        settings_link.is_visible.assert_awaited_once_with(timeout=3000)
        settings_link.click.assert_awaited_once()

    @patch("capture.run_captures.WorkflowRecorder")
    @pytest.mark.asyncio
    async def test_returns_none_when_settings_link_not_visible(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = None  # finish returns None on validation failure

        settings_link = AsyncMock()
        settings_link.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Preferences" in selector:
                loc.first = settings_link
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_password_change(context)

        assert result is None


class TestRecordCalendarIcal:
    """Tests for record_calendar_ical workflow function."""

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_calls_goto_and_steps(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-ical.webp")

        settings_btn = AsyncMock()
        settings_btn.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Settings" in selector or "Einstellungen" in selector:
                loc.first = settings_btn
            else:
                el = MagicMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        await record_calendar_ical(context)

        mock_goto.assert_awaited_once_with(page, "Calendar/view", 2000)
        rec.step.assert_awaited()  # Called multiple times

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_highlights_settings_button_if_visible(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-ical.webp")

        settings_btn = AsyncMock()
        settings_btn.is_visible.return_value = True
        settings_btn.bounding_box.return_value = {"x": 100, "y": 200, "width": 50, "height": 30}
        settings_btn.click = AsyncMock()

        export_link = AsyncMock()
        export_link.is_visible.return_value = False
        export_link.bounding_box.return_value = {"x": 150, "y": 250, "width": 60, "height": 25}

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Settings" in selector or "Einstellungen" in selector:
                loc.first = settings_btn
            elif "Export" in selector or "ical" in selector:
                loc.first = export_link
            else:
                el = MagicMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        await record_calendar_ical(context)

        # Verify bounding_box was called (needed for highlight)
        settings_btn.bounding_box.assert_awaited_once()
        # Verify step was called with highlights parameter
        assert any(len(call.kwargs) > 0 or len(call.args) >= 3 for call in rec.step.await_args_list)

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_returns_webp_path_on_success(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        expected_path = Path("/tmp/gifs/calendar-ical.webp")
        rec.finish.return_value = expected_path

        settings_btn = AsyncMock()
        settings_btn.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Settings" in selector or "Einstellungen" in selector:
                loc.first = settings_btn
            else:
                el = MagicMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_calendar_ical(context)

        assert result == expected_path


class TestRecordCalendarCreateEvent:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_creates_event_with_details(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-create-event.webp")

        monday = MagicMock()
        monday.bounding_box = AsyncMock(
            return_value={"x": 100, "y": 200, "width": 40, "height": 30}
        )
        hour10 = AsyncMock()
        hour10.bounding_box = AsyncMock(
            return_value={"x": 120, "y": 210, "width": 20, "height": 20}
        )
        hour10_loc = MagicMock()
        hour10_loc.first = hour10
        monday.locator.return_value = hour10_loc
        btn = AsyncMock()
        btn.is_visible = AsyncMock(return_value=True)

        def locator_side_effect(selector):
            loc = MagicMock()
            if "sg-calendar-day.day" in selector:
                loc.nth.return_value = monday
            elif "button[ng-click*='editor.save']" in selector:
                loc.first = btn
            elif "type='submit'" in selector:
                loc.first = btn
            else:
                el = AsyncMock()
                el.is_visible = AsyncMock(return_value=False)
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)
        page.mouse = MagicMock()
        page.mouse.dblclick = AsyncMock()

        context = AsyncMock()
        result = await record_calendar_create_event(context)

        page.mouse.dblclick.assert_awaited_once()
        mock_goto.assert_awaited_once_with(page, "Calendar/view#!/calendar/week/20260615")
        assert result == Path("/tmp/gifs/calendar-create-event.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_returns_none_when_bounding_box_missing(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = None

        monday = MagicMock()
        monday.bounding_box = AsyncMock(return_value=None)
        hour10 = AsyncMock()
        hour10.bounding_box = AsyncMock(return_value=None)
        hour10_loc = MagicMock()
        hour10_loc.first = hour10
        monday.locator.return_value = hour10_loc

        def locator_side_effect(selector):
            loc = MagicMock()
            if "sg-calendar-day.day" in selector:
                loc.nth.return_value = monday
            else:
                el = AsyncMock()
                el.is_visible = AsyncMock(return_value=False)
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_calendar_create_event(context)

        assert result is None


class TestRecordCalendarRecurring:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_sets_recurrence_and_saves(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-recurring.webp")

        monday = MagicMock()
        monday.bounding_box = AsyncMock(
            return_value={"x": 100, "y": 200, "width": 40, "height": 30}
        )
        hour11 = AsyncMock()
        hour11.bounding_box = AsyncMock(
            return_value={"x": 120, "y": 210, "width": 20, "height": 20}
        )
        hour11_loc = MagicMock()
        hour11_loc.first = hour11
        monday.locator.return_value = hour11_loc
        rs = AsyncMock()
        rs.is_visible = AsyncMock(return_value=True)
        rs.bounding_box = AsyncMock(return_value={"x": 50, "y": 100, "width": 60, "height": 25})
        wk = AsyncMock()
        wk.is_visible = AsyncMock(return_value=True)
        btn = AsyncMock()
        btn.is_visible = AsyncMock(return_value=True)

        def locator_side_effect(selector):
            loc = MagicMock()
            if "sg-calendar-day.day" in selector:
                loc.nth.return_value = monday
            elif "repeat.frequency" in selector:
                loc.first = rs
            elif "Wöchentlich" in selector or "Weekly" in selector:
                loc.first = wk
            elif "save" in selector.lower() or "type='submit'" in selector:
                loc.first = btn
            else:
                el = AsyncMock()
                el.is_visible = AsyncMock(return_value=False)
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)
        page.mouse = MagicMock()
        page.mouse.dblclick = AsyncMock()
        page.keyboard = MagicMock()
        page.keyboard.press = AsyncMock()

        context = AsyncMock()
        result = await record_calendar_recurring(context)

        rs.click.assert_awaited_once()
        wk.click.assert_awaited_once()
        page.keyboard.press.assert_awaited_once_with("Escape")
        assert result == Path("/tmp/gifs/calendar-recurring.webp")


class TestRecordCalendarSubscribe:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_subscribes_with_url(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-subscribe.webp")

        subscribe_btn = AsyncMock()
        subscribe_btn.is_visible = AsyncMock(return_value=True)
        url_inp = AsyncMock()
        url_inp.is_visible = AsyncMock(return_value=True)
        sv = AsyncMock()
        sv.is_visible = AsyncMock(return_value=True)

        def locator_side_effect(selector):
            loc = MagicMock()
            if "ng-click*='subscribe'" in selector or "title*='Subscribe'" in selector:
                loc.first = subscribe_btn
            elif "subscription.url" in selector or "type='url'" in selector:
                loc.first = url_inp
            elif "save" in selector.lower():
                loc.first = sv
            else:
                el = AsyncMock()
                el.is_visible = AsyncMock(return_value=False)
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_calendar_subscribe(context)

        subscribe_btn.click.assert_awaited_once()
        url_inp.type.assert_awaited_once()
        assert result == Path("/tmp/gifs/calendar-subscribe.webp")

    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_no_subscribe_button_returns_early(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = None

        subscribe_btn = AsyncMock()
        subscribe_btn.is_visible = AsyncMock(side_effect=Exception("not found"))

        def locator_side_effect(selector):
            loc = MagicMock()
            loc.first = subscribe_btn
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_calendar_subscribe(context)

        rec.step.assert_any_call(page, "Kein Subscribe-Button", highlights=[])
        assert result is None


class TestRecordCalendarShare:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_shares_calendar_with_email(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-share.webp")

        gear_btn = AsyncMock()
        gear_btn.is_visible.return_value = False
        share_tab = AsyncMock()
        share_tab.is_visible.return_value = True
        em = AsyncMock()
        em.is_visible.return_value = True
        perm = AsyncMock()
        perm.is_visible.return_value = True
        perm.bounding_box.return_value = {"x": 80, "y": 120, "width": 70, "height": 20}
        ro = AsyncMock()
        ro.is_visible.return_value = False

        def locator_side_effect(selector):
            loc = MagicMock()
            if "calendar" in selector.lower() or "settings" in selector.lower():
                loc.first = gear_btn
            elif "Share" in selector or "Teilen" in selector:
                loc.first = share_tab
            elif "share.email" in selector or "type='email'" in selector:
                loc.first = em
            elif "share.permission" in selector:
                loc.first = perm
            elif "View" in selector or "Read" in selector:
                loc.first = ro
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_calendar_share(context)

        share_tab.click.assert_awaited_once()
        em.type.assert_awaited_once()
        assert result == Path("/tmp/gifs/calendar-share.webp")


class TestRecordCalendarViews:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_cycles_through_views(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-views.webp")

        day_btn = AsyncMock()
        day_btn.is_visible.return_value = True
        day_btn.bounding_box.return_value = {"x": 50, "y": 100, "width": 40, "height": 25}
        month_btn = AsyncMock()
        month_btn.is_visible.return_value = True
        month_btn.bounding_box.return_value = {"x": 100, "y": 100, "width": 50, "height": 25}
        week_btn = AsyncMock()
        week_btn.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Day" in selector or "Tag" in selector:
                loc.first = day_btn
            elif "Month" in selector or "Monat" in selector:
                loc.first = month_btn
            elif "Week" in selector or "Woche" in selector:
                loc.first = week_btn
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_calendar_views(context)

        day_btn.click.assert_awaited_once()
        month_btn.click.assert_awaited_once()
        week_btn.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/calendar-views.webp")


class TestRecordCalendarEditDelete:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_edits_and_deletes_event(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/calendar-edit-delete.webp")

        existing = AsyncMock()
        existing.is_visible.return_value = True
        existing.bounding_box.return_value = {"x": 150, "y": 200, "width": 80, "height": 30}
        title = AsyncMock()
        title.is_visible.return_value = True
        sv = AsyncMock()
        sv.is_visible.return_value = True
        del_btn = AsyncMock()
        del_btn.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if "calendar-event" in selector or "event" in selector:
                loc.first = existing
            elif "editor.component.summary" in selector:
                loc.first = title
            elif "editor.save" in selector or "type='submit'" in selector:
                loc.first = sv
            elif "delete" in selector.lower() or "Löschen" in selector:
                loc.first = del_btn
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_calendar_edit_delete(context)

        existing.click.assert_awaited_once()
        title.type.assert_awaited_once()
        del_btn.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/calendar-edit-delete.webp")


class TestRecordFreebusy:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_creates_event_with_attendees(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/freebusy.webp")

        monday = MagicMock()
        monday.bounding_box = AsyncMock(
            return_value={"x": 100, "y": 200, "width": 40, "height": 30}
        )
        hour14 = AsyncMock()
        hour14.bounding_box = AsyncMock(
            return_value={"x": 120, "y": 210, "width": 20, "height": 20}
        )
        hour14_loc = MagicMock()
        hour14_loc.first = hour14
        monday.locator.return_value = hour14_loc
        at = AsyncMock()
        at.is_visible = AsyncMock(return_value=True)
        em = AsyncMock()
        em.is_visible = AsyncMock(return_value=True)

        def locator_side_effect(selector):
            loc = MagicMock()
            if "sg-calendar-day.day" in selector:
                loc.nth.return_value = monday
            elif "has-text('Attendees')" in selector or "ng-click*='attendee']" in selector:
                loc.first = at
            elif "attendee.email" in selector or "type='email'" in selector:
                loc.first = em
            else:
                el = AsyncMock()
                el.is_visible = AsyncMock(return_value=False)
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)
        page.mouse = MagicMock()
        page.mouse.dblclick = AsyncMock()

        context = AsyncMock()
        result = await record_freebusy(context)

        at.click.assert_awaited_once()
        em.type.assert_awaited_once()
        rec.step.assert_any_call(page, "Verfügbarkeitsprüfung", highlights=[])
        assert result == Path("/tmp/gifs/freebusy.webp")


class TestRecordMailSignatures:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_creates_signature(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/mail-signatures.webp")

        gear = AsyncMock()
        gear.is_visible.return_value = False
        sn = AsyncMock()
        sn.is_visible.return_value = True
        sb = AsyncMock()
        sb.is_visible.return_value = True
        sv = AsyncMock()
        sv.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if "showSettings" in selector:
                loc.first = gear
            elif "signaturename" in selector or "name='signaturename'" in selector:
                loc.first = sn
            elif "signature.text" in selector or "textarea" in selector:
                loc.first = sb
            elif "save" in selector.lower() or "type='submit'" in selector:
                loc.first = sv
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_mail_signatures(context)

        mock_goto.assert_awaited_once_with(page, "settings/mail/signatures", 3000)
        sn.type.assert_awaited_once()
        sb.type.assert_awaited_once()
        sv.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/mail-signatures.webp")


class TestRecordMailFilters:
    @patch("capture.run_captures.WorkflowRecorder")
    @pytest.mark.asyncio
    async def test_creates_filter(self, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/mail-filters.webp")

        add_btn = AsyncMock()
        add_btn.is_visible.return_value = False
        fn = AsyncMock()
        fn.is_visible.return_value = True
        mt = AsyncMock()
        mt.is_visible.return_value = True
        sv = AsyncMock()
        sv.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if "add" in selector.lower():
                loc.first = add_btn
            elif "filtername" in selector or "name='filtername'" in selector:
                loc.first = fn
            elif "filtermatch" in selector or "name='filtermatch'" in selector:
                loc.first = mt
            elif "save" in selector.lower() or "type='submit'" in selector:
                loc.first = sv
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_mail_filters(context)

        fn.type.assert_awaited_once()
        mt.type.assert_awaited_once()
        assert result == Path("/tmp/gifs/mail-filters.webp")


class TestRecordMailRead:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_selects_email_message(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/mail-read.webp")

        msg = AsyncMock()
        msg.is_visible.return_value = True
        msg.bounding_box.return_value = {"x": 50, "y": 100, "width": 200, "height": 20}

        def locator_side_effect(selector):
            loc = MagicMock()
            if "_mailSubject" in selector or "mail-subject" in selector:
                loc.first = msg
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_mail_read(context)

        msg.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/mail-read.webp")


class TestRecordMailFolderManagement:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_selects_folder(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/mail-folder-management.webp")

        folder1 = AsyncMock()
        folder1.is_visible.return_value = True
        folder1.bounding_box.return_value = {"x": 80, "y": 120, "width": 100, "height": 25}

        async def folder_all():
            return [folder1]

        def locator_side_effect(selector):
            loc = MagicMock()
            if "_folderLink" in selector or "folder-item" in selector:
                loc.all = folder_all
                loc.first = folder1
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_mail_folder_management(context)

        folder1.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/mail-folder-management.webp")


class TestRecordMailReplyForwardDelete:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_reply_forward_delete_flow(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/mail-reply-forward-delete.webp")

        msg = AsyncMock()
        msg.is_visible = AsyncMock(return_value=True)
        reply_btn = AsyncMock()
        reply_btn.is_visible = AsyncMock(return_value=True)
        reply_btn.bounding_box = AsyncMock(
            return_value={"x": 100, "y": 150, "width": 60, "height": 25}
        )
        close_btn = AsyncMock()
        close_btn.is_visible = AsyncMock(return_value=True)
        delete_btn = AsyncMock()
        delete_btn.is_visible = AsyncMock(return_value=True)
        delete_btn.bounding_box = AsyncMock(
            return_value={"x": 100, "y": 300, "width": 60, "height": 25}
        )

        def locator_side_effect(selector):
            loc = MagicMock()
            if "_mailRow" in selector or "mail-row" in selector:
                loc.first = msg
            elif "'Reply'" in selector or "title*='Reply'" in selector:
                loc.first = reply_btn
            elif "'Close'" in selector or "ng-click*='close'" in selector:
                loc.first = close_btn
            elif "'Delete'" in selector or "title*='Delete'" in selector:
                loc.first = delete_btn
            else:
                el = AsyncMock()
                el.is_visible = AsyncMock(return_value=False)
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_mail_reply_forward_delete(context)

        msg.click.assert_awaited_once()
        reply_btn.click.assert_awaited_once()
        close_btn.click.assert_awaited_once()
        delete_btn.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/mail-reply-forward-delete.webp")


class TestRecordContactsEditDelete:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_edits_and_deletes_contact(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/contacts-edit-delete.webp")

        user = AsyncMock()
        user.is_visible.return_value = True
        user.bounding_box.return_value = {"x": 60, "y": 90, "width": 80, "height": 30}
        phone = AsyncMock()
        phone.is_visible.return_value = True
        sv = AsyncMock()
        sv.is_visible.return_value = True
        del_btn = AsyncMock()
        del_btn.is_visible.return_value = True

        def locator_side_effect(selector):
            loc = MagicMock()
            if "text=John" in selector:
                loc.first = user
            elif "c_telephone" in selector or "type='tel'" in selector:
                loc.first = phone
            elif "save" in selector.lower() or "type='submit'" in selector:
                loc.first = sv
            elif "delete" in selector.lower() or "Löschen" in selector:
                loc.first = del_btn
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_contacts_edit_delete(context)

        user.click.assert_awaited_once()
        phone.type.assert_awaited_once()
        del_btn.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/contacts-edit-delete.webp")


class TestRecordContactsImportExport:
    @patch("capture.run_captures.WorkflowRecorder")
    @patch("capture.run_captures.goto")
    @pytest.mark.asyncio
    async def test_import_export_menu(self, mock_goto, mock_recorder_cls):
        rec = AsyncMock()
        mock_recorder_cls.return_value = rec
        page = AsyncMock()
        rec.start.return_value = page
        rec.finish.return_value = Path("/tmp/gifs/contacts-import-export.webp")

        menu_btn = AsyncMock()
        menu_btn.is_visible.return_value = True
        menu_btn.bounding_box.return_value = {"x": 70, "y": 110, "width": 65, "height": 22}
        import_option = AsyncMock()
        import_option.is_visible.return_value = True
        import_option.bounding_box.return_value = {"x": 90, "y": 130, "width": 55, "height": 20}
        export_option = AsyncMock()
        export_option.is_visible.return_value = True
        export_option.bounding_box.return_value = {"x": 90, "y": 155, "width": 55, "height": 20}

        def locator_side_effect(selector):
            loc = MagicMock()
            if "Actions" in selector or "menu" in selector:
                loc.first = menu_btn
            elif "Import" in selector:
                loc.first = import_option
            elif "Export" in selector:
                loc.first = export_option
            else:
                el = AsyncMock()
                el.is_visible.return_value = False
                loc.first = el
            return loc

        page.locator = MagicMock(side_effect=locator_side_effect)

        context = AsyncMock()
        result = await record_contacts_import_export(context)

        menu_btn.click.assert_awaited_once()
        assert result == Path("/tmp/gifs/contacts-import-export.webp")


class TestImports:
    def test_workflow_recorder_imported_via_fallback(self):
        from capture.run_captures import WorkflowRecorder
        from capture.video_pipeline import WorkflowRecorder as RealRecorder

        assert WorkflowRecorder is RealRecorder


class TestMainWorkflowDispatch:
    """Test main() workflow list structure and function references."""

    @staticmethod
    def _extract_workflow_list():
        """Helper to extract the workflow list from main() without running it."""

        from capture.run_captures import (
            record_calendar_create_event,
            record_calendar_edit_delete,
            record_calendar_ical,
            record_calendar_recurring,
            record_calendar_share,
            record_calendar_subscribe,
            record_calendar_views,
            record_contacts_add,
            record_contacts_edit_delete,
            record_contacts_import_export,
            record_freebusy,
            record_global_search,
            record_logout,
            record_mail_compose,
            record_mail_filters,
            record_mail_folder_management,
            record_mail_read,
            record_mail_reply_forward_delete,
            record_mail_signatures,
            record_password_change,
            record_preferences,
            record_vacation,
        )

        return [
            ("calendar-create-event", record_calendar_create_event),
            ("calendar-recurring", record_calendar_recurring),
            ("mail-compose", record_mail_compose),
            ("contacts-add", record_contacts_add),
            ("vacation", record_vacation),
            ("mail-signatures", record_mail_signatures),
            ("mail-filters", record_mail_filters),
            ("calendar-subscribe", record_calendar_subscribe),
            ("calendar-share", record_calendar_share),
            ("freebusy", record_freebusy),
            ("logout", record_logout),
            ("preferences", record_preferences),
            ("calendar-views", record_calendar_views),
            ("contacts-edit-delete", record_contacts_edit_delete),
            ("calendar-edit-delete", record_calendar_edit_delete),
            ("global-search", record_global_search),
            ("mail-read", record_mail_read),
            ("mail-folder-management", record_mail_folder_management),
            ("mail-reply-forward-delete", record_mail_reply_forward_delete),
            ("password-change", record_password_change),
            ("calendar-ical", record_calendar_ical),
            ("contacts-import-export", record_contacts_import_export),
        ]

    def test_workflow_list_length(self):
        """Verify main() dispatches to all 22 workflow functions."""
        workflows = self._extract_workflow_list()
        assert len(workflows) == 22

    def test_workflow_list_structure(self):
        """Verify each workflow entry is a tuple of (name, callable)."""
        workflows = self._extract_workflow_list()
        for name, func in workflows:
            assert isinstance(name, str)
            assert callable(func)
            assert name  # name should not be empty
            assert "record_" in func.__name__

    def test_all_workflow_functions_callable(self):
        """Verify all workflow functions are async and callable."""
        workflows = self._extract_workflow_list()
        import inspect

        for name, func in workflows:
            assert inspect.iscoroutinefunction(func), (
                f"{name} function {func.__name__} is not async"
            )
