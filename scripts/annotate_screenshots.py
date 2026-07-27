"""Annotate SOGo tutorial screenshots with red boxes and directional arrows.

Usage:
    python scripts/annotate_screenshots.py --all
    python scripts/annotate_screenshots.py --doc sogo-logout

Adds red bounding boxes and arrows to highlight the relevant UI element
in each screenshot. No text is drawn on the image — descriptions go in
markdown alt text.
"""

import os
import sys
import argparse
from pathlib import Path

from PIL import Image, ImageDraw

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_V5 = PROJECT_ROOT / "site" / "versioned_docs" / "version-5" / "assets"
ASSETS_V6 = PROJECT_ROOT / "site" / "versioned_docs" / "version-6" / "assets"

RED = (220, 50, 50)
RED_TRANSPARENT = (220, 50, 50, 160)
DARK_RED = (180, 30, 30)


def detect_sidebar_width(img):
    """Detect the left sidebar width by finding the teal navigation column."""
    w, h = img.size
    # Sample the first row to find where teal ends and white begins
    sidebar_w = 0
    for x in range(w):
        r, g, b = img.getpixel((x, 5))[:3]
        # Teal is around (77, 128, 128)
        if r < 100 and g > 100 and b > 100:
            sidebar_w = x + 1
        elif sidebar_w > 0 and r > 200 and g > 200 and b > 200:
            break
    return max(sidebar_w, 180)  # at least 180px


def draw_arrow(draw, x1, y1, x2, y2, color=RED, width=3):
    """Draw an arrow from (x1,y1) to (x2,y2)."""
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Arrowhead
    arrow_len = 12
    dx = x2 - x1
    dy = y2 - y1
    length = max(1, (dx*dx + dy*dy) ** 0.5)
    ux, uy = dx / length, dy / length
    # Two barbs
    barb1 = (x2 - int(ux * arrow_len - uy * arrow_len * 0.4),
             y2 - int(uy * arrow_len + ux * arrow_len * 0.4))
    barb2 = (x2 - int(ux * arrow_len + uy * arrow_len * 0.4),
             y2 - int(uy * arrow_len - ux * arrow_len * 0.4))
    draw.line([(x2, y2), barb1], fill=color, width=width)
    draw.line([(x2, y2), barb2], fill=color, width=width)


def draw_red_box(draw, x, y, w, h, color=RED, width=3):
    """Draw a red bounding box."""
    draw.rectangle([x, y, x + w, y + h], outline=color, width=width)


def annotate_logout(img, draw, sw, iw, ih):
    """Highlight the power icon in the top-right toolbar."""
    # Power icon is in the far top-right of the toolbar
    box_x = iw - 80
    box_y = 5
    box_w = 60
    box_h = 35
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    # Arrow pointing to it from the left
    draw_arrow(draw, box_x - 60, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_preferences(img, draw, sw, iw, ih):
    """Highlight the gear icon in the top toolbar."""
    # Gear icon is in the top-right area of the toolbar
    box_x = iw - 160
    box_y = 5
    box_w = 55
    box_h = 35
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 60, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_password_change(img, draw, sw, iw, ih):
    """Highlight the password form in the main content area."""
    # Password form is in the center of the main content
    box_x = sw + (iw - sw) // 4
    box_y = ih // 4
    box_w = (iw - sw) // 2
    box_h = ih // 3
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w // 2, box_y - 40, box_x + box_w // 2, box_y - 5)


def annotate_mail_folder_management(img, draw, sw, iw, ih):
    """Highlight the folder list in the sidebar."""
    # Folder list is in the sidebar
    box_x = 10
    box_y = 80
    box_w = sw - 20
    box_h = ih - 160
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w + 20, box_y + box_h // 2, box_x + box_w - 5, box_y + box_h // 2)


def annotate_mail_reply_forward_delete(img, draw, sw, iw, ih):
    """Highlight the toolbar buttons for reply/forward/delete."""
    # Toolbar buttons are above the message list
    box_x = sw + 20
    box_y = 60
    box_w = (iw - sw) - 40
    box_h = 45
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w // 2, box_y - 40, box_x + box_w // 2, box_y - 5)


def annotate_calendar_create_event(img, draw, sw, iw, ih):
    """Highlight the calendar grid time slot."""
    box_x = sw + 40
    box_y = 120
    box_w = (iw - sw) - 80
    box_h = ih - 200
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w + 20, box_y + box_h // 2, box_x + box_w - 5, box_y + box_h // 2)


def annotate_calendar_edit_delete(img, draw, sw, iw, ih):
    """Highlight an event on the calendar."""
    box_x = sw + (iw - sw) // 3
    box_y = ih // 3
    box_w = (iw - sw) // 2
    box_h = 50
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_calendar_recurring(img, draw, sw, iw, ih):
    """Highlight the recurrence dropdown in event dialog."""
    box_x = sw + (iw - sw) // 3
    box_y = ih // 3
    box_w = (iw - sw) // 2
    box_h = ih // 3
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_calendar_views(img, draw, sw, iw, ih):
    """Highlight the view selector buttons."""
    box_x = sw + 20
    box_y = 60
    box_w = (iw - sw) - 40
    box_h = 40
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w // 2, box_y - 40, box_x + box_w // 2, box_y - 5)


def annotate_calendar_share(img, draw, sw, iw, ih):
    """Highlight the sharing dialog/permissions."""
    box_x = sw + (iw - sw) // 4
    box_y = ih // 4
    box_w = (iw - sw) // 2
    box_h = ih // 2
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_calendar_subscribe(img, draw, sw, iw, ih):
    """Highlight the subscription dialog."""
    box_x = sw + (iw - sw) // 4
    box_y = ih // 4
    box_w = (iw - sw) // 2
    box_h = ih // 3
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_calendar_ical(img, draw, sw, iw, ih):
    """Highlight the import/export menu."""
    box_x = sw + 20
    box_y = 60
    box_w = (iw - sw) - 40
    box_h = 40
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w // 2, box_y - 40, box_x + box_w // 2, box_y - 5)


def annotate_freebusy(img, draw, sw, iw, ih):
    """Highlight the free/busy grid."""
    box_x = sw + 40
    box_y = 100
    box_w = (iw - sw) - 80
    box_h = ih - 180
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w + 20, box_y + box_h // 2, box_x + box_w - 5, box_y + box_h // 2)


def annotate_contacts_add(img, draw, sw, iw, ih):
    """Highlight the contact form."""
    box_x = sw + (iw - sw) // 4
    box_y = ih // 4
    box_w = (iw - sw) // 2
    box_h = ih // 2
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_contacts_edit_delete(img, draw, sw, iw, ih):
    """Highlight the contact edit/delete actions."""
    box_x = sw + (iw - sw) // 3
    box_y = ih // 3
    box_w = (iw - sw) // 2
    box_h = ih // 2
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_contacts_import_export(img, draw, sw, iw, ih):
    """Highlight the import/export menu."""
    box_x = sw + 20
    box_y = 60
    box_w = (iw - sw) - 40
    box_h = 40
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w // 2, box_y - 40, box_x + box_w // 2, box_y - 5)


def annotate_global_search(img, draw, sw, iw, ih):
    """Highlight the global search bar."""
    # Search bar is typically at the top of the interface
    box_x = sw + (iw - sw) // 4
    box_y = 10
    box_w = (iw - sw) // 2
    box_h = 40
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_mail_compose(img, draw, sw, iw, ih):
    """Highlight the compose window."""
    box_x = sw + 30
    box_y = 60
    box_w = (iw - sw) - 60
    box_h = ih - 120
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w + 20, box_y + box_h // 2, box_x + box_w - 5, box_y + box_h // 2)


def annotate_mail_read(img, draw, sw, iw, ih):
    """Highlight the message preview pane."""
    box_x = sw + 20
    box_y = 110
    box_w = (iw - sw) - 40
    box_h = ih - 170
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x + box_w // 2, box_y - 40, box_x + box_w // 2, box_y - 5)


def annotate_mail_signatures(img, draw, sw, iw, ih):
    """Highlight the signature editor."""
    box_x = sw + (iw - sw) // 4
    box_y = ih // 4
    box_w = (iw - sw) // 2
    box_h = ih // 2
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_mail_filters(img, draw, sw, iw, ih):
    """Highlight the filter rules editor."""
    box_x = sw + (iw - sw) // 4
    box_y = ih // 4
    box_w = (iw - sw) // 2
    box_h = ih // 2
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


def annotate_vacation(img, draw, sw, iw, ih):
    """Highlight the vacation auto-reply form."""
    box_x = sw + (iw - sw) // 4
    box_y = ih // 4
    box_w = (iw - sw) // 2
    box_h = ih // 2
    draw_red_box(draw, box_x, box_y, box_w, box_h)
    draw_arrow(draw, box_x - 40, box_y + box_h // 2, box_x - 5, box_y + box_h // 2)


# Map each PNG to its annotation function
ANNOTATORS = {
    "logout.png": annotate_logout,
    "preferences.png": annotate_preferences,
    "password-change.png": annotate_password_change,
    "mail-folder-management.png": annotate_mail_folder_management,
    "mail-reply-forward-delete.png": annotate_mail_reply_forward_delete,
    "calendar-create-event.png": annotate_calendar_create_event,
    "calendar-edit-delete.png": annotate_calendar_edit_delete,
    "calendar-recurring.png": annotate_calendar_recurring,
    "calendar-views.png": annotate_calendar_views,
    "calendar-share.png": annotate_calendar_share,
    "calendar-subscribe.png": annotate_calendar_subscribe,
    "calendar-ical.png": annotate_calendar_ical,
    "freebusy.png": annotate_freebusy,
    "contacts-add.png": annotate_contacts_add,
    "contacts-edit-delete.png": annotate_contacts_edit_delete,
    "contacts-import-export.png": annotate_contacts_import_export,
    "global-search.png": annotate_global_search,
    "mail-compose.png": annotate_mail_compose,
    "mail-read.png": annotate_mail_read,
    "mail-signatures.png": annotate_mail_signatures,
    "mail-filters.png": annotate_mail_filters,
    "vacation.png": annotate_vacation,
}


def annotate_screenshot(image_path, output_path):
    """Add red box and arrow annotations to a screenshot."""
    img = Image.open(image_path).convert("RGBA")
    iw, ih = img.size

    # Create an overlay layer for the annotations
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Detect sidebar width
    sw = detect_sidebar_width(img)

    # Determine which annotator to use
    fname = os.path.basename(image_path)
    annotator = ANNOTATORS.get(fname)
    if annotator:
        annotator(img, draw, sw, iw, ih)
    else:
        # Generic: highlight the main content area
        box_x = sw + 20
        box_y = 60
        box_w = (iw - sw) - 40
        box_h = ih - 100
        draw_red_box(draw, box_x, box_y, box_w, box_h)

    # Composite overlay onto original
    annotated = Image.alpha_composite(img, overlay).convert("RGB")
    annotated.save(output_path, "PNG", optimize=True)
    print(f"  ✅ {os.path.basename(output_path)}")


def main():
    parser = argparse.ArgumentParser(description="Annotate SOGo screenshots")
    parser.add_argument("--all", action="store_true", help="Process all screenshots")
    parser.add_argument("--doc", type=str, help="Process a specific doc")
    args = parser.parse_args()

    ASSETS_V5.mkdir(parents=True, exist_ok=True)

    doc_to_png = {f"sogo-{name}": name for name in [
        "logout", "preferences", "password-change",
        "mail-folder-management", "mail-reply-forward-delete",
        "calendar-create-event", "calendar-edit-delete",
        "calendar-recurring", "calendar-views", "calendar-share",
        "calendar-subscribe", "calendar-ical", "freebusy",
        "contacts-add", "contacts-edit-delete", "contacts-import-export",
        "global-search", "mail-compose", "mail-read", "mail-signatures",
        "mail-filters", "vacation",
    ]}

    if args.doc:
        png_name = doc_to_png.get(args.doc)
        if not png_name:
            print(f"Unknown doc: {args.doc}")
            sys.exit(1)
        targets = [png_name + ".png"]
    elif args.all:
        targets = list(ANNOTATORS.keys())
    else:
        print("Specify --all or --doc DOC_NAME")
        sys.exit(1)

    for png_name in targets:
        src = ASSETS_V5 / png_name
        if not src.exists():
            print(f"  ⚠️  Skipping {png_name}: not found")
            continue
        annotate_screenshot(str(src), str(src))

    print("\nDone! All screenshots annotated.")


if __name__ == "__main__":
    main()
